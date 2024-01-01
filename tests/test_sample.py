# tests/test_hello_world.py
from pytemplate.main import say_hello


def test_say_hello():
    result = say_hello()
    assert result == "Hello, World!"
