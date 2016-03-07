import unittest

from rcquerybuilder.builder import Builder


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_basic_fluent_api(self):
        qb = Builder(collection=None)

        qb.field('name').equals('foobar').field('fizz').ne(None)

        query_list = qb.get_query_list()

        assert query_list == {'name': 'foobar', 'fizz': {'$ne': None}}

    def test_find_query(self):
        qb = Builder(collection=None)
        qb.field('name').is_not_in(['Matthew', 'Boris']) \
            .field('age').gte(21) \
            .field('attributes').is_type('object')

        query_list = qb.get_query_list()

        assert {'name': {'$nin': ['Matthew', 'Boris']},
                'age': {'$gte': 21},
                'attributes': {'$type': 3}} == query_list

    def test_update_query(self):
        qb = Builder(collection=None)

        qb.update(multi=True) \
            .field('foo').equals('bar').set('buzz') \
            .field('totals').gt(10) \
            .field('counter').inc(1) \
            .field('some_list').push({'name': 'testing', 'value': 'cool'})

        query_parts = qb.get_query().query

        assert {'foo': 'bar',
                'totals': {'$gt': 10}} == query_parts['query']

        assert {'$set': {'foo': 'buzz'},
                '$inc': {'counter': 1},
                '$push': {'some_list': {'name': 'testing', 'value': 'cool'}}} == query_parts['newObj']

    def test_insert_query(self):
        qb = Builder(collection=None)

        qb.insert() \
            .field('name').set('awesome') \
            .field('age').set(21) \
            .field('attributes').set([0, 1, 2, 3])

        insert_query = qb.get_query().query['newObj']

        assert {'name': 'awesome',
                'age': 21,
                'attributes': [0, 1, 2, 3]} == insert_query


if __name__ == '__main__':
    unittest.main()
