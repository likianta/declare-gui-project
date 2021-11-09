from .__ext__ import PropGetterAndSetter
from .__ext__ import T

__all__ = ['Property', 'PropertyGroup']


class Property:
    uid: T.Uid
    name: T.PropName
    value: T.Any
    
    def __init__(self, uid: T.Uid, name: T.Name, default_value=None):
        """
        
        Args:
            uid:
            name:
            default_value: Optional[Any]
                None: no value defined, it won't be generated to QML layout.
                      See the process logic in: `..builder.build_properties`.
                It is suggested that the subclasses do not modify default_value
                in its __init__ method.
        """
        self.uid = uid
        self.name = name
        self.value = default_value
    
    def kiss(self, arg_0):
        self.value = arg_0
        # if isinstance(arg_0, Property):
        #     self.value = arg_0.value
        # else:
        #     self.value = arg_0
    
    set = kiss  # alias (this is more popular to use)
    
    def bind(self, *args, **kwargs):
        pass
    
    @property
    def fullname(self) -> T.FullName:
        return f'{self.uid}.{self.name}'


class PropertyGroup(PropGetterAndSetter):
    uid: T.Uid
    # overwrite this value in subclass level.
    # see typical usage in `.group_properties.Anchors`.
    name: T.GroupName
    
    # _properties: T.Properties  # came from super class.
    
    def __init__(self, uid: T.Uid, *_):
        PropGetterAndSetter.__init__(self)
        self.uid = uid
        from declare_foundation.prop_sheet import init_prop_sheet
        init_prop_sheet(self, prefix=self.name)
    
    def kiss(self, _):
        raise Exception(
            'PropertyGroup doesnt support `kiss` method. '
            'You can only call its sub property to set values.'
        )
    
    set = kiss
    
    def bind(self, *_):
        raise Exception(
            'PropertyGroup doesnt support `bind` method. '
            'You can only call its sub property to bind values.'
        )
    
    @property
    def fullname(self) -> T.FullName:
        return f'{self.uid}.{self.name}'
    
    @property
    def properties(self):
        return self._properties
    
    def adapt(self) -> str:
        return self.fullname
