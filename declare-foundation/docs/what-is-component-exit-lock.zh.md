关联: `declare_foundation.components.base_component.ComponentExitLock`

> 注: 以下用 "~" 代指 `declare_foundation.components.base_component`.

# 作用机制

`~.BaseComponent` 在调用 `__enter__` 时, 会获取一个 "退出锁":

```python
class BaseComponent:
    def __enter__(self):
        global _com_exit_lock
        # 获取一个 "退出锁"
        self._exit_lock = _com_exit_lock.fetch_lock()  # type: int[0, 1]
        ...
```

该锁是一个大于等于 0 的整数. 通常来说, 它的值只有两种情况: 0 或者 1.

当退出锁的值是 0 时, `BaseComponent` 调用 `__exit__` 时可以正常退出; 当值为 1 时, 第一次调用 `__exit__` 时会被阻止正常退出, 此时退出锁 -= 1 (值变成 0); 第二次调用 `__exit__` 时才可以正常退出.

为什么要阻止一次正常退出呢? 目的就是 "延缓" 正常退出机制的发生.

如下示例:

```python
def some_view():
    with Text() as txt:
        return txt  # A

with WebPage() as page:
    with Build(some_view) as view:
    #    ^^^^^^^^^^^^^^^^ C
        pass
        with Div() as div:
            pass  # B
```

当运行到 A 位置时, 对象 `txt` 会退出. 但我们希望的是, 在执行到 B 位置之后, `txt` 才退出.

为了阻止 `txt` 在 A 位置就退出, 那么就试图让 `txt` 在 A 位置退出时阻止它的正常退出机制. 因此, `Build.__enter__` (位置 C) 就是做了这件事:

1. 在 `txt.__enter__` 之前, 告诉 `ComponentExitLock` 要给 `txt` 加一个值为 1 的退出锁
2. 在 `txt.__enter__` 时, `txt` 获取了这个锁
3. 在 `txt` 执行到 A, `txt` 想要退出 (第一次调用 `__exit__`), 由于 `txt` 的退出锁的存在, 导致 `txt` 没有完成正常退出操作. 此时 `declare_foundation.context_manager.context.Context:this` 指针仍然留在 `txt` (也就是说 with 的上下文环境仍然处于 `txt` 范围)
4. 然后, `div` 在 `txt` 的上下文环境下, 正确执行它的 `__enter__` 操作
5. `div` 在 B 位置执行完 `__exit__` 后, `Build(some_view)` 也开始触发 `Build.__exit__`, 在 `Build.__exit__` 中, `Build` 会主动再调用一次 `txt.__exit__`. 这次, `txt.__exit__` 就可以完成正常的退出操作了
