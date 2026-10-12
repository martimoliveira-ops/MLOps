def make_bold(function):
    def wrapped():
        return "<b>" + function() + "<b>"

    return wrapped


def make_italic(function):
    def wrapped():
        return "<i>" + function() + "</i>"

    return wrapped


def make_underline(function):
    def wrapped():
        return "<u>" + function() + "</u>"

    return wrapped


@make_bold
@make_italic
@make_underline
def hello():
    return "Hello everyone"


print(hello())
