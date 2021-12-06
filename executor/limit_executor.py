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
from typing import Iterator

from src.models.storage.batch import Batch
from src.executor.abstract_executor import AbstractExecutor
from src.planner.limit_plan import LimitPlan


class LimitExecutor(AbstractExecutor):
    """
    Limits the number of rows returned

    Arguments:
        node (AbstractPlan): The Limit Plan

    """

    def __init__(self, node: LimitPlan):
        super().__init__(node)
        self._limit_count = node.limit_value

    def validate(self):
        pass

    def exec(self) -> Iterator[Batch]:
        child_executor = self.children[0]
        remaining_tuples = self._limit_count
        # aggregates the batches into one large batch
        for batch in child_executor.exec():
            if len(batch) > remaining_tuples:
                yield batch[:remaining_tuples]
                return

            remaining_tuples -= len(batch)
            yield batch
