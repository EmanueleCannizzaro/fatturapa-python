
import os
import pytest

from fattura.fattura import Fattura

testdata = [
    'IT01234567890_FPR01.xml',
    'IT01234567890_FPR02.xml',
    'IT01234567890_FPR03.xml',
    'IT01234567890_FPA01.xml',
    'IT01234567890_FPA02.xml',
    'IT01234567890_FPA03.xml',
]

@pytest.mark.parametrize("basename", testdata)
def test_examples(basename):
    fattura = Fattura()
    filename = os.path.join('../data', basename)
    fattura.validate(filename)