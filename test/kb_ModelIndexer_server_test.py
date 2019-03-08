# -*- coding: utf-8 -*-
import json
import os
import unittest
from configparser import ConfigParser
from unittest.mock import Mock

from installed_clients.WorkspaceClient import Workspace
from kb_ModelIndexer.kb_ModelIndexerImpl import kb_ModelIndexer
from kb_ModelIndexer.kb_ModelIndexerServer import MethodContext


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
        cls.schema_dir = cls.cfg['schema-dir']
        cls.params = {'upa': '1/2/3'}
        cls.serviceImpl.indexer.ws.get_objects2 = Mock()

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

    def _validate(self, sfile, data):
        with open(os.path.join(self.schema_dir, sfile)) as f:
            d = f.read()

        schema = json.loads(d)
        for key in schema['schema'].keys():
            self.assertIn(key, data)

    def _validate_features(self, sfile, data, plist):
        with open(os.path.join(self.schema_dir, sfile)) as f:
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
    def test_media_index_1(self):
        self.serviceImpl.indexer.ws.get_objects2.return_value = self.mediaobj
        self.serviceImpl.indexer.ws.get_objects2.side_effect = None
        ret = self.serviceImpl.media_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('media_schema.json', ret[0]['data'])
        ret = self.serviceImpl.media_compound_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self.assertIn('schema', ret[0])
        self._validate_features('media_compound_schema.json', ret[0], [])

    def test_media_index_2(self):
        m2 = self.read_mock('media2_object.json')
        self.serviceImpl.indexer.ws.get_objects2.return_value = m2
        self.serviceImpl.indexer.ws.get_objects2.side_effect = None
        ret = self.serviceImpl.media_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('media_schema.json', ret[0]['data'])
        ret = self.serviceImpl.media_compound_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self.assertIn('schema', ret[0])
        self._validate_features('media_compound_schema.json', ret[0], [])

    def test_fbamodel_index(self):
        self.serviceImpl.indexer.ws.get_objects2.return_value = self.fbamodelobj
        self.serviceImpl.indexer.ws.get_objects2.side_effect = [self.fbamodelobj, self.gensubobj]
        ret = self.serviceImpl.fbamodel_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('data', ret[0])
        self.assertIn('schema', ret[0])
        self._validate('fbamodel_schema.json', ret[0]['data'])

    def test_modelcompound_index(self):
        self.serviceImpl.indexer.ws.get_objects2.return_value = self.fbamodelobj
        self.serviceImpl.indexer.ws.get_objects2.side_effect = None
        ret = self.serviceImpl.modelcompound_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self.assertIn('schema', ret[0])
        self._validate_features('modelcompound_schema.json', ret[0], [])

    def test_modelreaction_index(self):
        self.serviceImpl.indexer.ws.get_objects2.return_value = self.fbamodelobj
        self.serviceImpl.indexer.ws.get_objects2.side_effect = None
        ret = self.serviceImpl.modelreaction_index(self.ctx, self.params)
        self.serviceImpl.indexer.ws.get_objects2.side_effect = None
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self.assertIn('schema', ret[0])
        self._validate_features('modelreaction_schema.json', ret[0], [])

    def test_modelreactionproteinsubunit_index(self):
        self.serviceImpl.indexer.ws.get_objects2.return_value = self.fbamodelobj
        self.serviceImpl.indexer.ws.get_objects2.side_effect = None
        ret = self.serviceImpl.modelreactionproteinsubunit_index(self.ctx, self.params)
        self.assertIsNotNone(ret[0])
        self.assertIn('features', ret[0])
        self.assertIn('schema', ret[0])
        schema_file = 'modelreactionproteinsubunit_schema.json'
        self._validate_features(schema_file, ret[0], [])
