import pytest

import gdg


def test_format_generation():
    assert(gdg.Constants.format_generation() == 'g')

def test_format_epoch():
    assert(gdg.Constants.format_epoch() == 'e')




