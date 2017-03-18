# coding=utf-8

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

#
# Directory settings.
#

# Directory of designer tables.
DESIGNER_TABLE_DIRECTORY = "../example/tables"

# Directory of schemas.
SCHEMA_DIRECTORY = "../example/schemas"

# Directory of temporary files (include auto-generated proto files and protobuf python files).
# TODO：Fix the problem when TEMP_DIRECTORY is set to out of the bin directory
TEMP_DIRECTORY = "Temp"

# Directory of auto-generated data files.
PROTO_DATA_DIRECTORY = "../example/Output/Data"

# Directory of auto-generated code files.
PROTO_CODE_DIRECTORY = "../example/Output/Codes"

#
# File settings
#

# The file defines tables to process.
DATABASE_PATH = "../example/schemas/Database.xlsx"

DATABASE_SHEET = "Sheet1"

#
# Proto template settings.
#

PROTO_PACKAGE = "AncientOne"

PROTO_DATA_SET_MESSAGE_NAME_SUFFIX = "DataSet"

PROTO_DATA_SET_MESSAGE_FIELD_NAME_SUFFIX = "Array"
