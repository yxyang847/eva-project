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
from typing import List
from src.parser.table_ref import TableRef
from src.catalog.models.df_column import DataFrameColumn


class CreatePlan(AbstractPlan):
    """
    This plan is used for storing information required for create table
    operations.
    Arguments:
        video_ref {TableRef} -- video ref for table to be created in storage
        column_list {List[DataFrameColumn]} -- Columns to be added
        if_not_exists {bool} -- Whether to override if there is existing table
    """

    def __init__(self, video_ref: TableRef,
                 column_list: List[DataFrameColumn],
                 if_not_exists: bool = False):
        super().__init__(PlanOprType.CREATE)
        self._video_ref = video_ref
        self._column_list = column_list
        self._if_not_exists = if_not_exists

    @property
    def video_ref(self):
        return self._video_ref

    @property
    def if_not_exists(self):
        return self._if_not_exists

    @property
    def column_list(self):
        return self._column_list
