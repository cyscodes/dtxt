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

import os


class Generator:
    def __init__(self):
        pass

    @classmethod
    def to_csharp_file(cls, proto_path, code_path):
        if not os.path.isfile(proto_path):
            print("{} is missing.".format(proto_path))
            return
        os.system("protogen -i:{proto_path} -o:{code_path}".format(
            proto_path=proto_path,
            code_path=code_path
        ))

    @classmethod
    def to_python_file(cls, proto_path, code_path):
        if not os.path.isfile(proto_path):
            print("{} is missing.".format(proto_path))
            return
        proto_directory, proto_filename = os.path.split(proto_path)
        code_directory, code_filename = os.path.split(code_path)
        os.system("protoc --proto_path={proto_directory} --python_out={code_directory} {proto_path}".format(
            proto_directory=proto_directory,
            code_directory=code_directory,
            proto_path=proto_path
        ))
        # TODO: Rename generated python file to code_filename
