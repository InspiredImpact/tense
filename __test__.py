from contextlib import AbstractContextManager


class A:
    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...


print(issubclass(A, AbstractContextManager))