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
from src.planner.union_plan import UnionPlan
from src.utils.logging_manager import LoggingManager, LoggingLevel


class UnionExecutor(AbstractExecutor):
    """
    Merge the seq scan queries
    Arguments:
        node (AbstractPlan): The UnionPlan

    """

    def __init__(self, node: UnionPlan):
        super().__init__(node)

    def validate(self):
        pass

    def exec(self) -> Iterator[Batch]:
        if self.node.all is False:
            LoggingManager().log('Only UNION ALL is supported now.',
                                 LoggingLevel.WARNING)

        # We should have only two children
        for child in self.children:
            for batch in child.exec():
                yield batch
