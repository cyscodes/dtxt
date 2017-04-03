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

#
# Directory settings.
#
DIRECTORY = {
    # Directory of designer tables.
    "DESIGNER_TABLE_DIRECTORY": "../example/tables",

    # Directory of schemas.
    "SCHEMA_DIRECTORY": "../example/schemas",

    # Directory of temporary files (include auto-generated proto files and protobuf python files).
    # TODO：Fix the problem when TEMP_DIRECTORY is set to out of the bin directory
    "TEMP_DIRECTORY": "Temp",

    # Directory of auto-generated data files.
    "PROTO_DATA_DIRECTORY": "../example/Output/Data",

    # Directory of auto-generated code files.
    "PROTO_CODE_DIRECTORY": "../example/Output/Codes",
}

#
# Proto file template settings.
#

PROTO = {
    "PACKAGE_NAME": "MyPackage",
    "DATA_SET_MESSAGE_NAME_SUFFIX": "DataSet",
    "DATA_SET_MESSAGE_FIELD_NAME_SUFFIX": "Array"
}

#
# Config table settings.
#

DATABASE_TABLE = {
    "PATH": "../example/schemas/Database.xlsx",
    "SHEET_NAME": "Sheet1",
    "COLUMN": {
        "EXCEL_NAME": "excel_name",
        "SHEET_NAME": "sheet_name",
        "TABLE_NAME": "table_name"
    }
}

SCHEMA_TABLE = {
    "COLUMN": {
        "COLUMN_NAME": "column_name",
        "PROTO_FIELD_NAME": "proto_field_name",
        "PROTO_FIELD_TYPE": "proto_field_type"
    }
}
