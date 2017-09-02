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

import dtxt_table_impl


class Table:
    """
    Abstract Data structure for config tables.

    In our tool, config table is composed of title row and data rows.
    """

    def __init__(self):
        pass

    def dispose(self):
        """
        Free resources.
        """
        pass

    def get_data_rows(self):
        """
        Get available row number of data rows.

        :return: (list of int)
            List of row numbers.
        """
        return []

    def get_data_text(self, row_number, column_name):
        """
        Get data text of specified row and column

        :param row_number: (int)
            Row number of the cell.

        :param column_name: (str)
            Column name of the cell.

        :return:
            Data text of the cell.
        """
        return None


#
# Implementations for Table.
#


class ExcelTable(Table):
    """
    Config table written in excel sheets.
    """

    __COLUMN_NAME_ROW = 0  # Row number of column name in excel sheet.

    __DATA_ROW_START = 1  # Row number of the first data row in excel sheet.

    def __init__(self, excel_sheet):
        Table.__init__(self)
        self.__excel_sheet = excel_sheet
        self.__row_count = self.__excel_sheet.get_row_count()  # Total row count of excel sheet.
        self.__column_indexes = {}  # Dict of str, int pair. Key is column name, and value is column index.
        self.__init_column_indexes()

    def dispose(self):
        self.__excel_sheet.close()

    def get_data_rows(self):
        # No data rows.
        if self.__row_count <= self.__DATA_ROW_START:
            return []

        return range(self.__DATA_ROW_START, self.__row_count)

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
        return self.__class__.__COLUMN_NAME_ROW < data_row < self.__row_count

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
        # No column name row.
        if self.__row_count < self.__DATA_ROW_START:
            return

        column_names = self.__excel_sheet.get_row_values(self.__class__.__COLUMN_NAME_ROW)
        for index, column_name in enumerate(column_names):
            self.__column_indexes[column_name] = index


#
# Factory methods for instantiating Table.
#


def create_table_by_excel_sheet(filename, sheet_name):
    excel_sheet = dtxt_table_impl.Tepb(filename)
    excel_sheet.open_excel_file_by_sheet_name(sheet_name)
    return ExcelTable(excel_sheet)
