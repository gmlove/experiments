import json
import re


class ModelBase:

    @staticmethod
    def is_normal_prop(obj, key):
        is_prop = isinstance(getattr(type(obj), key, None), property)
        is_constant = re.match('^[A-Z_0-9]+$', key)
        return not (key.startswith('__') or callable(getattr(obj, key)) or is_prop or is_constant)

    @staticmethod
    def is_basic_type(value):
        return value is None or type(value) in [int, float, str, list, tuple, bool, dict]

    def _serialize_prop(self, name):
        value = getattr(self, name)
        if isinstance(value, (tuple, list)):
            try:
                json.dumps(value)
                return value
            except Exception:
                return [v._as_dict() for v in value]
        return value

    def _as_dict(self):
        keys = dir(self)
        props = {}
        for key in keys:
            if not ModelBase.is_normal_prop(self, key):
                continue
            value = self._serialize_prop(key)
            if not (ModelBase.is_basic_type(value) or isinstance(value, ModelBase)):
                raise Exception('unkown value to serialize to dict: key={}, value={}'.format(key, value))
            props[key] = value if self.is_basic_type(value) else value._as_dict()
        return props

    def _short_prop(self, name):
        value = getattr(self, name)
        if isinstance(value, (tuple, list)):
            try:
                json.dumps(value)
                return value
            except Exception:
                return [v._as_short_dict() for v in value]
        return value

    def _as_short_dict(self):
        keys = dir(self)
        props = {}
        for key in keys:
            if not ModelBase.is_normal_prop(self, key):
                continue
            value = self._short_prop(key)
            if not (ModelBase.is_basic_type(value) or isinstance(value, ModelBase)):
                raise Exception('unkown value to serialize to short dict: key={}, value={}'.format(key, value))
            props[key] = value if self.is_basic_type(value) else value._as_short_dict()
        return props

    def serialize(self):
        return json.dumps(self._as_dict(), ensure_ascii=False)

    def _deserialize_prop(self, name, deserialized):
        setattr(self, name, deserialized)

    @classmethod
    def deserialize(cls, json_encoded):
        if json_encoded is None:
            return None

        import inspect
        args = inspect.getfullargspec(cls)
        args_without_self = args.args[1:]
        obj = cls(*([None] * len(args_without_self)))

        data = json.loads(json_encoded, encoding='utf8') if type(json_encoded) is str else json_encoded
        keys = dir(obj)
        for key in keys:
            if not ModelBase.is_normal_prop(obj, key):
                continue
            if key in data:
                obj._deserialize_prop(key, data[key])
        return obj

    def __str__(self):
        return self.serialize()

    def _prop_eq(self, name, value, value_other):
        return value == value_other

    def __eq__(self, other):
        if other is None or other.__class__ is not self.__class__:
            return False

        keys = dir(self)
        for key in keys:
            if not ModelBase.is_normal_prop(self, key):
                continue
            value, value_other = getattr(self, key), getattr(other, key)
            if not (ModelBase.is_basic_type(value) or isinstance(value, ModelBase)):
                raise Exception('unsupported value to compare: key={}, value={}'.format(key, value))
            if value is None and value_other is None:
                continue
            if (value is None and value_other is not None) or (value is not None and value_other is None):
                return False
            if not self._prop_eq(key, value, value_other):
                return False

        return True

    def short_repr(self):
        return json.dumps(self._as_short_dict(), ensure_ascii=False)
