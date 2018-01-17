def print_max(x, y):
    '''prints the axxiumm of two numbers. 打印两个数值中的最大数.
    The two values must be eintegers.这两个数都应该是整数'''
    x = int(x)
    y = int(y)

    if x > y:
        print(x, 'is maximum')
    else:
        print(y, 'is maximum')
    '''dddd
    '''
print_max(3, 5)
print(print_max.__doc__)