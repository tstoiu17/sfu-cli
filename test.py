params = {    
    'base': '?'
    'year': '2022', # returns list
    'term': 'fall', # returns list
    'department': 'cmpt', # returns list
    'courseNumber': '120', # returns list
    'courseSection': 'd100', # returns dict
}


exit()
base_url = f'http://www.sfu.ca/bin/wcm/course-outlines'
req_url = base_url 
#os.system('clear')
for k, v in params.items():
    req_url = f'{req_url}{v}/'
    print(f'Requesting url: {req_url}')
    r = requests.get(req_url)
    json_res = json.loads(r.text)
    json_fmt = json.dumps(json_res, indent=4)
    if isinstance(json_res, list):
        #keys = json_res[0].keys()
        #print(*keys, sep='\n')
        jsonf = json.dumps(json_res[0], indent=4)
        print(jsonf)
    if isinstance(json_res, dict):
        print(*json_res.keys(), sep='\n')
    #input('Press enter...')
    #print(f'len: {len(json_res)}')
    #input('Press enter...')
    #print(80*'-')
    #print(json_fmt)
    #print(80*'-')
    #input('Press enter...')
    #os.system('clear')

exit()

test_url = f'http://www.sfu.ca/bin/wcm/course-outlines?{year}{term}{department}{courseNumber}{courseSection}'
json_res = json.loads(r.text)
print(type(json_res))

