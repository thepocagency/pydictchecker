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
        path_list = PyDictChecker._split(_path_str)
        return PyDictChecker._get_sub_dict_by_path_list(_current_dict, path_list)

    @staticmethod
    def check(_current_dict={}, _conditions=[]):

        _is_valid = True

        for _current_condition in _conditions:

            if global_config.__key_path__ not in _current_condition:
                raise Exception("{} has to be defined".format(global_config.__key_path__))

            # Means: with a tuple (comparator + comparative_value + cast_to)
            is_terminal_node = (global_config.__key_conditions__ not in _current_condition
                                and global_config.__key_comparator__ in _current_condition
                                and global_config.__key_comparative_value__ in _current_condition
                                and global_config.__key_cast_to__ in _current_condition)

            # Means: with a sub-conditions array
            is_middle_node = (global_config.__key_conditions__ in _current_condition
                                and global_config.__key_comparator__ not in _current_condition
                                and global_config.__key_comparative_value__ not in _current_condition
                                and global_config.__key_cast_to__ not in _current_condition)

            if not is_terminal_node and not is_middle_node:
                raise Exception("One of the condition is not valid: it has to contain a (sub)-condition array or a tuple (comparator+comparative_value+cast_to)")

            _path_string = _current_condition[global_config.__key_path__]
            _current_sub_node = PyDictChecker._get_sub_node(_current_dict, _path_string)

            if _current_sub_node is None:
                return False

            if is_terminal_node:
                _comparator = _current_condition[global_config.__key_comparator__]
                _comparative_value = _current_condition[global_config.__key_comparative_value__]
                _cast_to = _current_condition[global_config.__key_cast_to__]

                _is_valid = (_is_valid and DynamicOperation.compare(_current_sub_node,
                                                                    _comparator,
                                                                    _comparative_value,
                                                                    _cast_to))
            else:
                _sub_conditions = _current_condition[global_config.__key_conditions__]
                _is_valid = (_is_valid and PyDictChecker.check(_current_sub_node, _sub_conditions))

        return _is_valid
