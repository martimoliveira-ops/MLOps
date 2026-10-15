def make_bold(function):
    def wrapped(*args, **kwargs):
        return "<b>" + function(*args, **kwargs) + "</b>"

    return wrapped


def make_italic(function):
    def wrapped(*args, **kwargs):
        return "<i>" + function(*args, **kwargs) + "</i>"

    return wrapped


def make_underline(function):
    def wrapped(*args, **kwargs):
        return "<u>" + function(*args, **kwargs) + "</u>"

    return wrapped


@make_bold
@make_italic
@make_underline
def hello():
    return "Hello everyone"


@make_bold
@make_italic
@make_underline
def format_text(text):
    return text


if __name__ == "__main__":
    print(hello())
