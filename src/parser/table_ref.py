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

from __future__ import annotations
from typing import Union


from src.parser.select_statement import SelectStatement


class TableInfo:
    """
    stores all the table info, inspired from postgres
    """

    def __init__(self, table_name=None, schema_name=None, database_name=None):
        self._table_name = table_name
        self._schema_name = schema_name
        self._database_name = database_name

    @property
    def table_name(self):
        return self._table_name

    @property
    def schema_name(self):
        return self._schema_name

    @property
    def database_name(self):
        return self._database_name

    def __str__(self):
        table_info_str = "TABLE INFO:: (" + self._table_name + ")"

        return table_info_str

    def __eq__(self, other):
        if not isinstance(other, TableInfo):
            return False
        return (self.table_name == other.table_name
                and self.schema_name == other.schema_name
                and self.database_name == other.database_name)


class TableRef:
    """
    dummy class right now need to handle join expression
    Attributes:
        table: can be one of the following based on the query type:
            TableInfo: expression of table name and database name,
            SelectStatement: select statement in case of nested queries,
            JoinDefinition: join statement in case of join queries #TODO
        sample_freq: sampling frequency for the table reference
    """

    def __init__(self,
                 table: Union[TableInfo, SelectStatement] = None,
                 sample_freq: float = None):
        self._table = table
        self._sample_freq = sample_freq

    @property
    def table(self):
        return self._table

    @property
    def sample_freq(self):
        return self._sample_freq

    def is_select(self) -> bool:
        return isinstance(self.table, SelectStatement)

    def __str__(self):
        table_ref_str = "TABLE REF:: ( {} SAMPLE FREQUENCY {})".format(
            str(self.table), str(self.sample_freq))
        return table_ref_str

    def __eq__(self, other):
        if not isinstance(other, TableRef):
            return False
        return (self.table == other.table
                and self.sample_freq == other.sample_freq)
