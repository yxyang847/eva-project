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
import pandas as pd
from typing import Any
from src.expression.abstract_expression import AbstractExpression, \
    ExpressionType
from src.models.storage.batch import Batch
from src.catalog.column_type import ColumnType


class ConstantValueExpression(AbstractExpression):
    # ToDo Implement generic value class
    # for now we don't assign any class to value
    # it can have types like string, int etc
    # return type not set, handle that based on value
    def __init__(self, value: Any, v_type: ColumnType = ColumnType.INTEGER):
        super().__init__(ExpressionType.CONSTANT_VALUE)
        self._value = value
        self._v_type = v_type

    def evaluate(self, *args, **kwargs):
        return Batch(pd.DataFrame({0: [self._value]}))

    @property
    def value(self):
        return self._value

    @property
    def v_type(self):
        return self._v_type
    # ToDo implement other functionalities like maintaining hash
    # comparing two objects of this class(==)

    def __eq__(self, other):
        is_subtree_equal = super().__eq__(other)
        if not isinstance(other, ConstantValueExpression):
            return False
        # if the value type is NDARRAY, we need to reduce the
        # iterator to bool
        is_equal = is_subtree_equal and self.v_type == other.v_type

        if self.v_type == ColumnType.NDARRAY:
            return is_equal and all(self.value == other.value)
        else:
            return is_equal and self.value == other.value
