# PyDictChecker

## Table of content

1. [ What is PyDictChecker? ](#what-is-pydictchecker)
1. [ Examples ](#examples)
1. [ Default comparators / cast-operators ](#default-comparators--cast-operators)
1. [ Main commands ](#main-commands)
    1. [ Test ](#test)
    1. [ Build ](#build)
    1. [ Import PyDictChecker into your project ](#import-pydictchecker-into-your-project)
1. [ Credits ](#credits)

## What is PyDictChecker?

PyDictChecker is a generic Python3 tool to run recursively through a dictionary and validate any kind of conditions in a given dictionary.

It is designed as a ''_dictionary parser_'' to verify element existence & value.

You can use ''_human-readable_'' rule to move on a _node_ and check recursively and relatively any conditions (and sub-conditions).

## Examples

Let's say you have the dictionary below:   

```
music_library = {
    'artists': [
        {
            'id': 1,
            'real_name': {
                'firstname': 'Jean - Philippe Léo',
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
```

### Ex. 1

If you want to check if the last artist has at least one album:

```
output = PyDictChecker.check(music_library, {
    'path': 'artists->:last:->albums->:first:'
})
```

NB: 
- output['\_is\_valid'] is valid in this case because the node exists
- output['result'] is the first album in this case  

### Ex. 2

If you want to check if: 
- the first artist exists;
- and his real lastname is 'Smet';
- and his third album was published after 1961.

You can run the next method: 

```
output = PyDictChecker.check(music_library, {
    'path': 'artists->:first:',
    'conditions': [
        {
            'path': 'real_name->lastname',
            'comparator': '==',
            'comparative_value': 'Smet',
            'cast_to': None,
            'output': True
        },
        {
            'path': 'albums->:pos:2->year',
            'comparator': '>',
            'comparative_value': 1960,
            'cast_to': ':int:'
        }
    ]
})
```

NB: 
- please note that we use relative path in this case.
- the boolean output['\_is\_valid'] is True and we get the value 'Smet' in output['result']

### More

See / run this test file [ py_dict_checker_test.py ](https://github.com/thepocagency/pydictchecker/blob/master/test/py_dict_checker_test.py) for more details.

## Default comparators / cast-operators

So far, there are only these next comparators: ```'>'```, ```'<'```, ```'>='```, ```'<='```, ```'=='```, ```'!='```.

And these are the first operators:
 
 - to cast a string to an integer, with ```:int:```
 - to move into a dict: 
    - ```:first:```, 
    - ```:last:```, 
    - ```:pos:X``` (where X is the position of the element you want to move to)    

## Main commands

### Test

```
 $ python -m unittest discover -v -s . -p "*_test.py"
```

### Build

To create a build version in the "_dist_" directory

```
 $ python setup.py sdist
```

### Import PyDictChecker into your project

This project is not listed on Pypi but you can import it from Github:

```
 $ . venv/bin/activate
 $ pip install -e git+https://github.com/thepocagency/pydictchecker.git#egg=pydictchecker
 $ pip freeze > requirements.txt
```

## Credits

Developed by Alexandre Veremme @ [The POC Agency](https://www.the-poc-agency.com) (cf. [www.the-poc-agency.com](https://www.the-poc-agency.com))