import unittest

from rcquerybuilder.builder import Builder


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_basic_fluent_api(self):
        qb = Builder(collection=None)

        qb.field('name').equals('foobar').field('fizz').ne(None)

        query_list = qb.get_query_list()

        assert query_list == {'name': 'foobar', 'fizz': {'$ne': None}}


if __name__ == '__main__':
    unittest.main()
