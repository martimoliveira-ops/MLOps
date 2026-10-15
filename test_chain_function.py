from chain_of_functions import (
    format_text,
    hello,
    make_bold,
    make_italic,
    make_underline,
)


def text():
    return "text"


def test_make_bold():
    assert make_bold(text)() == "<b>text</b>"


def test_make_italic():
    assert make_italic(text)() == "<i>text</i>"


def test_make_underline():
    assert make_underline(text)() == "<u>text</u>"


def test_hello_applies_decorators_bottom_up():
    assert hello() == "<b><i><u>Hello everyone</u></i></b>"


def test_format_text_passes_input_through():
    assert format_text("hi") == "<b><i><u>hi</u></i></b>"
