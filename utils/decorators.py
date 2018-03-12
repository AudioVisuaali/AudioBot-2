def Commit(fn):
    def wrapper(self, *args, **kwargs):
        og_fn = fn(self, *args, **kwargs)
        self.session.commit()
        return og_fn
    return wrapper

def IsBoolean(fn):
    def wrapper(self, id, boolean, *args, **kwargs):
        if not isinstance(boolean, (bool)):
            return False
        og_fn = fn(self, id, boolean, *args, **kwargs)
        return og_fn
    return wrapper

def IsInteger(fn):
    def wrapper(self, id, integer, *args, **kwargs):
        if not isinstance(integer, (int)):
            return False
        og_fn = fn(self, id, integer, *args, **kwargs)
        return og_fn
    return wrapper

def IsString(fn):
    def wrapper(self, id, string, *args, **kwargs):
        if not isinstance(string, (str)):
            return False
        og_fn = fn(self, id, string, *args, **kwargs)
        return og_fn
    return wrapper

def MaxFifty(fn):
    def wrapper(self, id, integer, *args, **kwargs):
        if integer > 50:
            return False
        og_fn = fn(self, id, integer, *args, **kwargs)
        return og_fn
    return wrapper
