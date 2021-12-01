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

from src.parser.delete_statement import DeleteStatement
from src.parser.table_ref import TableRef

from src.parser.evaql.evaql_parserVisitor import evaql_parserVisitor
from src.parser.evaql.evaql_parser import evaql_parser


class Delete(evaql_parserVisitor):
    def visitDeleteStatement(self, ctx: evaql_parser.DeleteStatementContext):
        delete_stmt = self.visitChildren(ctx)
        return delete_stmt

    def visitSingleDeleteStatement(self, ctx: evaql_parser.SingleDeleteStatementContext):
        # from_table = self.visit(ctx.fileName()).value
        from_table = TableRef(self.visit(ctx.tableName()))
        # where_clause = self.visit(ctx.expression())
        stmt = DeleteStatement(from_table, None)
        return stmt
