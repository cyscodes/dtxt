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

import dtxt_tepb
import dtxt_code
import dtxt_proto2
import dtxt_data
import dtxt_argument
import dtxt_util


def generate_proto(schema, table_name):
    proto = dtxt_proto2.create_proto_from_schema(schema, table_name, dtxt_argument.PROTO_PACKAGE)
    dtxt_util.write_to_file(dtxt_util.get_proto_path(table_name), "wb+", dtxt_proto2.Generator.get_proto_string(proto))
    pass


def generate_proto_python_code(table_name):
    dtxt_code.Generator.to_python_file(dtxt_util.get_proto_path(table_name), dtxt_util.get_proto_path(table_name))


def generate_proto_data(table_name, table, schema):
    parser = dtxt_data.Parser(table_name, table, schema)
    parser.parse()
    dtxt_util.write_to_file(dtxt_util.get_proto_text_data_path(table_name), "wb+", parser.get_text_data())
    dtxt_util.write_to_file(dtxt_util.get_proto_binary_data_path(table_name), "wb+", parser.get_binary_data())


def generate_proto_csharp_code(table_name):
    dtxt_code.Generator.to_csharp_file(dtxt_util.get_proto_path(table_name), dtxt_util.get_code_path(table_name))


if __name__ == '__main__':
    database_excel = dtxt_tepb.Tepb(dtxt_argument.DATABASE_PATH, dtxt_argument.DATABASE_SHEET)
    database_excel.open_excel_file()
    database_table = dtxt_data.Table(database_excel)
    for data_row in database_table.get_data_rows():
        excel_name = database_table.get_data_text(data_row, "excel_name")
        sheet_name = database_table.get_data_text(data_row, "sheet_name")
        table_name = database_table.get_data_text(data_row, "table_name")

        designer_excel = dtxt_tepb.Tepb(dtxt_util.get_designer_excel_path(excel_name), sheet_name)
        designer_excel.open_excel_file()
        table = dtxt_data.Table(designer_excel)

        schema_excel = dtxt_tepb.Tepb(dtxt_util.get_schema_excel_path(excel_name), sheet_name)
        schema_excel.open_excel_file()
        schema = dtxt_data.Schema(dtxt_data.Table(schema_excel))

        generate_proto(schema, table_name)
        generate_proto_python_code(table_name)
        generate_proto_data(table_name, table, schema)
        generate_proto_csharp_code(table_name)
