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

import dtxt_argument
import dtxt_code
import dtxt_data
import dtxt_proto2
import dtxt_table
import dtxt_tepb
import dtxt_util


def generate_proto_file(schema, table_name):
    proto = dtxt_proto2.create_proto_by_schema_table(schema, table_name, dtxt_argument.PROTO["PACKAGE_NAME"])
    dtxt_util.write_to_file(
        dtxt_util.get_proto_file_path(table_name),
        "wb+",
        dtxt_proto2.Generator.get_proto_string(proto)
    )


def generate_proto_python_code_file(table_name):
    dtxt_code.Generator.to_python_file(
        dtxt_util.get_proto_file_path(table_name),
        dtxt_util.get_proto_file_path(table_name)
    )


def generate_proto_data_file(table_name, table, schema):
    parser = dtxt_data.Parser(table_name, table, schema)
    parser.parse()
    dtxt_util.write_to_file(
        dtxt_util.get_proto_text_data_path(table_name),
        "wb+",
        parser.get_text_data()
    )
    dtxt_util.write_to_file(
        dtxt_util.get_proto_binary_data_path(table_name),
        "wb+",
        parser.get_binary_data()
    )


def generate_proto_csharp_code_file(table_name):
    dtxt_code.Generator.to_csharp_file(
        dtxt_util.get_proto_file_path(table_name),
        dtxt_util.get_code_file_path(table_name)
    )


if __name__ == '__main__':
    # Open database table
    database_table = dtxt_table.create_table_by_excel_sheet(
        dtxt_argument.DATABASE_TABLE["PATH"],
        dtxt_argument.DATABASE_TABLE["SHEET_NAME"]
    )

    # Export tables defined in database table
    for data_row in database_table.get_data_rows():
        excel_name = database_table.get_data_text(data_row, dtxt_argument.DATABASE_TABLE["COLUMN"]["EXCEL_NAME"])
        sheet_name = database_table.get_data_text(data_row, dtxt_argument.DATABASE_TABLE["COLUMN"]["SHEET_NAME"])
        table_name = database_table.get_data_text(data_row, dtxt_argument.DATABASE_TABLE["COLUMN"]["TABLE_NAME"])

        table = dtxt_table.create_table_by_excel_sheet(
            dtxt_util.get_designer_table_path(excel_name),
            sheet_name
        )
        schema = dtxt_table.create_table_by_excel_sheet(
            dtxt_util.get_schema_table_path(excel_name),
            sheet_name
        )

        generate_proto_file(schema, table_name)
        generate_proto_python_code_file(table_name)
        generate_proto_data_file(table_name, table, schema)
        generate_proto_csharp_code_file(table_name)

    # Close database table
    database_table.dispose()
