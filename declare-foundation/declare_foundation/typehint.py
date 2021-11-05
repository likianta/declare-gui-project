from typing import *

if __name__ == '__main__':
    from declare_foundation.context_manager.contextable import Contextable \
        as _Contextable
else:
    _Contextable = None

TUid = str


class TContext:
    Component = object
    Context = List[Tuple[Component, 'Context']]
    Level = int
    IdChain = Dict[Level, int]
    Uid = TUid
    UidList = List[Uid]


class TContextable:
    Component = Optional[_Contextable]
    Function = Callable
    Uid = TUid
