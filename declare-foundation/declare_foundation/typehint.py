from os import PathLike as _PathLike
from typing import *

from lk_lambdex import lambdex as _lambdex

_TFakeModule = _lambdex('', """
    class FakeModule:
        def __getattr__(self, item):
            return None
        def __call__(self, *args, **kwargs):
            return None
    return FakeModule()
""")()

# some fake imports. it is uesful to improve ide code completion and type
# checks. they are not actually used in this module.
if __name__ == '__main__':
    from declare_foundation.context_manager import contextable as _contextable
    from declare_foundation.prop_sheet import base as _base_prop_sheet
    from declare_foundation.property import base as _base_properties
else:
    _base_prop_sheet = _TFakeModule
    _base_properties = _TFakeModule
    _contextable = _TFakeModule

# ------------------------------------------------------------------------------

TPath = Union[str, _PathLike]

TUid = str
TName = str
TFullName = str
TPropName = str

TProperty = _base_properties.Property
TPropertyGroup = _base_properties.PropertyGroup

TLevel = int
TComponent = _contextable.Contextable


class TsContextManager:
    Component = Optional[TComponent]
    Context = List[Tuple[Component, 'Context']]
    Function = Callable
    Level = int
    IdChain = Dict[Level, int]
    Uid = TUid
    UidList = List[Uid]


class TsPropSheet:
    # noinspection PyUnresolvedReferences,PyProtectedMember
    from typing import _UnionGenericAlias as RealUnionType
    
    Constructable = Callable
    PropSheet = _base_prop_sheet.PropSheet
    PropSheetIter = Iterator[_base_prop_sheet.PropSheet]
    PropsIter = Iterator[Tuple[TPropName, TProperty]]
    RawType = Union[TProperty, RealUnionType]
    Target = Union[TComponent,
                   _base_properties.PropertyGroup,
                   _base_prop_sheet.PropSheet]


class TsProperty:
    Any = Any
    Name = TName
    FullName = TFullName
    GroupName = TName
    PropName = TPropName
    Uid = TUid


class TsTraits:
    Properties = Dict[TPropName, Union[TProperty, TPropertyGroup]]
