from zope.component import getUtility

from unittest import TestCase
from unittest import TestSuite, makeSuite

from kuleuven.lirias.core.interfaces import IStorage
from kuleuven.lirias.staff.testing import LIRIAS_FIXTURE
from kuleuven.lirias.staff.interfaces import IObjectEncoder
from kuleuven.lirias.staff.browser.publications_for_id import process_publications
from kuleuven.lirias.staff.interfaces import IPublication, IPublicationAuthor


class TestMySetup(TestCase):
    """blub"""
    layer = LIRIAS_FIXTURE

    def setUp(self):
        self.storage = getUtility(IStorage, 'liriasstorage')
        self.objectencoder = getUtility(IObjectEncoder, 'objectencoder')
        interfaces_list = [IPublication, IPublicationAuthor]
        self.objectencoder.configure(encodable_interfaces=interfaces_list)

    def test_objectencoder(self):
        self.assertEqual(1, 1)
        filter=dict()
        filter['author_ids'] = ['0000001', ]
        publications = self.storage.fetch_publications_for_author(
                        filter=filter)
        processed_pubs = process_publications(publications=publications, 
                        objectencoder=self.objectencoder, filter=filter)

        ref_pubs = "{'123456789/68434': {'status': 'draft', 'pub_title': None, 'pub_info': None, 'title': 'The Matrix Afterlife', 'pub_pages': None, 'date_issued': '2014-10-15', 'wos': 0, 'pub_issn': None, 'genre': None, 'pub_volume': None, 'aut': [{'author_pos': '1', 'first_name': 'trinity', 'last_name': '', 'role': 'aut', 'id': '0000001'}, {'author_pos': '2', 'first_name': 'neo', 'last_name': '', 'role': 'aut', 'id': '0000002'}], 'pub_issue': None, 'id': '123456789/68434'}, '123456789/68431': {'status': 'published', 'pub_title': None, 'pub_info': None, 'title': 'The Matrix', 'pub_pages': None, 'date_issued': '1999', 'wos': 0, 'pub_issn': None, 'genre': None, 'pub_volume': None, 'aut': [{'author_pos': '2', 'first_name': 'trinity', 'last_name': '', 'role': 'aut', 'id': '0000001'}, {'author_pos': '3', 'first_name': 'neo', 'last_name': '', 'role': 'aut', 'id': '0000002'}, {'author_pos': '1', 'first_name': 'morpheus', 'last_name': '', 'role': 'aut', 'id': '0000004'}], 'pub_issue': None, 'id': '123456789/68431'}, '123456789/68432': {'status': 'published', 'pub_title': None, 'pub_info': None, 'title': 'The Matrix Reloaded', 'pub_pages': None, 'date_issued': '2003-05-07', 'wos': 0, 'pub_issn': None, 'genre': None, 'pub_volume': None, 'aut': [{'author_pos': '2', 'first_name': 'trinity', 'last_name': '', 'role': 'aut', 'id': '0000001'}, {'author_pos': '1', 'first_name': 'neo', 'last_name': '', 'role': 'aut', 'id': '0000002'}, {'author_pos': '3', 'first_name': 'morpheus', 'last_name': '', 'role': 'aut', 'id': '0000004'}], 'pub_issue': None, 'id': '123456789/68432'}, '123456789/68433': {'status': 'accepted', 'pub_title': None, 'pub_info': None, 'title': 'The Matrix Revolutions', 'pub_pages': None, 'date_issued': '2003-11-05', 'wos': 0, 'pub_issn': None, 'genre': None, 'pub_volume': None, 'aut': [{'author_pos': '1', 'first_name': 'trinity', 'last_name': '', 'role': 'aut', 'id': '0000001'}, {'author_pos': '2', 'first_name': 'neo', 'last_name': '', 'role': 'aut', 'id': '0000002'}, {'author_pos': '3', 'first_name': 'morpheus', 'last_name': '', 'role': 'aut', 'id': '0000004'}], 'pub_issue': None, 'id': '123456789/68433'}}"


        self.assertEqual(ref_pubs, processed_pubs.__repr__())

    def xx_test_serializer(self):
        self.assertEqual(1, 1)
        filter=dict()
        filter['author_ids'] = ['0000001', ]
        publications = self.storage.fetch_publications_for_author(
                        filter=filter)
        from z3c.schema2json.tools import serialize
        processed_pubs = process_publications(publications=(publications[0],), 
                        objectencoder=self.objectencoder, filter=filter)
        z3c_pubs = serialize(IPublication, publications[0], pretty_print=False)

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestMySetup))
    return suite
