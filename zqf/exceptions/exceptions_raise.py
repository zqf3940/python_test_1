# encoding=utf-8

class ShortInputException(Exception):
    def __init__(self, length, atleast):
        Exception.__init__(self)
        self.length = length
        self.atleast = atleast

try:
    text = input('Enter something --> ')
    if len(text) < 3:
        raise ShortInputException(len(text), 3)

except EOFError:
    print('why did you do an EOF on me?')
except ShortInputException as ex:
    print(('shortinputexception: the input was {0} long, expected at least {1}').format(ex.length, ex.atleast))
else:
    print('no exception was raised.')