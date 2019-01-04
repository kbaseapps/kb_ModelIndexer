/*
A KBase module: kb_ModelIndexer
*/

module kb_ModelIndexer {
    typedef structure {
        string file_name;
        UnspecifiedObject index;
    } Results;

    funcdef fbamodel_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef fbamodel_mapping(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef media_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef media_mapping(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef media_compound_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef media_compound_mapping(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef modelreaction_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef modelreaction_mapping(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef modelcompound_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef modelcompound_mapping(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef modelreactionproteinsubunit_index(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

    funcdef modelreactionproteinsubunit_mapping(mapping<string,UnspecifiedObject> params) returns (Results output) authentication required;

};
