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

import dtxt_util
import dtxt_settings


class EnumFieldRule:
    """
    Enumerator of Proto2 message field rule.
    """
    REQUIRED = "required"
    OPTIONAL = "optional"
    REPEATED = "repeated"

    def __init__(self):
        pass


class EnumFieldType:
    """
    Enumerator of Proto2 message field type.
    """
    DOUBLE = "double"
    FLOAT = "float"
    INT32 = "int32"
    INT64 = "int64"
    UINT32 = "uint32"
    UINT64 = "uint64"
    SINT32 = "sint32"
    SINT64 = "sint64"
    FIXED32 = "fixed32"
    FIXED64 = "fixed64"
    SFIXED32 = "sfixed32"
    SFIXED64 = "sfixed64"
    BOOL = "bool"
    STRING = "string"
    BYTES = "bytes"

    def __init__(self):
        pass


class Proto:
    """
    Proto2 data structure.
    """

    def __init__(self, package=None, messages=None):
        self.package = package
        self.messages = messages


class Message:
    """
    Proto2 message data structure.
    """

    def __init__(self, name=None, fields=None, comment=None):
        self.name = name
        self.fields = fields
        self.comment = comment


class MessageField:
    """
    Proto2 message field data structure.
    """

    def __init__(self, field_rule=None, field_type=None, name=None, tag=None, comment=None):
        self.field_rule = field_rule
        self.field_type = field_type
        self.name = name
        self.tag = tag
        self.comment = comment


class Generator:
    """
    Text generator in proto2 format.
    """
    INDENT_TEMPLATE = "\t"

    PROTO_PACKAGE_TEMPLATE = "%(indent)spackage %(package)s;"

    MESSAGE_TEMPLATE = "%(indent)s// %(comment)s\n%(indent)smessage %(name)s {\n%(message_field)s\n%(indent)s}"

    MESSAGE_FIELD_TEMPLATE = "%(indent)s%(field_rule)s %(field_type)s %(name)s = %(tag)s; // %(comment)s"

    def __init__(self):
        pass

    @classmethod
    def get_proto_string(cls, proto, indent=0):
        """
        Get proto text.

        :param proto: (Proto)
            Proto data.

        :param indent: (int)
            Indent of proto text. Should be non-negative int.

        :return: (str)
            Text of proto data.
        """
        if not isinstance(proto, Proto):
            return ""

        indent_text = cls.__get_indent_string(indent)
        texts = []

        # Set package text
        if proto.package is not None:
            texts.append(cls.PROTO_PACKAGE_TEMPLATE % dict(
                indent=indent_text,
                package=proto.package))

        # Set messages text
        if proto.messages is not None:
            for message in proto.messages:
                texts.append(cls.get_message_string(message, indent))

        return "\n".join(texts)

    @classmethod
    def get_message_string(cls, message, indent=0):
        """
        Get message text.

        :param message: (Message)
            Message data.

        :param indent: (int)
            Indent of message text. Should be non-negative int.

        :return:(str)
            Text of message data.
        """
        if not isinstance(message, Message):
            return ""

        indent_text = cls.__get_indent_string(indent)
        message_field_text = ""

        # Set message fields text
        if message.fields is not None:
            message_field_text = '\n'.join([cls.get_message_field_string(i, indent + 1) for i in message.fields])

        return cls.MESSAGE_TEMPLATE % dict(
            indent=indent_text,
            name=message.name,
            message_field=message_field_text,
            comment=message.comment
        )

    @classmethod
    def get_message_field_string(cls, message_field, indent=0):
        """
        Get message field text.

        :param message_field: (MessageField)
            Message field data.

        :param indent: (int)
            Indent of message field text. Should be non-negative int.

        :return: (str)
            Text of message field data.
        """
        if not isinstance(message_field, MessageField):
            return ""

        indent_text = cls.__get_indent_string(indent)

        return cls.MESSAGE_FIELD_TEMPLATE % dict(
            indent=indent_text,
            field_rule=message_field.field_rule,
            field_type=message_field.field_type,
            name=message_field.name,
            tag=message_field.tag,
            comment=message_field.comment
        )

    @classmethod
    def __get_indent_string(cls, indent):
        if indent < 0:
            return ""
        return "".join([cls.INDENT_TEMPLATE] * indent)


#
# Factory method for create proto.
#


def create_proto_by_schema_table(schema_table, table_name, package_name):
    # Create data message.
    data_message = Message(table_name, [])
    for schema_table_row in schema_table.get_data_rows():
        proto_field_type = schema_table.get_data_text(schema_table_row, dtxt_settings.SchemaTable.Column.ProtoFieldType)
        proto_field_name = schema_table.get_data_text(schema_table_row, dtxt_settings.SchemaTable.Column.ProtoFieldName)
        message_field = MessageField(EnumFieldRule.REQUIRED, proto_field_type, proto_field_name, schema_table_row)
        data_message.fields.append(message_field)

    # Create data set message.
    data_set_message = Message(dtxt_util.get_proto_data_set_message_name(table_name), [])
    DATA_SET_MESSAGE_TAG = 1
    data_set_message_field = MessageField(
        EnumFieldRule.REPEATED,
        table_name,
        dtxt_util.get_proto_data_set_message_field_name(table_name),
        DATA_SET_MESSAGE_TAG)
    data_set_message.fields.append(data_set_message_field)

    # Create proto.
    proto = Proto(package_name, [data_message, data_set_message])
    return proto
