from functools import wraps


def mana_requirement(mana_cost):
    def resource_requirement(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            if mana_cost <= self.current_mp:
                return func(*args, **kwargs)
            return False
        return wrapper
    return resource_requirement


def fury_requirement(fury_cost):
    def resource_requirement(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            if fury_cost <= self.current_fury:
                return func(*args, **kwargs)
            return False
        return wrapper
    return resource_requirement


def health_requirement(health_trigger):
    def resource_requirement(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            if (self.max_hp * int(health_trigger/100)) <= self.current_hp:
                return func(*args, **kwargs)
            return False
        return wrapper
    return resource_requirement

