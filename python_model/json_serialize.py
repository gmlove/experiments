import inspect
import json


def is_normal_prop(obj, key):
    is_prop = isinstance(getattr(type(obj), key, None), property)
    is_func_attr = callable(getattr(obj, key))
    is_private_attr = key.startswith('__')
    return not (is_func_attr or is_prop or is_private_attr)


def is_basic_type(value):
    return value is None or type(value) in [int, float, str, bool]


class JsonSerializable:

    def _serialize_prop(self, name):
        return getattr(self, name)

    def _as_dict(self):
        props = {}
        for key in dir(self):
            if not is_normal_prop(self, key):
                continue
            value = self._serialize_prop(key)
            if not (is_basic_type(value) or isinstance(value, JsonSerializable)):
                raise Exception('unknown value to serialize to dict: key={}, value={}'.format(key, value))
            props[key] = value if is_basic_type(value) else value._as_dict()
        return props

    def serialize(self):
        return json.dumps(self._as_dict(), ensure_ascii=False)

    def _deserialize_prop(self, name, deserialized):
        setattr(self, name, deserialized)

    @classmethod
    def deserialize(cls, json_encoded):
        if json_encoded is None:
            return None

        args = inspect.getfullargspec(cls)
        args_without_self = args.args[1:]
        obj = cls(*([None] * len(args_without_self)))

        data = json.loads(json_encoded, encoding='utf8') if type(json_encoded) is str else json_encoded
        for key in dir(obj):
            if not is_normal_prop(obj, key):
                continue
            if key in data:
                obj._deserialize_prop(key, data[key])
        return obj
