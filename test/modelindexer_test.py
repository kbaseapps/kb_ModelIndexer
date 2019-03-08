# -*- coding: utf-8 -*-
import json  # noqa: F401
import os  # noqa: F401
import time
import unittest
from configparser import ConfigParser  # py3
from os import environ
from unittest.mock import patch

from Utils.ModelIndexer import ModelIndexer
from installed_clients.WorkspaceClient import Workspace as workspaceService


class ModelIndexerTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_ModelIndexer'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        # authServiceUrl = cls.cfg['auth-service-url']
        # auth_client = _KBaseAuth(authServiceUrl)
        # user_id = auth_client.get_user(cls.token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.scratch = cls.cfg['scratch']
        cls.cfg['token'] = cls.token
        cls.upa = '1/2/3'
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
        wsName = "test_ModelIndexer_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    @patch('Utils.ModelIndexer.WorkspaceAdminUtils', autospec=True)
    def index_media_test(self, mock_wsa):
        iu = ModelIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.mediaobj
        res = iu.media_index(self.upa)
        self.assertIsNotNone(res)
        res = iu.media_compound_index(self.upa)
        self.assertIsNotNone(res)

    @patch('Utils.ModelIndexer.WorkspaceAdminUtils', autospec=True)
    def index_model_test(self, mock_wsa):
        iu = ModelIndexer(self.cfg)
        iu.ws.get_objects2.return_value = self.fbamodelobj
        res = iu.modelcompound_index(self.upa)
        self.assertIsNotNone(res)
        res = iu.modelreaction_index(self.upa)
        self.assertIsNotNone(res)
        res = iu.modelreactionproteinsubunit_index(self.upa)
        self.assertIsNotNone(res)

    @patch('Utils.ModelIndexer.WorkspaceAdminUtils', autospec=True)
    def index_fbamodel_test(self, mock_wsa):
        iu = ModelIndexer(self.cfg)
        iu.ws.get_objects2.side_effect = [self.fbamodelobj, self.gensubobj]
        res = iu.fbamodel_index(self.upa)
        self.assertIsNotNone(res)
