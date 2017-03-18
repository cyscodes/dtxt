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

import sys
import dtxt_proto2
import dtxt_argument
import dtxt_util


class Table:
    COLUMN_NAME_ROW = 0

    def __init__(self, excel_sheet):
        self.excel_sheet = excel_sheet
        self.row_count = self.excel_sheet.get_row_count()
        self.column_index = {}
        self.__init_column_index()

    def get_data_rows(self):
        if self.row_count <= 1:
            return []
        return range(1, self.row_count)

    def get_data_text(self, data_row, column_name):
        if not self.__is_data_row_valid(data_row) or not self.__is_column_name_valid(column_name):
            return None
        return self.excel_sheet.get_cell_value(data_row, self.column_index[column_name])

    def __is_data_row_valid(self, data_row):
        return self.__class__.COLUMN_NAME_ROW < data_row < self.row_count

    def __is_column_name_valid(self, column_name):
        return column_name in self.column_index

    def __init_column_index(self):
        if self.row_count < 1:
            return
        column_names = self.excel_sheet.get_row_values(self.__class__.COLUMN_NAME_ROW)
        for index in range(0, len(column_names)):
            self.column_index[column_names[index]] = index


class Schema:
    def __init__(self, schema_table):
        self.records = None
        self.__init_records(schema_table)

    def __init_records(self, schema_table):
        self.records = []
        for data_row in schema_table.get_data_rows():
            record = SchemaRecord(
                schema_table.get_data_text(data_row, "column_name"),
                schema_table.get_data_text(data_row, "proto_field_name"),
                schema_table.get_data_text(data_row, "proto_field_type"))
            self.records.append(record)


class SchemaRecord:
    def __init__(self, column_name=None, proto_field_name=None, proto_field_type=None):
        self.column_name = column_name
        self.proto_field_name = proto_field_name
        self.proto_field_type = proto_field_type


class Converter:
    def __init__(self):
        self.functions = {
            dtxt_proto2.EnumFieldType.DOUBLE: self.__to_float_value,
            dtxt_proto2.EnumFieldType.FLOAT: self.__to_float_value,
            dtxt_proto2.EnumFieldType.INT32: self.__to_int_value,
            dtxt_proto2.EnumFieldType.INT64: self.__to_long_value,
            dtxt_proto2.EnumFieldType.UINT32: self.__to_long_value,
            dtxt_proto2.EnumFieldType.UINT64: self.__to_long_value,
            dtxt_proto2.EnumFieldType.SINT32: self.__to_int_value,
            dtxt_proto2.EnumFieldType.SINT64: self.__to_long_value,
            dtxt_proto2.EnumFieldType.FIXED32: self.__to_int_value,
            dtxt_proto2.EnumFieldType.FIXED64: self.__to_long_value,
            dtxt_proto2.EnumFieldType.SFIXED32: self.__to_int_value,
            dtxt_proto2.EnumFieldType.SFIXED64: self.__to_long_value,
            dtxt_proto2.EnumFieldType.BOOL: self.__to_bool_value,
            dtxt_proto2.EnumFieldType.STRING: self.__to_str_value,
            dtxt_proto2.EnumFieldType.BYTES: self.__to_bytes_value
        }

    def to_value(self, field_type, cell_text):
        if field_type not in self.functions:
            print "Invalid field type: %s for cell text: %s" % (field_type, cell_text)
            return None
        return self.functions[field_type](cell_text)

    @staticmethod
    def __to_float_value(text):
        if len(str(text).strip()) <= 0:
            return None
        return float(text)

    @staticmethod
    def __to_int_value(text):
        if len(str(text).strip()) <= 0:
            return None
        return int(text)

    @staticmethod
    def __to_long_value(text):
        if len(str(text).strip()) <= 0:
            return None
        return long(text)

    @staticmethod
    def __to_bool_value(text):
        if len(str(text).strip()) <= 0:
            return None
        return bool(text)

    @staticmethod
    def __to_str_value(text):
        return unicode(text)

    @staticmethod
    def __to_bytes_value(text):
        return unicode(text).encode("utf-8")


class Parser:
    def __init__(self, table_name, table, schema):
        self.table = table
        self.schema = schema
        self.module_name = dtxt_util.get_proto_module_name(table_name)
        self.data_set_message_name = dtxt_util.get_proto_data_set_message_name(table_name)
        self.data_set_message_field_name = dtxt_util.get_proto_data_set_message_field_name(table_name)
        self.data_set_message = None
        self.data_converter = Converter()

    def parse(self):
        self.__load_proto_module()
        self.__fill_data_set()

    def get_text_data(self):
        if self.data_set_message is None:
            print "Data set message in %s is none" % self.module_name
            return None
        return str(self.data_set_message)

    def get_binary_data(self):
        if self.data_set_message is None:
            print "Data set message in %s is none" % self.module_name
            return None
        return self.data_set_message.SerializeToString()

    def __load_proto_module(self):
        try:
            sys.path.append(dtxt_argument.TEMP_DIRECTORY)
            exec ("from %s import *" % self.module_name)
        except BaseException:
            print "Load module: %s failed." % self.module_name
            raise
        else:
            self.data_set_message = getattr(sys.modules[self.module_name], self.data_set_message_name)()

    def __fill_data_set(self):
        if self.data_set_message is None:
            print "No data set message: %s" % self.data_set_message_name
            return
        data_set_message_field = self.data_set_message.__getattribute__(self.data_set_message_field_name)
        for data_row in self.table.get_data_rows():
            message = data_set_message_field.add()
            self.__fill_data(message, data_row)

    def __fill_data(self, message, data_row):
        for record in self.schema.records:
            cell_text = self.table.get_data_text(data_row, record.column_name)
            field_value = self.data_converter.to_value(record.proto_field_type, cell_text)
            message.__setattr__(record.proto_field_name, field_value)
