# coding=utf-8

# Copyright (C) 2017 Daryl Caster, Tyler Murphy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import xlrd
from dtxt_table import Table
from dtxt_settings import ExcelSettings


class Excel:
    """
    Class for operating excel files (include .xls and .xlsx format files).
    """

    def __init__(self, filename, sheet_name):
        """
        Initialize.

        :param filename: (str(utf-8 format) or unicode)
            Filename of the excel file, including directory.
        """
        self.__filename = filename
        self.__sheet_name = sheet_name
        self.book = None
        self.data = None

    def open(self):
        if not self.__is_file_type_valid():
            raise ValueError("Invalid filename", self.__filename)
        self.book = xlrd.open_workbook(self.__filename, encoding_override=u'utf-8')
        self.data = self.book.sheet_by_name(self.__sheet_name)
        if self.book is None:
            raise ValueError("Invalid sheet name", self.__sheet_name)
        return

    def close(self):
        self.book.release_resources()
        return

    def get_row_count(self):
        if self.data is not None:
            return self.data.nrows

    def get_row_values(self, row):
        if self.data is not None:
            return self.data.row_values(row)

    def get_column_values(self, col):
        if self.data is not None:
            return self.data.col_values(col)

    def get_cell_type(self, row, col):
        """
        Get cell value type

        :param row: (int)
            Row number.

        :param col: (int)
            Column number.

        :return: (int)
            Cell type, see following list:
            value   type
            0       empty
            1       string
            2       number
            3       date
            4       bool
            5       error
        """
        if self.data is not None:
            return self.data.cell(row, col).ctype

    def get_cell_value(self, row, col):
        if self.data is not None:
            return self.data.cell(row, col).value

    def __is_file_type_valid(self):
        lowercaseFilename = self.__filename.lower()
        return lowercaseFilename.endswith('.xlsx') or lowercaseFilename.endswith('.xls')


class ExcelTable(Table):
    """
    Config table written in excel sheets.
    """

    def __init__(self, filename, sheet_name):
        Table.__init__(self)
        excel_sheet = Excel(filename, sheet_name)
        excel_sheet.open()
        self.__excel_sheet = excel_sheet
        self.__row_count = self.__excel_sheet.get_row_count()  # Total row count of excel sheet.
        self.__column_indexes = {}  # Dict of unicode, int pair. Key is column name, and value is column index.
        self.__init_column_indexes()

    def dispose(self):
        self.__excel_sheet.close()

    def get_data_rows(self):
        # No data rows.
        if self.__row_count <= ExcelSettings.DataRowStart:
            return []

        return range(ExcelSettings.DataRowStart, self.__row_count)

    def get_data_text(self, row_number, column_name):
        # No specified cell.
        if not self.__is_data_row_valid(row_number) or not self.__is_column_name_valid(column_name):
            return None

        return self.__excel_sheet.get_cell_value(row_number, self.__column_indexes[column_name])

    def __is_data_row_valid(self, data_row):
        """
        Is data row within valid range.

        :param data_row: (int)
            Data row number.

        :return: (bool)
           True if data row is within row count and not column name row, False otherwise.
        """
        return ExcelSettings.ColumnNameRow < data_row < self.__row_count

    def __is_column_name_valid(self, column_name):
        """
        Is column name defined.

        :param column_name: (str)
            Column name.

        :return: (bool)
            True if column name is defined, False otherwise.
        """
        return column_name in self.__column_indexes

    def __init_column_indexes(self):
        """
        Initialize dict of column name, column index pair.
        """
        column_names = self.__excel_sheet.get_row_values(ExcelSettings.ColumnNameRow)
        for index, column_name in enumerate(column_names):
            self.__column_indexes[column_name] = index