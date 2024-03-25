from utils.locale_svc import flatten_dict, unflatten_dict

__init_json = {
    "en": "English",
    "a": {
        "b": {"c": {"d": "qqqq", "c": "cccc", "a": "aaaa"}, "b": "bbbb"},
        "d": {"c": "qweqwe", "b": "bbbbb"},
        "c": "ffff",
        "1": "qweqwe",
        "2": {"1": '11111', "a": "aaaaa"},
        "a": [
            "aaaa",
            {
                "b": "bbbb",
                "a": "aaaa",
                "c": ["aaaa", {"b": "bbbb", "a": "aaaa"}, "bbbb"]
            },
            "bbbb"
        ]
    }
}
z = {'a':
    {
        '0': 'aaaa',
        '1': {
            'b': 'bbbb', 'a': 'aaaa', 'c': {
                '0': 'aaaa',
                '1': {'b': 'bbbb', 'a': 'aaaa'},
                '2': 'bbbb'}
        },
        '2': 'bbbb'
    }}
z_a = {"a": [
    "aaaa",
    {
        "b": "bbbb",
        "a": "aaaa",
        "c": ["aaaa", {"b": "bbbb", "a": "aaaa"}, "bbbb"]
    },
    "bbbb"
]}
_inline_init_json = {
    'en': 'English',
    'a:b:c:d': 'qqqq', 'a:b:c:c': 'cccc', 'a:b:c:a': 'aaaa', 'a:b:b': 'bbbb',
    'a:d:c': 'qweqwe', 'a:d:b': 'bbbbb',
    'a:c': 'ffff',
    "a:'1'": 'qweqwe',
    "a:'2':'1'": '11111',
    "a:'2':a": 'aaaaa',
    'a:a:0': 'aaaa',
    'a:a:1:b': 'bbbb', 'a:a:1:a': 'aaaa',
    'a:a:1:c:0': 'aaaa', 'a:a:1:c:1:b': 'bbbb', 'a:a:1:c:1:a': 'aaaa', 'a:a:1:c:2': 'bbbb',
    'a:a:2': 'bbbb',
}


# print(flatten(__init_json))
# print(unflatten(flatten(__init_json)))
# print(unflatten(flatten(__init_json)) == __init_json)
# print(transform_dict_to_dict_with_list(z) == z_a)
# print(transform_dict_to_dict_with_list(unflatten_dict(_inline_init_json)))
# print(flatten_dict(__init_json) == _inline_init_json)
# print(unflatten_dict(_inline_init_json) == __init_json)


def test_flatten_unflutten_dict_fn():
    assert flatten_dict(__init_json) == _inline_init_json


def test_unflatten_unflutten_dict_fn():
    assert unflatten_dict(_inline_init_json) == __init_json