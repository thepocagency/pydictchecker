import operator

__version__ = "0.0.2"


__default_path_delimiter__ = '->'
__default_result_is_valid__ = 'is_valid'
__default_result_output__ = 'result'

__key_conditions__ = 'conditions'
__key_path__ = 'path'
__key_output__ = 'output'

__key_comparator__ = 'comparator'
__key_comparative_value__ = 'comparative_value'
__key_cast_to__ = 'cast_to'
__key_cast_to_int__ = ':int:'

__key_array_function_pos__ = ':pos:'
__key_array_function_first__ = ':first:'
__key_array_function_last__ = ':last:'

__all_array_functions__ = [
    __key_array_function_pos__,
    __key_array_function_first__,
    __key_array_function_last__
]

__all_comparators__ = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne
}

__all_casts__ = {
    __key_cast_to_int__: int,
}
