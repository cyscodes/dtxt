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

import dtxt_argument
import dtxt_proto2
import dtxt_util


class Converter:
    """
    Utility class for converting str to specified data type
    """

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

    def to_value(self, field_type, text):
        """
        Convert text to data type according to proto message field type

        :param field_type: (str)
            Proto message field type. See EnumFieldType in dtxt_proto2.

        :param text: (str)
            Text data.

        :return: (*)
            Data of specified data type.
        """
        if field_type not in self.functions:
            return text
        return self.functions[field_type](text)

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
    """
    Data parser based on proto file and related Python module.
    """

    def __init__(self, table_name, data_table, schema_table):
        self.table_name = table_name
        self.data_table = data_table
        self.schema_table = schema_table
        self.data_set_message = None  # Instance of data set message class in proto Python module.
        self.data_converter = Converter()

    def parse(self):
        """
        Parse data and fill into data set message instance.
        """
        self.__load_proto_module()
        self.__init_data_set_message()
        self.__fill_data_set_message()

    def get_text_data(self):
        """
        Get readable proto data.

        :return: (str)
            Readable proto data str.
        """
        if self.data_set_message is None:
            print("Data set message in {} is none".format(
                dtxt_util.get_proto_module_name(self.table_name)
            ))
            return None
        return str(self.data_set_message)

    def get_binary_data(self):
        """
        Get binary proto data.

        :return: (str)
            Binary proto data str.
        """
        if self.data_set_message is None:
            print("Data set message in {} is none".format(
                dtxt_util.get_proto_module_name(self.table_name)
            ))
            return None
        return self.data_set_message.SerializeToString()

    def __load_proto_module(self):
        """
        Load proto Python module.
        """
        module_name = dtxt_util.get_proto_module_name(self.table_name)
        try:
            sys.path.append(dtxt_argument.DIRECTORY["TEMP_DIRECTORY"])
            exec ("from {} import *".format(module_name))
        except BaseException:
            print("Load module: {} failed.".format(module_name))
            raise

    def __init_data_set_message(self):
        """
        Instantiate data set message class in proto Python module.
        """
        # Get data set message class definition in proto Python module.
        data_set_message_class = getattr(
            sys.modules[dtxt_util.get_proto_module_name(self.table_name)],
            dtxt_util.get_proto_data_set_message_name(self.table_name)
        )

        # Instantiate data set message class.
        self.data_set_message = data_set_message_class()

    def __fill_data_set_message(self):
        """
        Fill data into data set message field (Member variable of data set message instance).
        """
        if self.data_set_message is None:
            print("No data set message with name: {}".format(
                dtxt_util.get_proto_data_set_message_name(self.table_name)
            ))
            return
        # Get data set message field variable.
        data_set_message_field_name = dtxt_util.get_proto_data_set_message_field_name(self.table_name)
        data_set_message_field = self.data_set_message.__getattribute__(data_set_message_field_name)

        # Fill data into data set message field.
        for data_row in self.data_table.get_data_rows():
            message = data_set_message_field.add()
            self.__fill_data(message, data_row)

    def __fill_data(self, message, data_row):
        """
        Fill column data defined in schema table into data message.

        :param message:
            Data message instance.

        :param data_row:
            Row number in data table.
        """
        for schema_table_row in self.schema_table.get_data_rows():
            data_column_name = self.schema_table.get_data_text(
                schema_table_row,
                dtxt_argument.SCHEMA_TABLE["COLUMN"]["COLUMN_NAME"]
            )
            proto_field_type = self.schema_table.get_data_text(
                schema_table_row,
                dtxt_argument.SCHEMA_TABLE["COLUMN"]["PROTO_FIELD_TYPE"]
            )
            proto_field_name = self.schema_table.get_data_text(
                schema_table_row,
                dtxt_argument.SCHEMA_TABLE["COLUMN"]["PROTO_FIELD_NAME"]
            )
            cell_text = self.data_table.get_data_text(data_row, data_column_name)
            field_value = self.data_converter.to_value(proto_field_type, cell_text)
            message.__setattr__(proto_field_name, field_value)
