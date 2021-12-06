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

from src.planner.abstract_plan import AbstractPlan
from src.planner.types import PlanOprType
from src.expression.constant_value_expression import ConstantValueExpression


class SamplePlan(AbstractPlan):
    """
    This plan is used for storing information required for sample
    operations.

    Arguments:
        sample_freq: ConstantValueExpression
            A ConstantValueExpression which is the count of the
            gap between frames sampled.
    """

    def __init__(self, sample_freq: ConstantValueExpression):
        self._sample_freq = sample_freq
        super().__init__(PlanOprType.SAMPLE)

    @property
    def sample_freq(self):
        return self._sample_freq
