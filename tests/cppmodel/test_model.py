from util import get_tu
import ffig.cppmodel
from ffig.clang.cindex import TypeKind
from nose.tools import assert_equals
from nose.tools import raises


def test_repr():
    source = 'class A{}; void foo();'
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)

    assert_equals(
        str(model),
        "<cppmodel.Model filename=t.cpp, classes=['A'], functions=['foo']>")


@raises(Exception)
def test_broken_code():
    source = 'class A{}'

    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
