# PyDictChecker

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

If you want to verify if the last artist has at least one album:

```
from pydictchecker.py_dict_checker import PyDictChecker

PyDictChecker.check(music_library, [
    {
        'path': 'artists->:last:->albums->:first:',
        'conditions': []
    }
])
```

### Ex. 2

If you want to check if: 
- the first artist exists;
- and his real lastname is 'Smet';
- and his third album was published after 1961.

You can run the next method: 

```
from pydictchecker.py_dict_checker import PyDictChecker

PyDictChecker.check(music_library, [
            {
                'path': 'artists->:first:',
                'conditions': [
                    {
                        'path': 'real_name->lastname',
                        'comparator': '==',
                        'comparative_value': 'Smet',
                        'cast_to': None
                    },
                    {
                        'path': 'albums->:pos:2->year',
                        'comparator': '>',
                        'comparative_value': 1960,
                        'cast_to': ':int:'
                    }
                ]
            }
        ])
```

_NB: please note that we use relative path in this case._

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

## Credits

Developed by Alexandre Veremme @ [The POC Agency](https://www.the-poc-agency.com) (cf. [www.the-poc-agency.com](https://www.the-poc-agency.com))