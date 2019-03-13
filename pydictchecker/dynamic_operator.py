from pydictchecker.config.global_config import __all_comparators__, __all_casts__


class DynamicOperation:

    @staticmethod
    def compare(input_value, comparator_str, comparative_value, cast_to=None):

        if not comparator_str or comparator_str not in __all_comparators__:
            raise Exception('"operator_str" must be defined and/or be a valid operator (cf. __all_operators__')

        if cast_to is not None and cast_to not in __all_casts__:
            raise Exception('"cast_to" is not a valid cast (cf. __all_casts__')

        try:
            if cast_to is not None:
                input_value = __all_casts__[cast_to](input_value)

            return __all_comparators__[comparator_str](input_value, comparative_value)

        except Exception:  # There was an issue casting the value
            return False
