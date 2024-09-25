from asyncio import gather, ensure_future, get_event_loop, iscoroutine, iscoroutinefunction
from collections import namedtuple
from collections.abc import Iterable
from functools import partial
from typing import List
Loader = namedtuple('Loader', 'key,future')


class DataLoader(object):
    batch = True
    max_batch_size = None
    cache = True

    def __init__(self, batch_load_fn=None, batch=None, max_batch_size=None,
        cache=None, get_cache_key=None, cache_map=None, loop=None):
        self._loop = loop
        if batch_load_fn is not None:
            self.batch_load_fn = batch_load_fn
        assert iscoroutinefunctionorpartial(self.batch_load_fn
            ), 'batch_load_fn must be coroutine. Received: {}'.format(self.
            batch_load_fn)
        if not callable(self.batch_load_fn):
            raise TypeError(
                'DataLoader must be have a batch_load_fn which accepts Iterable<key> and returns Future<Iterable<value>>, but got: {}.'
                .format(batch_load_fn))
        if batch is not None:
            self.batch = batch
        if max_batch_size is not None:
            self.max_batch_size = max_batch_size
        if cache is not None:
            self.cache = cache
        self.get_cache_key = get_cache_key or (lambda x: x)
        self._cache = cache_map if cache_map is not None else {}
        self._queue = []

    def _schedule_dispatch(self):
        if not self._queue:
            return
        if not hasattr(self, '_dispatch_task') or self._dispatch_task.done():
            loop = self._loop or get_event_loop()
            self._dispatch_task = loop.call_soon(dispatch_queue, self)

    def _dispatch_single(self, key, future):
        try:
            result = self.batch_load_fn([key])
            if iscoroutine(result):
                future.add_done_callback(
                    partial(self._handle_future_result, key=key)
                )
                ensure_future(result).add_done_callback(
                    partial(self._handle_batch_result, future=future)
                )
            else:
                self._handle_batch_result(result, future)
        except Exception as exc:
            future.set_exception(exc)

    def _handle_future_result(self, _, key):
        if not self.cache:
            return
        cache_key = self.get_cache_key(key)
        if cache_key in self._cache:
            del self._cache[cache_key]

    def _handle_batch_result(self, batch_future, future):
        try:
            results = batch_future.result() if hasattr(batch_future, 'result') else batch_future
            if len(results) != 1:
                raise ValueError(
                    f"DataLoader must be constructed with a function which accepts "
                    f"Iterable<key> and returns Future<Iterable<value>>, but the function did "
                    f"not return a list of the same length as the keys."
                    f"\nResults:\n{results}"
                )
            future.set_result(results[0])
        except Exception as exc:
            future.set_exception(exc)

def iscoroutinefunctionorpartial(obj):
    while isinstance(obj, partial):
        obj = obj.func
    return iscoroutinefunction(obj)

    def load(self, key=None):
        """
        Loads a key, returning a `Future` for the value represented by that key.
        """
        if key is None:
            raise ValueError("The load method must be called with a key, but got None.")

        cache_key = self.get_cache_key(key)

        if self.cache and cache_key in self._cache:
            return self._cache[cache_key]

        future = self._loop.create_future() if self._loop else get_event_loop().create_future()
        self._queue.append(Loader(key=key, future=future))

        if self.batch:
            self._schedule_dispatch()
        else:
            self._dispatch_single(key, future)

        if self.cache:
            self._cache[cache_key] = future

        return future

    def load_many(self, keys):
        """
        Loads multiple keys, returning a list of values

        >>> a, b = await my_loader.load_many([ 'a', 'b' ])

        This is equivalent to the more verbose:

        >>> a, b = await gather(
        >>>    my_loader.load('a'),
        >>>    my_loader.load('b')
        >>> )
        """
        if not isinstance(keys, Iterable):
            raise TypeError(f"The loader.load_many() method must be called with Iterable<key> but got: {keys}")

        return gather(*[self.load(key) for key in keys])

    def clear(self, key):
        """
        Clears the value at `key` from the cache, if it exists. Returns itself for
        method chaining.
        """
        cache_key = self.get_cache_key(key)
        if cache_key in self._cache:
            del self._cache[cache_key]
        return self

    def clear_all(self):
        """
        Clears the entire cache. To be used when some event results in unknown
        invalidations across this particular `DataLoader`. Returns itself for
        method chaining.
        """
        self._cache.clear()
        return self

    def prime(self, key, value):
        """
        Adds the provided key and value to the cache. If the key already exists, no
        change is made. Returns itself for method chaining.
        """
        cache_key = self.get_cache_key(key)
        if cache_key not in self._cache:
            future = self._loop.create_future() if self._loop else get_event_loop().create_future()
            future.set_result(value)
            self._cache[cache_key] = future
        return self


def dispatch_queue(loader):
    """
    Given the current state of a Loader instance, perform a batch load
    from its current queue.
    """
    queue = loader._queue
    loader._queue = []

    max_batch_size = loader.max_batch_size

    if max_batch_size and max_batch_size < len(queue):
        chunks = [queue[i:i + max_batch_size] for i in range(0, len(queue), max_batch_size)]
    else:
        chunks = [queue]

    for chunk in chunks:
        keys = [loader.key for loader in chunk]
        futures = [loader.future for loader in chunk]

        batch_future = ensure_future(loader.batch_load_fn(keys))
        batch_future.add_done_callback(
            partial(_batch_load_fn_callback, loader=loader, keys=keys, futures=futures)
        )

def _batch_load_fn_callback(batch_future, loader, keys, futures):
    try:
        results = batch_future.result()
        if len(results) != len(keys):
            raise ValueError(
                f"DataLoader must be constructed with a function which accepts "
                f"Iterable<key> and returns Future<Iterable<value>>, but the function did "
                f"not return a list of the same length as the keys."
                f"\nKeys:\n{keys}"
                f"\nResults:\n{results}"
            )

        for future, result in zip(futures, results):
            if not future.done():
                future.set_result(result)
    except Exception as error:
        failed_dispatch(loader, keys, error)


def failed_dispatch(loader, keys, error):
    """
    Do not cache individual loads if the entire batch dispatch fails,
    but still reject each request so they do not hang.
    """
    for key in keys:
        cache_key = loader.get_cache_key(key)
        if cache_key in loader._cache:
            del loader._cache[cache_key]

        for loader_item in loader._queue:
            if loader_item.key == key:
                if not loader_item.future.done():
                    loader_item.future.set_exception(error)
