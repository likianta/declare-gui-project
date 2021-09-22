from typing import List
from typing import Optional

from ..context_manager import context
from ..context_manager import parent
from ..context_manager import this
from ..context_manager.uid_system import UID
from ..context_manager.uid_system import gen_id
from ..context_manager.uid_system import id_ref


class BaseComponent:
    parent: Optional['BaseComponent']
    children: List['BaseComponent']
    
    # initialized at `self.__enter__`
    level: int
    uid: UID
    
    __exit_lock: int
    
    def __init__(self):
        self.parent = None
        self.children = []
    
    def bind(self, *args, **kwargs):
        pass
    
    def gain(self, *args, **kwargs):
        pass
    
    def build(self):
        """
        Build self contained components (aka children components) within self's
        context.
        
        Examples:
            class AddressBar(BaseComponent):
                def build(self):
                    with Input() as inp:
                        inp.hint = 'Place in a file address'
                        
            with Windows() as win:
                with AddressBar() as addr_bar:
                    addr_bar.anchors.bind(
                        win.left, win.top, win.right, None
                    )
        """
        pass
    
    def __enter__(self):
        """
        Warnings:
            This method is not recommended to override. You can use `self
            ._inject_enter_code` instead.
        """
        global _com_exit_lock
        self.__exit_lock = _com_exit_lock.fetch_lock()
        
        # for now, `this` keyword represents 'the last' component (usually it
        # means 'parent' component), so we get the last component's real
        # instance by `this.represents`
        last_com = this.represents  # type: [BaseComponent, None]
        
        self.level = last_com.level + 1 if last_com is not None else 0
        self.uid = gen_id(self.level)
        
        context.update(self.uid, self.level, self, last_com)
        #   after `context.update`, `this` and `parent` now work as expected.
        #   i.e. now `this` represents `self`, and `parent` represents
        #   `last_com`.
        
        self.parent = parent.represents
        self.parent.children.append(self)
        
        self._inject_enter_code()
        
        return self

    def _inject_enter_code(self):
        pass

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
        if self.__exit_lock > 0:
            self.__exit_lock -= 1
            return
        
        self.build()
        
        self._inject_exit_code(this.represents, parent.represents)
        
        this.point_to(id_ref[(pid := self.uid.parent_id)])
        parent.point_to(id_ref[pid.parent_id] if pid else None)
    
    def _inject_exit_code(self, child_com, parent_com):
        pass


class Build:
    """
    Examples:
        def add_splash():
            with Image() as img:
                return img
        with HomePage() as home:
            with Build(add_splash) as splash:
                ...
    """
    
    def __init__(self, build_func, *args, **kwargs):
        self._build_func = lambda: build_func(*args, **kwargs)
        self._component = None
    
    def __enter__(self):
        global _com_exit_lock
        _com_exit_lock.put_a_lock(1)
        
        self._component = self._build_func()
        if self._component is None:
            self._component = this.represents
            assert self._component is not None
        
        return self._component
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._component.__exit__(exc_type, exc_val, exc_tb)


class ComponentExitLock:
    """
    Mechanism:
        See `docs/what-is-component-exit-lock.zh.md`.
    """
    
    _count = 0
    
    def fetch_lock(self):
        out = self._count
        self.reset_lock()
        return out
    
    def reset_lock(self):
        self._count = 0
    
    def put_a_lock(self, count=1):
        # only `class:Build` calls this method.
        self._count = count


_com_exit_lock = ComponentExitLock()
