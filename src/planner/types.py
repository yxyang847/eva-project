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
from enum import unique, IntEnum, auto


@unique
class PlanOprType(IntEnum):
    SEQUENTIAL_SCAN = auto()
    STORAGE_PLAN = auto()
    PP_FILTER = auto()
    INSERT = auto()
    CREATE = auto()
    CREATE_UDF = auto()
    LOAD_DATA = auto()
    UPLOAD = auto()
    UNION = auto()
    ORDER_BY = auto()
    LIMIT = auto()
    SAMPLE = auto()
    DELETE = auto()
    # add other types
