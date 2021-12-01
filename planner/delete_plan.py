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
from pathlib import Path


class DeletePlan(AbstractPlan):
    """
    This plan is used for storing information required for upload
    operations.

    Arguments:
        path(Path): file path (with prefix prepended) where
                    the data is uploaded
        video_blob(str): base64 encoded video string
        """

    def __init__(self, video_catalog_id: int):
        super().__init__(PlanOprType.DELETE)
        self._video_catalog_id = video_catalog_id

    # def __init__(self, from_table: TableRef = None,
    #              where_clause: AbstractExpression = None,
    #              **kwargs):
    #     super().__init__(PlanOprType.DELETE)
    #     self._from_table = from_table
    #     self._where_clause = where_clause

    @property
    def video_catalog_id(self):
        return self._video_catalog_id

    def __str__(self):
        print_str = 'DeletePlan(video_catalog_id={})'.format(
            self.video_catalog_id)
        return print_str
