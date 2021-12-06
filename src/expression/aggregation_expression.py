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
from src.expression.abstract_expression import AbstractExpression, \
    ExpressionType, \
    ExpressionReturnType
from src.models.storage.batch import Batch


class AggregationExpression(AbstractExpression):

    def __init__(self, exp_type: ExpressionType, left: AbstractExpression,
                 right: AbstractExpression):
        children = []
        if left is not None:
            children.append(left)
        if right is not None:
            children.append(right)
        super().__init__(exp_type, rtype=ExpressionReturnType.INTEGER,
                         children=children)  # can also be a float

    def evaluate(self, *args, **kwargs):
        batch = self.get_child(0).evaluate(*args, **kwargs)
        if self.etype == ExpressionType.AGGREGATION_SUM:
            return Batch(frames=batch.frames.agg(['sum']))
        elif self.etype == ExpressionType.AGGREGATION_COUNT:
            return Batch(frames=batch.frames.agg(['count']))
        elif self.etype == ExpressionType.AGGREGATION_AVG:
            return Batch(frames=batch.frames.agg(['mean']))
        elif self.etype == ExpressionType.AGGREGATION_MIN:
            return Batch(frames=batch.frames.agg(['min']))
        elif self.etype == ExpressionType.AGGREGATION_MAX:
            return Batch(frames=batch.frames.agg(['max']))

    def __eq__(self, other):
        is_subtree_equal = super().__eq__(other)
        if not isinstance(other, AggregationExpression):
            return False
        return (is_subtree_equal
                and self.etype == other.etype)
