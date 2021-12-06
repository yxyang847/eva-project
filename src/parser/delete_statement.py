# coding=utf-8
# Copyright 2018-2020 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from src.parser.statement import AbstractStatement
from src.parser.table_ref import TableRef

from src.parser.types import StatementType
from src.expression.abstract_expression import AbstractExpression
from pathlib import Path


class DeleteStatement(AbstractStatement):
    """
    Upload Statement constructed after parsing the input query

    Arguments:
        path(Path): file path (with prefix prepended) where
                    the data is uploaded
        video_blob(str): base64 encoded video string
    """

    def __init__(self, from_table: TableRef = None,
                 where_clause: AbstractExpression = None,
                 **kwargs):
        super().__init__(StatementType.DELETE)
        self._from_table = from_table
        self._where_clause = where_clause

    def __str__(self) -> str:
        print_str = "DELETE FROM {}".format(self._from_table)
        print_str += " WHERE " + str(self._where_clause)
        return print_str

    @property
    def where_clause(self):
        return self._where_clause

    @where_clause.setter
    def where_clause(self, where_expr: AbstractExpression):
        self._where_clause = where_expr

    @property
    def from_table(self):
        return self._from_table

    @from_table.setter
    def from_table(self, table: TableRef):
        self._from_table = table

    def __eq__(self, other):
        if not isinstance(other, DeleteStatement):
            return False
        return (self.from_table == other.from_table
                and self.where_clause == other.where_clause)
