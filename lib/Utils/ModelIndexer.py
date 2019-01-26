# Special Indexer for Narrative Objects
from Utils.WorkspaceAdminUtils import WorkspaceAdminUtils
import json
import os
from hashlib import sha224


class ModelIndexer:
    def __init__(self, config):
        self.ws = WorkspaceAdminUtils(config)
        ldir = os.path.dirname(os.path.abspath(__file__))
        self.schema_dir = '/'.join(ldir.split('/')[0:-2])

    def _tf(self, val):
        if val == 0:
            return False
        else:
            return True

    def _guid(self, upa):
        (wsid, objid, ver) = upa.split('/')
        return "WS:%s:%s:%s" % (wsid, objid, ver)

    def media_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        for k in ['id', 'name', 'external_source_id', 'type']:
            rec[k] = data.get(k, '')
        rec['mediacompounds'] = len(data['mediacompounds'])
        rec['Denfined'] = self._tf(data['isDefined'])
        rec['Minimal'] = self._tf(data['isMinimal'])
        rec['Aerobic'] = self._tf(data.get('isAerobic', False))
        schema = self.mapping('media_schema.json')
        return {'data': rec, 'schema': schema}

    def media_compound_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {}
        rec['parent'] = {}
        features_rec = []
        for feature in data['mediacompounds']:
            frec = {}
            for k in ['compound_ref', 'name', 'inchikey']:
                frec[k] = feature.get(k)
            if 'id' in feature:
                id = feature['id']
            else:
                id = feature['compound_ref'].split('/')[-1]
            frec['id'] = id
            frec['concentration'] = float(feature['concentration'])
            frec['minFlux'] = float(feature['minFlux'])
            frec['maxFlux'] = float(feature['maxFlux'])
            frec['guid'] = '%s:%s' % (self._guid(upa), id)
            features_rec.append(frec)
            # "compound_ref": "6/4/1/compounds/id/cpd00244",
            # "concentration": 0.001,
            # "id": "cpd00244",
            # "inchikey": "",
            # "maxFlux": 100,
            # "minFlux": -100,
            # "name": "Ni2+",
            # "smiles": ""

        rec['features'] = features_rec
        rec['schema'] = self.mapping('media_compound_schema.json')
        return rec

    def fbamodel_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        for k in ['id', 'name', 'source', 'type']:
            rec[k] = data.get(k)
        rec['modelcompartments'] = len(data['modelcompartments'])
        rec['modelcompounds'] = len(data['modelcompounds'])
        rec['modelreactions'] = len(data['modelreactions'])
        # From genome genome_ref
        genome_ref = data['genome_ref']
        req = {'ref': genome_ref,
               'included': ['scientific_name', 'taxonomy', 'id']
               }
        gdata = self.ws.get_objects2({'objects': [req]})['data'][0]['data']
        rec['genome_guid'] = genome_ref
        rec['scientific_name'] = gdata['scientific_name']
        rec['taxonomy'] = gdata.get('taxonomy')
        rec['genome_name'] = gdata['id']
        schema = self.mapping('fbamodel_schema.json')
        return {'data': rec, 'schema': schema}

    def modelcompound_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['parent'] = {}
        features_rec = []
        for feature in data['modelcompounds']:
            frec = {}
            for k in ['id', 'name', 'formula', 'aliases']:
                frec[k] = feature[k]
            frec['inchikey'] = feature.get('inchikey', '')
            frec['guid'] = '%s:%s' % (self._guid(upa), feature['id'])
            features_rec.append(frec)

        rec['features'] = features_rec
        rec['schema'] = self.mapping('modelcompound_schema.json')

        return rec

    def modelreaction_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['parent'] = {}
        features_rec = []
        for feature in data['modelreactions']:
            frec = {}
            for k in ['id', 'name', 'aliases']:
                frec[k] = feature[k]
            frec['pathway'] = feature.get('pathway', '')
            frec['guid'] = '%s:%s' % (self._guid(upa), feature['id'])
            features_rec.append(frec)

        rec['features'] = features_rec
        rec['schema'] = self.mapping('modelreaction_schema.json')
        return rec

    def modelreactionproteinsubunit_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = dict()
        rec['parent'] = {}
        features_rec = []
        for reactions in data['modelreactions']:
            for proteins in reactions['modelReactionProteins']:
                for sub in proteins['modelReactionProteinSubunits']:
                    frec = {}
                    for k in ['role', 'feature_refs']:
                        frec[k] = sub[k]
                    id = '%s:%s:%s' % (reactions['id'],
                                       proteins['complex_ref'],
                                       sub['role'])
                    h = sha224(id.encode('utf-8')).hexdigest()
                    frec['guid'] = '%s:%s' % (self._guid(upa), h)
                    features_rec.append(frec)
        rec['features'] = features_rec
        rec['schema'] = self.mapping('modelreactionproteinsubunit_schema.json')
        return rec

    def mapping(self, filename):
        with open(os.path.join(self.schema_dir, filename)) as f:
            schema = json.loads(f.read())
        return schema['schema']
