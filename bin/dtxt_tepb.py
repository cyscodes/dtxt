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

import xlrd

class Tepb:

    def __init__(self, filename):
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        self.filename = filename.decode('utf-8')
        self.book = None
        self.data = None

    def set_file_path(self, filename):
        self.filename = filename

    def file_type(self):
        lowercaseFilename = self.filename.lower()
        if lowercaseFilename.endswith('.xlsx') or lowercaseFilename.endswith('.xls'):
            return 0
        else:
            return -1

    def open_excel_file_by_sheet_index(self, index):
        if self.file_type() == 0:
            self.book = xlrd.open_workbook(self.filename, encoding_override="utf8")
            self.data = self.book.sheet_by_index(index)
            print "\nSheet #%d  %s:\t\t %d row(s)\t %d column(s)\n" % (
                index, self.data.name, self.data.nrows, self.data.ncols
            )
            return
        else:
            print "Error: Wrong file type!\n"

    def open_excel_file_by_sheet_name(self, sheetName):
        if self.file_type() == 0:
            self.book = xlrd.open_workbook(self.filename, encoding_override="utf8")
            self.data = self.book.sheet_by_name(sheetName)
            print "\nSheet #%d  %s:\t\t %d row(s)\t %d column(s)\n" % (
                self.data.number, sheetName, self.data.nrows, self.data.ncols
            )
            return
        else:
            print "Error: Wrong file type!\n"

    def get_row_values(self, row):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            #print self.data.row_values(row)
            return self.data.row_values(row)

    def get_col_values(self, col):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            #print self.data.col_values(col)
            return self.data.col_values(col)

    '''
    value   type
    0       empty
    1       string
    2       number
    3       date
    4       bool
    5       error
    '''
    def get_cell_value_type(self, row, col):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            #print self.data.cell(row, col).ctype
            return self.data.cell(row, col).ctype

    def get_cell_value(self, row, col):
        if self.data is None:
            print "Error: No sheet opened!\n"
            return
        else:
            #print self.data.cell(row, col).value
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
    def close(self):
        self.book.release_resources()
        return

    def info(self):
        print "\nExcel File:\t\t %s\n" % (self.filename)
        if self.book is None:
            print "Warning: No file opened!\n"
            return
        else:
            print "Sheet Index\t\tSheet Names"
            #print self.book.sheets()
            index = 0
            while index < len(self.book.sheets()):
                print "\t%d\t\t\t%s" % (index, self.book.sheets()[index].name)
                index += 1
        return