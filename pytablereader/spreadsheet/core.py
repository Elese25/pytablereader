# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

from .._constant import TableNameTemplate as tnt
from ..interface import TableLoader


class SpreadSheetLoader(TableLoader):
    """
    Abstract class of table data.
    Especially spreadsheets that consists multiple rows.

    .. py:attribute:: table_name

        Table name string. Defaults to ``%(sheet)s``.

    .. py:attribute:: start_row

        The first row to search header row.
    """

    def __init__(self, source):
        super(SpreadSheetLoader, self).__init__(source)

        self.start_row = 0
        self._worksheet = None
        self._start_col_idx = None
        self._end_col_idx = None

    @abc.abstractproperty
    def _sheet_name(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def _row_count(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def _col_count(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _is_empty_sheet(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _get_start_row_idx(self):  # pragma: no cover
        pass

    @property
    def _format_name(self):
        return "spreadsheet"

    def _make_table_name(self):
        self._validate()

        return self._replace_table_name_template(
            self._get_basic_tablename_mapping() +
            [
                (tnt.SHEET,  self._sheet_name),
            ],
        )

    def _get_default_table_name_template(self):
        return "{:s}".format(tnt.SHEET)