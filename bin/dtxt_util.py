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

import os

import dtxt_argument


def write_to_file(path, mode, data):
    """
    Write data to path in specified mode.
    The directory will be auto-created if it does not exist.

    :param path: (str)
        Output file path.

    :param mode: (str)
        Write mode.

    :param data: (str)
        Data to write.
    """
    # Create directory if not exist.
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write to file.
    target_file = open(path, mode)
    target_file.write(data)
    target_file.close()


def get_designer_table_path(filename):
    return os.path.join(dtxt_argument.DIRECTORY["DESIGNER_TABLE_DIRECTORY"], filename)


def get_schema_table_path(filename):
    return os.path.join(dtxt_argument.DIRECTORY["SCHEMA_DIRECTORY"], filename)


def get_proto_file_path(table_name):
    return os.path.join(dtxt_argument.DIRECTORY["TEMP_DIRECTORY"], "{}.proto".format(table_name))


def get_code_file_path(table_name):
    return os.path.join(dtxt_argument.DIRECTORY["PROTO_CODE_DIRECTORY"], "{}.cs".format(table_name))


def get_proto_text_data_path(table_name):
    return os.path.join(dtxt_argument.DIRECTORY["PROTO_DATA_DIRECTORY"], "{}.txt".format(table_name))


def get_proto_binary_data_path(table_name):
    return os.path.join(dtxt_argument.DIRECTORY["PROTO_DATA_DIRECTORY"], "{}.binary".format(table_name))


def get_proto_module_name(table_name):
    return "{}_pb2".format(table_name)


def get_proto_data_set_message_name(table_name):
    return "{}{}".format(table_name, dtxt_argument.PROTO["DATA_SET_MESSAGE_NAME_SUFFIX"])


def get_proto_data_set_message_field_name(table_name):
    return "{}{}".format(table_name, dtxt_argument.PROTO["DATA_SET_MESSAGE_FIELD_NAME_SUFFIX"])
