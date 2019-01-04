# -*- coding: utf-8 -*-
#BEGIN_HEADER
from Utils.ModelIndexer import ModelIndexer
#END_HEADER


class kb_ModelIndexer:
    '''
    Module Name:
    kb_ModelIndexer

    Module Description:
    A KBase module: kb_ModelIndexer
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "HEAD"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.shared_folder = config['scratch']
        self.wsa_token = None
        self.wsa_token = config.get('workspace-admin-token', None)
        self.indexer = ModelIndexer(config)
        #END_CONSTRUCTOR
        pass


    def fbamodel_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN fbamodel_index
        output = self.indexer.fbamodel_index(params['upa'])
        #END fbamodel_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method fbamodel_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def fbamodel_mapping(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN fbamodel_mapping
        output = self.indexer.mapping('fbamodel_schema.json')
        #END fbamodel_mapping

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method fbamodel_mapping return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def media_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN media_index
        output = self.indexer.media_index(params['upa'])
        #END media_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method media_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def media_mapping(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN media_mapping
        output = self.indexer.mapping('media_schema.json')
        #END media_mapping

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method media_mapping return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def media_compound_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN media_compound_index
        output = self.indexer.media_compound_index(params['upa'])
        #END media_compound_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method media_compound_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def media_compound_mapping(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN media_compound_mapping
        output = self.indexer.mapping('media_compound_schema.json')
        #END media_compound_mapping

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method media_compound_mapping return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def modelreaction_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN modelreaction_index
        output = self.indexer.modelreaction_index(params['upa'])
        #END modelreaction_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method modelreaction_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def modelreaction_mapping(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN modelreaction_mapping
        output = self.indexer.mapping('modelreaction_schema.json')
        #END modelreaction_mapping

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method modelreaction_mapping return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def modelcompound_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN modelcompound_index
        output = self.indexer.modelcompound_index(params['upa'])
        #END modelcompound_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method modelcompound_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def modelcompound_mapping(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN modelcompound_mapping
        output = self.indexer.mapping('modelcompound_schema.json')
        #END modelcompound_mapping

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method modelcompound_mapping return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def modelreactionproteinsubunit_index(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN modelreactionproteinsubunit_index
        output = self.indexer.modelreactionproteinsubunit_index(params['upa'])
        #END modelreactionproteinsubunit_index

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method modelreactionproteinsubunit_index return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def modelreactionproteinsubunit_mapping(self, ctx, params):
        """
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "Results" -> structure: parameter
           "file_name" of String, parameter "index" of unspecified object
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN modelreactionproteinsubunit_mapping
        output = self.indexer.mapping('modelreaction_schema.json')
        #END modelreactionproteinsubunit_mapping

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method modelreactionproteinsubunit_mapping return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
