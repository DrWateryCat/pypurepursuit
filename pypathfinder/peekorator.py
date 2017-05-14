class Peekorator(object):

    def __init__(self, generator):
        self.empty = False
        self.peek = None
        self.generator = generator
        try:
            self.peek = self.generator.next()
        except StopIteration:
            self.empty = True

    def __iter__(self):
        return self

    def next(self):
        """
        Return the self.peek element, or raise StopIteration
        if empty
        """
        if self.empty:
            raise StopIteration()
        to_return = self.peek
        try:
            self.peek = self.generator.next()
        except StopIteration:
            self.peek = None
            self.empty = True
        return to_return