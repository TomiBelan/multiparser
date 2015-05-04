def my_generator(should_skip_20=False):
    print("begin")
    yield 10
    if not should_skip_20:
        yield 20
    yield 30
    print("end")

my_iterator = my_generator(True)
print(next(my_iterator))
print(next(my_iterator))
print(next(my_iterator))
