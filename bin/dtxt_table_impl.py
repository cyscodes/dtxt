# coding=utf8

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


class Tepb:
    """
    Class for operating excel files (include .xls and .xlsx format files).
    """

    def __init__(self, filename):
        """
        Initialize.

        :param filename: (str(utf-8 format) or unicode)
            Filename of the excel file, including directory.
        """
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        self.filename = filename.decode('utf-8')
        self.book = None
        self.data = None

    def open_excel_file_by_sheet_index(self, index):
        if not self.__is_file_type_valid():
            print("Error: Wrong file type!\n")
            return
        self.book = xlrd.open_workbook(self.filename, encoding_override="utf8")
        self.data = self.book.sheet_by_index(index)
        return

    def open_excel_file_by_sheet_name(self, sheet_name):
        if not self.__is_file_type_valid():
            print("Error: Wrong file type!\n")
            return
        self.book = xlrd.open_workbook(self.filename, encoding_override="utf8")
        self.data = self.book.sheet_by_name(sheet_name)
        return

    def close(self):
        self.book.release_resources()
        return

    def get_row_count(self):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            return self.data.nrows

    def get_row_values(self, row):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            return self.data.row_values(row)

    def get_col_values(self, col):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            return self.data.col_values(col)

    def get_cell_value_type(self, row, col):
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
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            return self.data.cell(row, col).ctype

    def get_cell_value(self, row, col):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            return self.data.cell(row, col).value

    ''' Write File ---- Save for later
    def set_cell_value(self, row, col, value, ctype = 1, xf = 0):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            self.data.put_cell(row, col, ctype, value, xf)
            return
    '''

    def info(self):
        print "\nExcel File:\t\t %s\n" % (self.filename)
        if self.book is None:
            print "Warning: No file opened!\n"
            return
        else:
            print "Sheet Index\t\tSheet Names"
            for index in range(0, self.book.nsheets):
                print "\t%d\t\t\t%s" % (index, self.book.sheets()[index].name)
        return

    def __is_file_type_valid(self):
        lowercaseFilename = self.filename.lower()
        return lowercaseFilename.endswith('.xlsx') or lowercaseFilename.endswith('.xls')
