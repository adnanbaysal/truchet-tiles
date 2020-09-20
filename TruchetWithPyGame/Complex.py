class ComplexTypeError(TypeError):
    pass


class Complex:
    """Class of complex numbers and operations"""
    def __init__(self, re, im):
        self.re = re
        self.im = im

    @classmethod
    def check_complex_type(cls, x):
        if type(x) != cls:
            raise ComplexTypeError

    def add(self, y):
        Complex.check_complex_type(y)
        self.re += y.re
        self.im += y.im

    def subtract(self, y):
        Complex.check_complex_type(y)
        self.re -= y.re
        self.im -= y.im

    def invert(self):
        if self.re == 0 and self.im == 0:
            raise ZeroDivisionError
        d = self.re ** 2 + self.im ** 2
        self.re /= d
        self.im /= -d

    def multiply(self, y):
        Complex.check_complex_type(y)
        re = self.re * y.re - self.im * y.im
        im = self.re * y.im + self.im * y.re
        self.re = re
        self.im = im

    def divide(self, y):
        Complex.check_complex_type(y)
        yinv = Complex(y.re, y.im)
        yinv.invert()
        self.multiply(yinv)


def cmult(x, y):
    Complex.check_complex_type(x)
    Complex.check_complex_type(y)
    re = x.re * y.re - x.im * y.im
    im = x.re * y.im + x.im * y.re
    return Complex(re, im)


def cminv(x):
    Complex.check_complex_type(x)
    if x.re == 0 and x.im == 0:
        raise ZeroDivisionError
    d = x.re ** 2 + x.im ** 2
    re = x.re / d
    im = -x.im / d
    return Complex(re, im)


def cdiv(x, y):
    Complex.check_complex_type(x)
    Complex.check_complex_type(y)
    yinv = cminv(y)
    return cmult(x, yinv)


def cadd(x, y):
    Complex.check_complex_type(x)
    Complex.check_complex_type(y)
    re = x.re + y.re
    im = x.im + y.im
    return Complex(re, im)


def csubt(x, y):
    Complex.check_complex_type(x)
    Complex.check_complex_type(y)
    re = x.re - y.re
    im = x.im - y.im
    return Complex(re, im)


def csquare(x):
    Complex.check_complex_type(x)
    re = x.re ** 2 - x.im ** 2
    im = 2 * x.re * x.im
    return Complex(re, im)

def test_complex():
    """Test will be written later"""
    # x = Complex(1, 2)
    # y = csquare(x)
    # print(y.re, y.im)
    pass


if __name__ == "__main__":
    test_complex()
