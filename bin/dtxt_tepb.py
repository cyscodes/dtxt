# coding=utf8

# Copyright (C) 2017 Cao Yang, Teng Teng
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

import xlrd


class Tepb:
    def __init__(self, filename, sheet_name):
        # TODO: process the difference of string and unicode
        self.filename = filename
        self.sheet_name = sheet_name
        self.sheetNumber = None
        self.book = None
        self.data = None

    def set_file_path(self, filename):
        self.filename = filename

    #    def set_sheet_by_index(self, index):
    #        self.sheetNumber = index

    def file_type(self):
        lowercaseFilename = self.filename.lower()
        if lowercaseFilename.endswith('.xlsx') or lowercaseFilename.endswith('.xls'):
            return 0
        else:
            return -1

    def open_excel_file(self):
        if self.file_type() == 0:
            self.book = xlrd.open_workbook(self.filename, encoding_override="utf8")
            self.sheetNumber = None
            if self.sheet_name is not None:
                self.sheetNumber = self.__get_sheet_index(self.sheet_name)
                self.data = self.book.sheet_by_index(self.sheetNumber)
                print("\nSheet #{:d}:\t\t {:d} row(s)\t {:d} column(s)\n".format(
                    self.sheetNumber,
                    self.data.nrows,
                    self.data.ncols
                ))
            else:
                print("Error: Wrong sheet name!\n")
        else:
            print("Error: Wrong file type!\n")

    def get_row_values(self, row):
        if self.data is None:
            print("Error: No sheet opened!\n")
            return
        else:
            # print self.data.row_values(row)
            return self.data.row_values(row)

    def get_col_values(self, col):
        if self.data is None:
            print("Error: No sheet opened!\n")
            return
        else:
            # print self.data.col_values(col)
            return self.data.col_values(col)

    def get_cell_value_type(self, row, col):
        """
        :return:
        value   type
        0       empty
        1       string
        2       number
        3       date
        4       bool
        5       error
        """
        if self.data is None:
            print("Error: No sheet opened!\n")
            return
        else:
            # print self.data.cell(row, col).ctype
            return self.data.cell(row, col).ctype

    def get_cell_value(self, row, col):
        if self.data is None:
            print("Error: No sheet opened!\n")
            return
        else:
            # print self.data.cell(row, col).value
            return self.data.cell(row, col).value

    # TODO: Debug set_cell_value function.
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
        print("\nExcel File:\t\t {}\nSheet Number:\t {:d}".format(
            self.filename,
            self.sheetNumber
        ))
        if self.book is None:
            print("Warning: No file opened!\n")
            return
        else:
            print("Sheet Index\t\tSheet Names")
            # print self.book.sheets()
            index = 0
            while index < len(self.book.sheets()):
                print "\t%d\t\t\t%s" % (index, self.book.sheets()[index].name)
                index += 1
        return

    def get_row_count(self):
        if self.data is None:
            return 0
        return self.data.nrows

    def __get_sheet_index(self, sheet_name):
        for index in range(0, len(self.book.sheets())):
            if sheet_name == self.book.sheets()[index].name:
                return index
        return -1
