# Special Indexer for Narrative Objects
import json
import os
from hashlib import sha224

from Utils.WorkspaceAdminUtils import WorkspaceAdminUtils


class ModelIndexer:
    def __init__(self, config):
        self.ws = WorkspaceAdminUtils(config)
        self.schema_dir = config['schema-dir']

    def _tf(self, val):
        if val == 0:
            return False
        else:
            return True

    def _guid(self, upa):
        (wsid, objid, ver) = upa.split('/')
        return f"WS:{wsid}:{objid}:{ver}"

    def media_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'mediacompounds': len(data['mediacompounds']),
               'Denfined': self._tf(data['isDefined']),
               'Minimal': self._tf(data['isMinimal']),
               'Aerobic': self._tf(data.get('isAerobic', False))}
        for k in ['id', 'name', 'external_source_id', 'type']:
            rec[k] = data.get(k, '')
        schema = self.mapping('media_schema.json')
        return {'data': rec, 'schema': schema}

    def media_compound_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'parent': {}}
        features_rec = []
        for feature in data['mediacompounds']:
            if 'id' in feature:
                _id = feature['id']
            else:
                _id = feature['compound_ref'].split('/')[-1]

            frec = {'id': _id,
                    'concentration': float(feature['concentration']),
                    'minFlux': float(feature['minFlux']),
                    'maxFlux': float(feature['maxFlux']),
                    'guid': f'{self._guid(upa)}:{_id}'}
            for k in ['compound_ref', 'name', 'inchikey']:
                frec[k] = feature.get(k)

            features_rec.append(frec)
        rec['features'] = features_rec
        rec['schema'] = self.mapping('media_compound_schema.json')
        return rec

    def fbamodel_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'modelcompartments': len(data['modelcompartments']),
               'modelcompounds': len(data['modelcompounds']),
               'modelreactions': len(data['modelreactions'])}
        for k in ['id', 'name', 'source', 'type']:
            rec[k] = data.get(k)
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
        rec = {'parent': {}}
        features_rec = []
        for feature in data['modelcompounds']:
            frec = {'inchikey': feature.get('inchikey', ''),
                    'guid': f'{self._guid(upa)}:{feature["id"]}'}
            for k in ['id', 'name', 'formula', 'aliases']:
                frec[k] = feature[k]
            features_rec.append(frec)

        rec['features'] = features_rec
        rec['schema'] = self.mapping('modelcompound_schema.json')
        return rec

    def modelreaction_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'parent': {}}
        features_rec = []
        for feature in data['modelreactions']:
            frec = {'pathway': feature.get('pathway', ''),
                    'guid': f'{self._guid(upa)}:{feature["id"]}'}
            for k in ['id', 'name', 'aliases']:
                frec[k] = feature[k]
            features_rec.append(frec)

        rec['features'] = features_rec
        rec['schema'] = self.mapping('modelreaction_schema.json')
        return rec

    def modelreactionproteinsubunit_index(self, upa):
        obj = self.ws.get_objects2({'objects': [{'ref': upa}]})['data'][0]
        data = obj['data']
        rec = {'parent': {}}
        features_rec = []
        for reactions in data['modelreactions']:
            for proteins in reactions['modelReactionProteins']:
                for sub in proteins['modelReactionProteinSubunits']:
                    frec = {}
                    for k in ['role', 'feature_refs']:
                        frec[k] = sub[k]
                    _id = f'{reactions["id"]}:{proteins["complex_ref"]}:{sub["role"]}'
                    h = sha224(_id.encode('utf-8')).hexdigest()
                    frec['guid'] = f'{self._guid(upa)}:{h}'
                    features_rec.append(frec)
        rec['features'] = features_rec
        rec['schema'] = self.mapping('modelreactionproteinsubunit_schema.json')
        return rec

    def mapping(self, filename):
        with open(os.path.join(self.schema_dir, filename)) as f:
            schema = json.loads(f.read())
        return schema['schema']
