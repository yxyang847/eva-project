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
from src.planner.storage_plan import StoragePlan
from src.storage.storage_engine import StorageEngine


class StorageExecutor(AbstractExecutor):

    def __init__(self, node: StoragePlan):
        super().__init__(node)

    def validate(self):
        pass

    def exec(self) -> Iterator[Batch]:
        return StorageEngine.read(self.node.video, self.node.batch_mem_size)
