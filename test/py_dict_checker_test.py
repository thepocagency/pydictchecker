# coding=utf-8

import unittest
import pydictchecker.config.global_config as config
from pydictchecker.py_dict_checker import PyDictChecker


class PyDictCheckerTest(unittest.TestCase):

    def test_is_array_function(self):

        _is_array_function, _position = PyDictChecker._is_array_function()
        self.assertFalse(_is_array_function)

        _is_array_function, _position = PyDictChecker._is_array_function('Johnny->Hallyday->will->never_die')
        self.assertFalse(_is_array_function)

        try:
            _is_array_function, _position = PyDictChecker._is_array_function(':pos:')
        except Exception:
            self.assertTrue(True, 'Exception is expected because there is no position value given after the key')

        _is_array_function, _position = PyDictChecker._is_array_function(':pos:2')
        self.assertTrue(_is_array_function and _position == 2)

        _is_array_function, _position = PyDictChecker._is_array_function(':first:')
        self.assertTrue(_is_array_function and _position == 0)

        _is_array_function, _position = PyDictChecker._is_array_function(':last:')
        self.assertTrue(_is_array_function and _position == -1)

        _is_array_function, _position = PyDictChecker._is_array_function(':rock:')
        self.assertTrue(not _is_array_function and _position is None)

    def test_split(self):

        path_list = PyDictChecker._split()
        self.assertTrue(len(path_list) == 0)

        path_list = PyDictChecker._split('')
        self.assertTrue(len(path_list) == 0)

        path_list = PyDictChecker._split('Johnny')
        self.assertTrue(len(path_list) == 1)
        self.assertTrue(path_list[0] == 'Johnny')

        path_list = PyDictChecker._split('Johnny->Hallyday')
        self.assertTrue(len(path_list) == 2)
        self.assertTrue(path_list[1] == 'Hallyday')

        path_list = PyDictChecker._split('Johnny->0->Hallyday')
        self.assertTrue(len(path_list) == 3)
        self.assertTrue(path_list[2] == 'Hallyday')

    def test_get_sub_dict_by_path_list(self):

        try:
            PyDictChecker._get_sub_dict_by_path_list({}, [])
        except Exception:
            self.assertTrue(True, 'Exception is expected because the "path_list" is empty')

        current_dict = {'I_love': 'Johnny Hallyday'}
        self.assertIsNone(PyDictChecker._get_sub_dict_by_path_list(current_dict, ['I_dont_love']))

        current_dict = {'The_best?': 'Johnny Hallyday'}
        self.assertEqual(PyDictChecker._get_sub_dict_by_path_list(current_dict, ['The_best?']), 'Johnny Hallyday')

        current_dict = {'Johnny_Hallyday': {'Is_he_alive?': True, 'Do_I_love_him?': True}}
        self.assertTrue(PyDictChecker._get_sub_dict_by_path_list(current_dict, ['Johnny_Hallyday', 'Is_he_alive?']))

        # To test the position

        current_dict = {
            'artists': [
                {
                    'firstname': 'Johnny',
                    'lastname': 'hallyday'
                }
            ]
        }

        try:
            PyDictChecker._get_sub_dict_by_path_list(current_dict, ['artists', ':pos:', 'firstname'])
        except Exception:
            self.assertTrue(True, 'Exception is expected because there is no position value after :pos:')

        self.assertEqual(PyDictChecker._get_sub_dict_by_path_list(current_dict, ['artists', ':pos:0', 'firstname']),
                         'Johnny')

        self.assertEqual(PyDictChecker._get_sub_dict_by_path_list(current_dict, ['artists', ':first:', 'firstname']),
                         'Johnny')

        self.assertEqual(PyDictChecker._get_sub_dict_by_path_list(current_dict, ['artists', ':last:', 'firstname']),
                         'Johnny')

        self.assertIsNone(PyDictChecker._get_sub_dict_by_path_list(current_dict, ['artists', ':pos:2', 'firstname']))

    def test_get_sub_node(self):
        current_dict = {'Johnny_Hallyday': {'Nickname': {'English': 'The French Elvis'}}}
        self.assertEqual(PyDictChecker._get_sub_node(current_dict, 'Johnny_Hallyday->Nickname->English'),
                         'The French Elvis')

    def test_check(self):
        # The dictionnary we want to check. Of course, it could be a original JSON, converted into a dict
        music_library = {
            'artists': [
                {
                    'id': 1,
                    'real_name': {
                        'firstname': "Jean - Philippe Léo",
                        'lastname': 'Smet'
                    },
                    'artist_name' : {
                        'firstname': 'Johnny',
                        'lastname': 'Hallyday',
                    },
                    'albums': [
                        {
                            'year': 1961,
                            'name': 'Salut les copains'
                        },
                        {
                            'year': 1961,
                            'name': 'Nous les gars, nous les filles'
                        },
                        {
                            'year': 1962,
                            'name': 'Sings Americas Rockin Hits'
                        }
                    ]
                }
            ]
        }

        # We want to check if the last artist has at one album
        _output = PyDictChecker.check(music_library, {
            config.__key_path__: 'artists->:last:->albums->:first:'
        })

        self.assertTrue(_output[config.__default_result_is_valid__])
        self.assertIsNotNone(_output[config.__default_result_output__])

        # If you want to check if:
        # - the first artist exists;
        # - and his real lastname is 'Smet';
        # - and his third album was published after 1960.
        _output = PyDictChecker.check(music_library, {
            config.__key_path__: 'artists->:first:',
            config.__key_conditions__: [
                {
                    config.__key_path__: 'real_name->lastname',
                    config.__key_comparator__: '==',
                    config.__key_comparative_value__: 'Smet',
                    config.__key_cast_to__: None,
                    config.__key_output__: True
                },
                {
                    config.__key_path__: 'albums->:pos:2->year',
                    config.__key_comparator__: '>',
                    config.__key_comparative_value__: 1960,
                    config.__key_cast_to__: config.__key_cast_to_int__
                }
            ]
        })

        self.assertTrue(_output[config.__default_result_is_valid__])
        self.assertEqual(_output[config.__default_result_output__], 'Smet')

        # We want to get a false validation:
        # 1. the first artist
        # 2. if his real lastname is 'Smet'
        # 3. and his LAST album was published BEFORE 1960
        _output = PyDictChecker.check(music_library, {
            config.__key_path__: 'artists->:first:',
            config.__key_conditions__: [
                {
                    config.__key_path__: 'real_name->lastname',
                    config.__key_comparator__: '==',
                    config.__key_comparative_value__: 'Smet',
                    config.__key_cast_to__: None
                },
                {
                    config.__key_path__: 'albums->:last:->year',
                    config.__key_comparator__: '<',
                    config.__key_comparative_value__: 1960,
                    config.__key_cast_to__: config.__key_cast_to_int__,
                    config.__key_output__: True
                }
            ]
        })

        self.assertFalse(_output[config.__default_result_is_valid__])
        self.assertEqual(_output[config.__default_result_output__], 1962)

if __name__ == '__main__':
    unittest.main()
