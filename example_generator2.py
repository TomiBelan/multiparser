class MyGenerator:
    def __init__(self, should_skip_20=False):
        self.should_skip_20 = should_skip_20
        self.last_result = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.last_result == None:
            print("begin")
            self.last_result = 10
            return 10
        if self.last_result == 10 and not self.should_skip_20:
            self.last_result = 20
            return 20
        if self.last_result == 10 or self.last_result == 20:
            self.last_result = 30
            return 30
        if self.last_result == 30:
            print("end")
            raise StopIteration()

my_iterator = MyGenerator(True)
print(next(my_iterator))
print(next(my_iterator))
print(next(my_iterator))
