import requests
import json
import os


def display_options(options):
    """Print the options dictionary with styling using ANSI escape codes"""
    escape_code = '\u001b[{}m'
    fg_red_bold = escape_code.format('31;1')
    fg_blue_bold = escape_code.format('34;1')
    reset = escape_code.format('0')

    for k, v in options.items():
        if k == 'q' or k == 'r':
            print(fg_red_bold, end='')
        else:
            print(fg_blue_bold, end='')
        print(f'({k}) {v}')
        print(reset, end='')


base_url = f'http://www.sfu.ca/bin/wcm/course-outlines?'
req_url = base_url
params = []
level = 0
"""Levels
0: base
1: year
2: term
3: dept
4: course
5: sect (we'll stop at the course section details)
"""
quit = False
while level < 5 and not quit:
    os.system('clear')

    # create request
    query = "/".join(params)
    req_url = f'{base_url}{query}'
    r = requests.get(req_url)
    print(f'{level}: Requesting /{query}')

    # get json of response
    j = r.json()
    # display options
    options = {str(i): obj['text'] for i, obj in enumerate(j)}
    # TODO: include these options for choosing year and term
    """
    # dyanmic variable parameters
    options['c'] = 'current'
    options['r'] = 'registration'
    """
    options['q'] = 'quit'
    options['r'] = 'restart'
    display_options(options)
    # prompt for choice
    invalid = True
    while invalid:
        choice = input('> ').strip()
        level += 1

        # check if choice is valid
        if choice in options:
            invalid = False
            if choice == 'q':
                quit = True
            if choice == 'r':
                params.clear()
                level = 0
            else: # update params with choice
                params.append(j[int(choice)]['value'])
        else:
            print('Invalid choice entered')


os.system('clear')
query = "/".join(params)
req_url = f'{base_url}{query}'
r = requests.get(req_url)
print(f'{level}: Requesting /{query}')
j = json.loads(r.text)
print(json.dumps(j, indent=4))
