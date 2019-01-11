# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from kb_ModelIndexer.kb_ModelIndexerImpl import kb_ModelIndexer
from kb_ModelIndexer.kb_ModelIndexerServer import MethodContext
from kb_ModelIndexer.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace
from unittest.mock import Mock
import json


class kb_ModelIndexerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_ModelIndexer'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.cfg['workspace-admin-token'] = token

        # Getting username from Auth profile for token
        # authServiceUrl = cls.cfg['auth-service-url']
        # auth_client = _KBaseAuth(authServiceUrl)
        # user_id = auth_client.get_user(token)
        user_id = 'bogus'
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_ModelIndexer',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = kb_ModelIndexer(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.mock_dir = os.path.join(cls.test_dir, 'mock_data')

        cls.wsinfo = cls.read_mock('get_workspace_info.json')
        cls.mediaobj = cls.read_mock('media_object.json')
        cls.fbamodelobj = cls.read_mock('fbamodel_object.json')
        cls.gensubobj = cls.read_mock('genome_sub_object.json')

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    @classmethod
    def read_mock(cls, filename):
        with open(os.path.join(cls.mock_dir, filename)) as f:
            obj = json.loads(f.read())
        return obj

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_ModelIndexer_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def _validate(self, sfile, data):
        with open(self.test_dir + '/../' + sfile) as f:
            d = f.read()

        schema = json.loads(d)
        for key in schema['schema'].keys():
            self.assertIn(key, data)

    def _validate_features(self, sfile, data, plist):
        with open(self.test_dir + '/../' + sfile) as f:
            d = f.read()
        feature = data['features'][0]
        parent = data['parent']

        schema = json.loads(d)
        for key in schema['schema'].keys():
            if key in plist:
                self.assertIn(key, parent)
            else:
                self.assertIn(key, feature)

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_mappings(self):
        ret = self.getImpl().fbamodel_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().media_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().media_compound_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().modelcompound_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().modelreaction_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])

        ret = self.getImpl().modelreactionproteinsubunit_mapping(self.getContext(), {})
        self.assertIsNotNone(ret[0])


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_indexers(self):
        impl = self.getImpl()
        params = {'upa': '1/2/3'}
        impl.indexer.ws.get_objects2 = Mock()

        impl.indexer.ws.get_objects2.return_value = self.mediaobj
        ret = impl.media_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('media_schema.json', ret[0]['data'])
        ret = impl.media_compound_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self._validate_features('media_compound_schema.json', ret[0], [])

        m2 = self.read_mock('media2_object.json')
        impl.indexer.ws.get_objects2.return_value = m2
        ret = impl.media_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('media_schema.json', ret[0]['data'])
        ret = impl.media_compound_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self._validate_features('media_compound_schema.json', ret[0], [])

        impl.indexer.ws.get_objects2.return_value = self.fbamodelobj
        impl.indexer.ws.get_objects2.side_effect = [self.fbamodelobj, self.gensubobj]
        ret = impl.fbamodel_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self._validate('fbamodel_schema.json', ret[0]['data'])

        impl.indexer.ws.get_objects2.return_value = self.fbamodelobj
        impl.indexer.ws.get_objects2.side_effect = None
        ret = impl.modelcompound_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self._validate_features('modelcompound_schema.json', ret[0], [])
        ret = impl.modelreaction_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self._validate_features('modelreaction_schema.json', ret[0], [])
        ret = impl.modelreactionproteinsubunit_index(self.getContext(), params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        schema_file = 'modelreactionproteinsubunit_schema.json'
        self._validate_features(schema_file, ret[0], [])
