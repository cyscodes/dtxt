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
    # Create directory if not exist.
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write to file.
    target_file = open(path, mode)
    target_file.write(data)
    target_file.close()


def to_unicode(text):
    if isinstance(text, str):
        # TODO: The text maybe not encoded in utf-8.
        return text.decode("utf8")
    if isinstance(text, unicode):
        return text
    print("Cannot convert input to unicode")
    return None

def to_utf8_string(text):
    unicode_text = to_unicode(text)
    if unicode_text is not None:
        return unicode_text.encode("utf8")
    return None


# TODO
def get_designer_excel_path(filename):
    return os.path.join(dtxt_argument.DESIGNER_TABLE_DIRECTORY, filename)


# TODO
def get_schema_excel_path(filename):
    return os.path.join(dtxt_argument.SCHEMA_DIRECTORY, filename)


# TODO
def get_proto_path(table_name):
    return "%(directory)s/%(filename)s.proto" % dict(
        directory=dtxt_argument.TEMP_DIRECTORY,
        filename=table_name)


# TODO
def get_code_path(table_name):
    return "%(directory)s/%(filename)s.cs" % dict(
        directory=dtxt_argument.PROTO_CODE_DIRECTORY,
        filename=table_name)


# TODO
def get_proto_text_data_path(table_name):
    return "%(directory)s/%(table_name)s.txt" % dict(
        directory=dtxt_argument.PROTO_DATA_DIRECTORY,
        table_name=table_name)


# TODO
def get_proto_binary_data_path(table_name):
    return "%(directory)s/%(table_name)s.binary" % dict(
        directory=dtxt_argument.PROTO_DATA_DIRECTORY,
        table_name=table_name)


def get_proto_module_name(table_name):
    return "%s_pb2" % table_name


def get_proto_data_set_message_name(table_name):
    return "%(table_name)s%(suffix)s" % dict(
        table_name=table_name,
        suffix=dtxt_argument.PROTO_DATA_SET_MESSAGE_NAME_SUFFIX)


def get_proto_data_set_message_field_name(table_name):
    return "%(table_name)s%(suffix)s" % dict(
        table_name=table_name,
        suffix=dtxt_argument.PROTO_DATA_SET_MESSAGE_FIELD_NAME_SUFFIX)
