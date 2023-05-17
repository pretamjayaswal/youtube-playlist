def smart_divide(func):
    def inner(a, b):
        if b == 0:
            print("Whoops! Division by 0")
            return None

        return func(a, b)
    return inner


@smart_divide
def divide(a, b):
    print(a/b)

divide(8, 2)




def smarty_div(func):
    def inner(x,y):
        if y==0:
            print('denom is 0 !!...aborted')
            return None
        return func(x,y)
    return inner

@smarty_div
def mydiv(x,y):
    print(x/y)

mydiv(16,0)















