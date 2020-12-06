def foo():
    x = bar()

def bar():
    def baz():
        z = 2
        return z
    y = baz()
    return 4

foo()
