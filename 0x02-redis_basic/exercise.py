#!/usr/bin/env python3
"""
module that writes string to Redis
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ decorator that counts instances cache is called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ the wrapper functions """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ stores history of inputs and outputs """
    input_list = method.__qualname__ + ":inputs"
    output_list = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """ wrapper function for call_history method """
        self._redis.rpush(input_list, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """ replays the history of a function """
    cache = redis.Redis()
    name = method.__qualname__
    calls = cache.get(name).decode("utf-8")
    print(f"{name} was called {calls} times:")
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, out in zip(inputs, outputs):
        print("{}(*{}) -> {}"
              .format(name, i.decode('utf-8'), out.decode('utf-8')))


class Cache:
    """ class that store instance of redis client """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ converts data back to the desired format """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, data: str) -> str:
        """ get string """
        return self.get(key, str)

    def get_int(self, data: str) -> int:
        """ return an int """
        return self.get(key, int)
