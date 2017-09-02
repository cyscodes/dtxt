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
# Input Settings
#

class DataTable:
    Directory = u'../example/tables'
    pass


class CatalogTable:
    FilePath = u'../example/schemas/Database.xlsx'

    SheetName = u'Sheet1'

    class Column:
        ExcelName = u'excel_name'

        SheetName = u'sheet_name'

        TableName = u'table_name'


class SchemaTable:
    Directory = u'../example/schemas'

    class Column:
        ColumnName = u'column_name'

        ProtoFieldName = u'proto_field_name'

        ProtoFieldType = u'proto_field_type'


#
# Output Settings
#

class DataFile:
    Directory = u'../example/Output/Data'


class ProtoFile:
    # TODO Fix to support
    Directory = None

    PackageName = u'MyPackage'

    DataSetMessageNameSuffix = u'DataSet'

    DataSetMessageFieldNameSuffix = u'Array'


class CSharpCodeFile:
    Directory = u'../example/Output/Codes'


class TemporaryFile:
    Directory = u'Temp'
