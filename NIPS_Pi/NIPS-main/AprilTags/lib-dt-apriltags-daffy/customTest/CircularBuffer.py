class RingBuffer:
    """ Class that implements a not-yet-full buffer. """
    def __init__(self, bufsize):
        self.bufsize = bufsize
        self.data = []

    class __Full:
        """ Class that implements a full buffer. """
        def add(self, x):
            """ Add an element overwriting the oldest one. """
            self.data[self.currpos] = x
            self.currpos = (self.currpos+1) % self.bufsize
        def get(self):
            """ Return list of elements in correct order. """
            return self.data[self.currpos:]+self.data[:self.currpos]

    def add(self,x):
        """ Add an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.bufsize:
            # Initializing current position attribute
            self.currpos = 0
            # Permanently change self's class from not-yet-full to full
            self.__class__ = self.__Full

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data