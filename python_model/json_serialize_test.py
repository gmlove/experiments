import unittest
import json

from python_model.json_serialize import JsonSerializable


class A(JsonSerializable):

    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b if b is not None else B(0)

    @property
    def id(self):
        return self.a

    def _deserialize_prop(self, name, deserialized):
        if name == 'b':
            self.b = B.deserialize(deserialized)
            return
        super()._deserialize_prop(name, deserialized)


class B(JsonSerializable):

    def __init__(self, b):
        super().__init__()
        self.b = b


class SerializableModelTest(unittest.TestCase):

    def test_model_should_serialize_correctly(self):
        self.assertEqual(json.dumps({'a': 1, 'b': {'b': 2}}), A(1, B(2)).serialize())

    def test_model_should_deserialize_correctly(self):
        a = A.deserialize(json.dumps({'a': 1, 'b': {'b': 2}}))
        self.assertEqual(1, a.a)
        self.assertEqual(2, a.b.b)

    def test_model_should_deserialize_with_default_value_correctly(self):
        a = A.deserialize(json.dumps({'a': 1}))
        self.assertEqual(1, a.a)
        self.assertEqual(0, a.b.b)
