from Workspace.WorkspaceClient import Workspace
import json
import os


def grab(upa, file):
    if not os.path.exists(file):
        d = ws.get_objects2({'objects': [{'ref': upa}]})
        with open(file, 'w') as f:
            f.write(json.dumps(d, indent=4))


ws = Workspace('https://ci.kbase.us/services/ws')

grab('36815/4/1', './test/mock_data/media_object.json')

grab('17335/21/2', './test/mock_data/fbamodel_object.json')

grab('4/23/1', './test/mock_data/media2_object.json')


upa = '16174/15/1'
l = ['scientific_name', 'taxonomy', 'id']
fname = './test/mock_data/genome_sub_object.json'
if not os.path.exists(fname):
    d = ws.get_objects2({'objects': [{'ref': upa, 'included': l}]})
    with open(fname, 'w') as f:
        f.write(json.dumps(d, indent=2))
