from .__ext__ import T


class _BaseClass:
    pass


def base_setattr(self, name, value):
    _BaseClass.__setattr__(self, name, value)


def base_getattr(self, name):
    return _BaseClass.__getattribute__(self, name)


# -----------------------------------------------------------------------------

PROPS = '_properties'


class PropGetterAndSetter:
    _properties: T.Properties
    
    def __init__(self):
        # the subclass should update `properties` in its `__init__` method.
        self._properties = {}
    
    def __getattr__(self, key: str):
        if key == PROPS:
            try:
                return base_getattr(self, PROPS)
            except AttributeError:
                return ()
        elif key.startswith('_'):
            return base_getattr(self, key)
        
        if key in self._properties:
            return self.__getprop__(key)
        else:
            return self.__getattribute__(key)
    
    def __setattr__(self, key: str, value):
        if key == PROPS or key.startswith('_'):
            base_setattr(self, key, value)
            return
        
        if key in self._properties:
            self.__setprop__(key, value)
        else:
            base_setattr(self, key, value)
    
    def __getprop__(self, key):
        return self._properties[key]
    
    def __setprop__(self, key, value):
        self._properties[key].set(value)
