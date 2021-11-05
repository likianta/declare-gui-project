from lk_logger import lk

from .context_manager import ctx_mgr
from .id_system import id_mgr
from ..typehint import TContextable as T

_pointer = None  # NOTE: this is a workaround for `ContextWrapper.build`.


class Contextable:
    uid: T.Uid
    _exit_lock: int
    
    def __enter__(self):
        self._exit_lock = _ctx_lock.fetch_lock()
        self.uid = ctx_mgr.upgrade(self)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # self._exit_lock:
        #   0 : exitable
        #   1+: not exitable for now, we will decrease `self._exit_lock` count
        #       and waiting for the next call
        if self._exit_lock > 0:
            self._exit_lock -= 1
            global _pointer
            _pointer = self
            return
        ctx_mgr.downgrade()
        id_mgr.set(self.uid, self)


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


_ctx_lock = ContextLock()


class ContextWrapper:
    _comp: T.Component
    _func: T.Function
    
    def __init__(self, func):
        self._func = func
    
    def __enter__(self):
        _ctx_lock.put_a_lock(1)
        return self
    
    def build(self, *args, **kwargs):
        self._comp = self._func(*args, **kwargs)
        if self._comp is None:
            lk.logt('[W0314]', 'The wrapped function should return its '
                               'component. (Here we use a workaround to fix '
                               'this issue.)', h='parent')
            self._comp = _pointer
        return self._comp
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._comp.__exit__(exc_type, exc_val, exc_tb)


Builder = ContextWrapper  # the alias name is more popular with developers.
