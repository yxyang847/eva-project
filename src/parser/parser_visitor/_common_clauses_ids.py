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

import warnings
from src.parser.evaql.evaql_parserVisitor import evaql_parserVisitor

from src.expression.tuple_value_expression import TupleValueExpression

from src.parser.table_ref import TableInfo

from src.parser.evaql.evaql_parser import evaql_parser

from src.utils.logging_manager import LoggingLevel, LoggingManager


##################################################################
# COMMON CLAUSES Ids, Column_names, Table_names
##################################################################
class CommonClauses(evaql_parserVisitor):
    def visitTableName(self, ctx: evaql_parser.TableNameContext):

        table_name = self.visit(ctx.fullId())
        if table_name is not None:
            table_info = TableInfo(table_name=table_name)
            return table_info
        else:
            warnings.warn("Invalid from table", SyntaxWarning)

    def visitFullColumnName(self, ctx: evaql_parser.FullColumnNameContext):
        # Adding support for a.b
        # Will restrict implementation to raise error for a.b.c
        dottedIds = []
        if ctx.dottedId():
            if len(ctx.dottedId()) != 1:
                LoggingManager().log("Only tablename.colname syntax supported",
                                     LoggingLevel.ERROR)
                return
            for id in ctx.dottedId():
                dottedIds.append(self.visit(id))

        uid = self.visit(ctx.uid())

        if len(dottedIds):
            return TupleValueExpression(table_name=uid, col_name=dottedIds[0])
        else:
            return TupleValueExpression(col_name=uid)

    def visitSimpleId(self, ctx: evaql_parser.SimpleIdContext):
        # todo handle children, right now assuming TupleValueExpr
        return ctx.getText()
        # return self.visitChildren(ctx)

    def visitDottedId(self, ctx: evaql_parser.DOT_ID):
        if ctx.DOT_ID():
            return ctx.getText()[1:]
        if ctx.uid():
            return self.visit(ctx.uid())
