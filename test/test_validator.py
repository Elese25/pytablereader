# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

import pytablereader as ptr
from pytablereader._constant import SourceType
from pytablereader._validator import FileValidator
from pytablereader._validator import TextValidator


class Test_FileValidator_validate:

    @pytest.mark.parametrize(["value"], [
        ["test"],
    ])
    def test_normal(self, tmpdir, value):
        p_file_path = tmpdir.join(value)

        with open(str(p_file_path), "w") as _f:
            pass

        validator = FileValidator(str(p_file_path))
        assert validator.source_type == SourceType.FILE
        validator.validate()

    @pytest.mark.parametrize(["value", "expected"], [
        [None, IOError],
        ["", IOError],
    ])
    def test_exception_null(self, value, expected):
        validator = FileValidator(value)

        with pytest.raises(expected):
            validator.validate()

    @pytest.mark.parametrize(["value", "expected"], [
        ["te\0st", ptr.InvalidFilePathError]
    ])
    def test_exception_invalid_path(self, tmpdir, value, expected):
        validator = FileValidator(value)

        with pytest.raises(expected):
            validator.validate()


class Test_TextValidator_validate:

    @pytest.mark.parametrize(["value"], [
        ["test"],
    ])
    def test_normal(self, value):
        validator = TextValidator(value)
        assert validator.source_type == SourceType.TEXT
        validator.validate()

    @pytest.mark.parametrize(["value", "expected"], [
        [None, ptr.EmptyDataError],
        ["", ptr.EmptyDataError],
    ])
    def test_exception(self, value, expected):
        validator = TextValidator(value)

        with pytest.raises(expected):
            validator.validate()