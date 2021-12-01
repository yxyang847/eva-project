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
import os
import base64

from src.catalog.catalog_manager import CatalogManager
from src.planner.delete_plan import DeletePlan
from src.executor.abstract_executor import AbstractExecutor

from src.storage.storage_engine import StorageEngine
from src.models.storage.batch import Batch
from src.configuration.configuration_manager import ConfigurationManager


class DeleteExecutor(AbstractExecutor):

    def __init__(self, node: DeletePlan):
        super().__init__(node)
        config = ConfigurationManager()
        self.path_prefix = config.get_value('storage', 'path_prefix')

    def validate(self):
        pass

    def exec(self):
        """
        Upload the video blob into the location defined by 'path'
        on the server. The video blob is in base64 format, so
        it will first be decoded by the executor and then saved
        at the specified path with a predefined prefix
        """

        # path = self.node.file_path
        path = "test_video.mp4"
        final_path = os.path.join(self.path_prefix, path)
        if os.path.exists(final_path):
            os.remove(final_path)

        video_id = self.node.video_catalog_id
        # data_tuple = []
        # for col, val in zip(self.node.column_list, self.node.value_list):
        #     val = val.evaluate()
        #     val.frames.columns = [col.col_name]
        #     data_tuple.append(val)

        # batch = Batch.merge_column_wise(data_tuple)
        #metadata = CatalogManager().get_metadata(video_id)
        # verify value types are consistent

        CatalogManager().delete_metadata_new(video_id)

        # batch.frames = SchemaUtils.petastorm_type_cast(
        #     metadata.schema.petastorm_schema, batch.frames)
        # StorageEngine.write(metadata, batch)
        
