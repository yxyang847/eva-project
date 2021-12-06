import unittest
import pandas as pd
import numpy as np

from src.executor.orderby_executor import OrderByExecutor
from src.executor.limit_executor import LimitExecutor
from src.expression.tuple_value_expression import TupleValueExpression
from src.models.storage.batch import Batch
from src.parser.types import ParserOrderBySortType
from test.executor.utils import DummyExecutor
from src.planner.orderby_plan import OrderByPlan
from src.planner.limit_plan import LimitPlan
from src.expression.constant_value_expression import ConstantValueExpression


class LimitExecutorTest(unittest.TestCase):

    def test_should_return_smaller_num_rows(self):
        dfs = [pd.DataFrame(np.random.randint(0, 100, size=(100, 4)),
                            columns=list('ABCD')) for _ in range(4)]

        batches = [Batch(frames=df) for df in dfs]

        limit_value = 125

        plan = LimitPlan(ConstantValueExpression(limit_value))

        limit_executor = LimitExecutor(plan)
        limit_executor.append_child(DummyExecutor(batches))
        reduced_batches = list(limit_executor.exec())

        total_size = 0
        for batch in reduced_batches:
            total_size += batch.batch_size

        self.assertEqual(total_size, limit_value)

    def test_should_return_limit_greater_than_size(self):
        """ This should return the exact same data
        if the limit value is greater than what is present.
        This will also leave a warning """

        dfs = [pd.DataFrame(np.random.randint(0, 100, size=(100, 4)),
                            columns=list('ABCD')) for _ in range(4)]

        batches = [Batch(frames=df) for df in dfs]

        previous_total_size = 0
        for batch in batches:
            previous_total_size += batch.batch_size

        limit_value = 500

        plan = LimitPlan(ConstantValueExpression(limit_value))

        limit_executor = LimitExecutor(plan)
        limit_executor.append_child(DummyExecutor(batches))
        reduced_batches = list(limit_executor.exec())

        after_total_size = 0
        for batch in reduced_batches:
            after_total_size += batch.batch_size

        self.assertEqual(previous_total_size, after_total_size)

    def test_should_return_top_frames_after_sorting(self):
        """
        Checks if limit returns the top 2 rows from the data
        after sorting

        data (3 batches):
        'A' 'B' 'C'
        [1, 1, 1]
        ----------
        [1, 5, 6]
        [4, 7, 10]
        ----------
        [2, 9, 7]
        [4, 1, 2]
        [4, 2, 4]
        """

        df1 = pd.DataFrame(
            np.array([[1, 1, 1]]), columns=['A', 'B', 'C'])
        df2 = pd.DataFrame(
            np.array([[1, 5, 6], [4, 7, 10]]), columns=['A', 'B', 'C'])
        df3 = pd.DataFrame(
            np.array([[2, 9, 7], [4, 1, 2],
                      [4, 2, 4]]), columns=['A', 'B', 'C'])

        batches = [Batch(frames=df) for df in [df1, df2, df3]]

        "query: .... ORDER BY A ASC, B DESC limit 2"

        plan = OrderByPlan(
            [(TupleValueExpression('A'), ParserOrderBySortType.ASC),
             (TupleValueExpression('B'), ParserOrderBySortType.DESC)])

        orderby_executor = OrderByExecutor(plan)
        orderby_executor.append_child(DummyExecutor(batches))

        sorted_batches = list(orderby_executor.exec())

        limit_value = 2
        plan = LimitPlan(ConstantValueExpression(limit_value))
        limit_executor = LimitExecutor(plan)
        limit_executor.append_child(DummyExecutor(sorted_batches))
        reduced_batches = list(limit_executor.exec())

        # merge everything into one batch
        aggregated_batch = Batch.concat(reduced_batches, copy=False)
        """
           A  B   C
        0  1  5   6
        1  1  1   1
        """

        expected_df1 = pd.DataFrame(
            np.array([[1, 5, 6], [1, 1, 1]]), columns=['A', 'B', 'C'])

        expected_batches = [Batch(frames=df) for df in [expected_df1]]

        self.assertEqual(expected_batches[0], aggregated_batch)
