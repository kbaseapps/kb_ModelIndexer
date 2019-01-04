from Workspace.WorkspaceClient import Workspace
import json

ws = Workspace('https://ci.kbase.us/services/ws')

upa = '36815/4/1'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/media_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))

upa = '33192/10/1'
upa = '17335/21/2'
d = ws.get_objects2({'objects': [{'ref': upa}]})
with open('./test/mock_data/fbamodel_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))

upa = '16174/15/1'
l = [ 'scientific_name', 'taxonomy', 'id' ]
d = ws.get_objects2({'objects': [{'ref': upa, 'included': l}]})
with open('./test/mock_data/genome_sub_object.json', 'w') as f:
    f.write(json.dumps(d, indent=2))
