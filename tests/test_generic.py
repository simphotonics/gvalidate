import pytest

from gvalidate import validate


@validate(lambda x: x > 0, "length", enable_warnings=True)
def f_positive(length, width):
    pass


@validate(lambda x: x > 0, enable_warnings=True)
def f_positive_check_all(length, width):
    pass


class TestValidatePositive:
    def test_raised_exception_pos(self):
        with pytest.raises(ValueError):
            f_positive(-3, width=5)

    def test_raised_exception_keyword(self):
        with pytest.raises(ValueError):
            f_positive_check_all(3, width=-5)

    def test_raised_exception_incompatible_type(self):
        with pytest.raises(ValueError):
            f_positive("not_a_number", width="a")

    def test_message(self):
        try:
            f_positive(-3, width=5)
        except ValueError as e:
            assert (
                "Invalid argument in function "
                "f_positive: length = -3. " in str(e)
            )

    def test_all(self):
        with pytest.raises(ValueError):
            f_positive_check_all(5, width=-3)


@validate(lambda x: x > 0, 'length', enable_warnings=True)
@validate(lambda func: callable(func), 'callback', enable_warnings=True)
def g(length, callback):
    """
    Used to test nested validation decorators.
    """
    pass


class TestNestedValidation:
    def callback(self, x):
        return x

    def test_raised_exception_pos(self):
        with pytest.raises(ValueError):
            g(-3, callback=self.callback)

    def test_raised_exception_keyword(self):
        with pytest.raises(ValueError):
            g(3, callback="not a function")

    def test_raised_exception_incompatible_type(self):
        with pytest.raises(ValueError):
            g("not_a_number", callback=self.callback)

    def test_message(self):
        try:
            g(-3, callback=self.callback)
        except ValueError as e:
            assert "Invalid argument in function g: length = -3. " in str(e)


class TestValidate:
    @validate(
        validator=lambda x: False,
        argument_names = ("length", "width"),
        error_type=TypeError,
        message="__Appended to exception message__",
        enable_warnings=True,
    )
    def h(self, length, width):
        pass

    def test_raised_exception_pos(self):
        with pytest.raises(TypeError):
            self.h(3, 4)

    def test_message(self):
        try:
            self.h(3, 4)
        except TypeError as e:
            assert "__Appended to exception message__" in str(e)
