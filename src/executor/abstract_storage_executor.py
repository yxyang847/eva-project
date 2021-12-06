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
from abc import ABC

from src.executor.abstract_executor import AbstractExecutor
from src.planner.storage_plan import StoragePlan


class AbstractStorageExecutor(AbstractExecutor, ABC):
    """
    Abstract executor for storage. This executor returns the batch frames
    from the storage layer.
    """

    def __init__(self, node: StoragePlan):
        super().__init__(node)
