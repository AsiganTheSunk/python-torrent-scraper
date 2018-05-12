class StringUtils():
    def __init__(self):
        return

    def eval_wrapped_key(self, value, wrap_type):
        '''
        This function peform auxiliary help to the build name functions validating the content of the string
        :param value: It represents the key you'regex testing
        :param wrap_type: It represents the type of wrapping the string it's going to get, numbers 0 to 2, being
                        0 for [value], 1 for (value), 2 for -(value) 3 value
        :return: modified value
        '''
        if value is None:
            return ''
        else:
            if wrap_type is -1:
                if value is '':
                    return ''
                return (' ' + value)
            elif wrap_type is 0:
                if value is '':
                    return value
                return (' [' + value + ']')
            elif wrap_type is 1:
                if value is '':
                    return value
                return (' (' + value + ')')
            elif wrap_type is 2:
                if value is '':
                    return value
                return (' - (' + value + ')')
            elif wrap_type is 3:
                if value is '':
                    return value
                return ('.' + value)
            elif wrap_type is 4:
                if value is '':
                    return value
                return (' - ' + value)
            else:
                return value
