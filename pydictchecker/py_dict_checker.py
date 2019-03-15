from pydictchecker.config import global_config
from pydictchecker.dynamic_operator import DynamicOperation


class PyDictChecker:

    @staticmethod
    def _is_array_function(_final_path=''):

        # If it is an empty path or if there is a '->', that means it is not a final path
        if not _final_path or global_config.__default_path_delimiter__ in _final_path:
            return False, None

        for _possible_array_path in global_config.__all_array_functions__:
            if _possible_array_path in _final_path:

                _position = None

                if _possible_array_path == global_config.__key_array_function_pos__:
                    _position = _final_path.split(global_config.__key_array_function_pos__, 1)[1]

                if _possible_array_path == global_config.__key_array_function_first__:
                    _position = 0

                if _possible_array_path == global_config.__key_array_function_last__:
                    _position = -1

                try:
                    _position = int(_position)
                except Exception:
                    raise Exception("position not defined after the array function")

                return True, _position

        return False, None

    @staticmethod
    def _split(_path_str=''):
        """
        Split a path (using the default '->' separator) into a list of strings
        :param path_str (example: 'toto->titi')
        :return: a list of strings (example: ['toto', 'titi']
        """
        if not _path_str:
            return []

        if _path_str and global_config.__default_path_delimiter__ not in _path_str:
            return [_path_str]

        return _path_str.split(global_config.__default_path_delimiter__)

    @staticmethod
    def _get_sub_dict_by_path_list(_current_dict={}, _path_list=[]):

        if len(_path_list) == 0:
            raise Exception("path_list can not be empty")

        _current_path = _path_list[0]
        sub_dict = {}

        if isinstance(_current_dict, list):

            if len(_current_dict) == 0:
                return None

            _is_array_function, _position = PyDictChecker._is_array_function(_current_path)

            if _is_array_function:
                try:
                    sub_dict = _current_dict[_position]
                except Exception:  # If there is a range exception...
                    return None
        else:

            if _current_path not in _current_dict:
                return None

            sub_dict = _current_dict[_current_path]

        if len(_path_list) > 1:
            _path_list.pop(0)  # Remove the first element
            return PyDictChecker._get_sub_dict_by_path_list(sub_dict, _path_list)
        else:
            return sub_dict

    @staticmethod
    def _get_sub_node(_current_dict={}, _path_str=''):
        return PyDictChecker._get_sub_dict_by_path_list(_current_dict, PyDictChecker._split(_path_str))

    @staticmethod
    def _print_result(_is_valid=True, _output_value=None):
        return {
            global_config.__default_result_is_valid__: _is_valid,
            global_config.__default_result_output__: _output_value
        }

    @staticmethod
    def _check(_current_dict={}, _conditions=[], _is_valid=True, _output_value=None):

        for _current_condition in _conditions:

            # Before complex step: always return if False
            if not _is_valid:
                return PyDictChecker._print_result(_is_valid, _output_value)

            if global_config.__key_path__ not in _current_condition:
                raise Exception("{} has to be defined".format(global_config.__key_path__))

            _path_string = _current_condition[global_config.__key_path__]
            _current_sub_node = PyDictChecker._get_sub_node(_current_dict, _path_string)

            if _current_sub_node is None:
                _is_valid = False

            # Set the output if the user asked for it
            # In this case, we always return the latest deepest node (if there is many 'output' in the conditions)
            if ((global_config.__key_output__ in _current_condition
                    and _current_condition[global_config.__key_output__] is True)
                    or _output_value is None):
                _output_value = _current_sub_node

            # If there is a condition
            if (_is_valid and global_config.__key_conditions__ not in _current_condition
                    and global_config.__key_comparator__ in _current_condition
                    and global_config.__key_comparative_value__ in _current_condition
                    and global_config.__key_cast_to__ in _current_condition):

                _comparator = _current_condition[global_config.__key_comparator__]
                _comparative_value = _current_condition[global_config.__key_comparative_value__]
                _cast_to = _current_condition[global_config.__key_cast_to__]

                _is_valid = (_is_valid and DynamicOperation.compare(_current_sub_node,
                                                                    _comparator,
                                                                    _comparative_value,
                                                                    _cast_to))

            # If there are some sub-conditions to run
            if _is_valid and global_config.__key_conditions__ in _current_condition:

                _sub_conditions = _current_condition[global_config.__key_conditions__]

                _sub_result = PyDictChecker._check(_current_sub_node,
                                                   _sub_conditions,
                                                   _is_valid,
                                                   _output_value)

                _is_valid = (_is_valid and _sub_result[global_config.__default_result_is_valid__])
                _output_value = _sub_result[global_config.__default_result_output__]

        return PyDictChecker._print_result(_is_valid, _output_value)

    @staticmethod
    def check(_current_dict={}, *_conditions):

        _condition_array = []

        for _current_condition in _conditions:
            _condition_array.append(_current_condition)

        return PyDictChecker._check(_current_dict, _condition_array)
