from typing import List
from typing import Optional

from .dict_tree import DictTreeEx
from .keywords import parent
from .keywords import this
from .uid_system import UID
from .uid_system import gen_id
from .uid_system import id_ref


class ContextManager:
    # component tree
    _tree = DictTreeEx(
        {'uid': None, 'level': 0, 'com': None, 'children': {}},
        setin='children'
    )
    ''' {
            uid: {
                'uid': `uid_system.UID|None`,
                'level': `int 0|1|2|3|...`,
                'com': `comonents/base_component.py:BaseComponent`,
                'children': {
                    uid: {
                        'uid': ...,
                        'level': ...,
                        'com': ...,
                        'children': { ... }
                    }, ...
                }
            }, ...
        }
    '''
    
    def update(self, uid, layer_level, com, last_com):
        """
        Returns:
            (this, parent)
        """
        parent_id = str(uid.parent_id)
        uid = str(uid)
        
        kwargs = {'uid': uid, 'level': layer_level, 'com': com}
        
        curr_level = layer_level
        last_level = last_com.level if last_com else -1
        
        if curr_level > last_level:
            self._tree.insert_inside(uid, **kwargs)
        elif curr_level == last_level:
            self._tree.insert_beside(uid, **kwargs)
        else:
            if (dedent_count := last_level - curr_level) == 1:
                self._tree.insert_ouside(uid, **kwargs)
            else:
                # noinspection PyTypeChecker
                for key in ([None] * (dedent_count - 1) + [uid]):
                    self._tree.insert_ouside(key)
        
        # ----------------------------------------------------------------------
        # update `id_ref`, `this` and `parent` pointers
        
        this_com = id_ref[uid] = com
        parent_com = id_ref[parent_id]
        
        this.point_to(this_com)
        parent.point_to(parent_com)
        
        return this, parent


class Context:
    level: int
    uid: UID
    parent: Optional['Context']
    children: List['Context']
    _exit_lock: int

    def __init__(self):
        self.parent = None
        self.children = []

    def __enter__(self):
        """
        Warnings:
            This method is not recommended to override. You can use `self
            ._inject_enter_code` instead.
        """
        global _ctx_lock
        self._exit_lock = _ctx_lock.fetch_lock()
        
        # for now, `this` keyword represents 'the last' component (usually it
        # means 'parent' component), so we get the last component's real
        # instance by `this.represents`
        last_com = this.represents
        
        self.level = last_com.level + 1 if last_com is not None else 0
        self.uid = gen_id(self.level)
        
        ctx_mgr.update(self.uid, self.level, self, last_com)
        #   after `context.update`, `this` and `parent` now work as expected.
        #   i.e. now `this` represents `self`, and `parent` represents
        #   `last_com`.
        
        if parent.represents:
            self.parent = parent.represents
            self.parent.children.append(self)
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Change `this` and `parent` points to `parent` and `parent.parent`.
        
        Warnings:
            This method is not recommended to override. You can use `self
            ._inject_exit_code` instead.
        """
        # self._exit_lock:
        #   0 : exitable
        #   1+: not exitable for now, we will decrease `self._exit_lock` count
        #       and waiting for the next call
        if self._exit_lock > 0:
            self._exit_lock -= 1
            return
        
        this.point_to(id_ref[(pid := self.uid.parent_id)])
        parent.point_to(id_ref[pid.parent_id] if pid else None)


class ContextLock:
    """
    Mechanism:
        See `docs/what-is-context-lock.zh.md`.
    """
    _count = 0
    
    def fetch_lock(self) -> int:
        out = self._count
        self.reset_lock()
        return out
    
    def reset_lock(self):
        self._count = 0
    
    def put_a_lock(self, count=1):
        # only `class:Build` calls this method.
        self._count = count


class ContextLockScheduler:
    
    def __init__(self, build_func, *args, **kwargs):
        self._build_func = lambda: build_func(*args, **kwargs)
        self._component = None
    
    def __enter__(self):
        global _ctx_lock
        _ctx_lock.put_a_lock(1)
        
        self._component = self._build_func()
        if self._component is None:
            self._component = this.represents
            assert self._component is not None
        
        return self._component
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._component.__exit__(exc_type, exc_val, exc_tb)


ctx_mgr = ContextManager()
_ctx_lock = ContextLock()
