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

class CellType:
    Empty = 0

    String = 1

    Number = 2

    Date = 3

    Bool = 4

    Error = 5


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

        :param column_name: (unicode)
            Column name of the cell.

        :return:
            Data text of the cell.
        """
        return None


#
# Factory methods for instantiating Table.
#

def create_table_by_excel_sheet(filename, sheet_name):
    from dtxt_table_impl import ExcelTable
    return ExcelTable(filename, sheet_name)
