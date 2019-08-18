# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from github import Github
import sys

popauth = [
    {
        'type': 'input',
        'name': 'username',
        'message': 'Enter your Github username : '
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Enter your Github password : '
    }
]

"""
if not provided on command line args :
fallback()
"""
creds = prompt(popauth)
print(creds['password'], creds['username'])

def handle(answers):
    main, sub = answers['init'], answers['opts']
    if main == 'My status':
        get_status()
    elif main == 'Top contributors':
        if sub == 'Overall':
            top_contributors(opt)
        else:
            top_contributors(opt)
    elif main == 'Active maintainers':
        if sub == 'Overall':
            active_maintainers(opt)
        else:
            active_maintainers(opt)
    elif main == 'Insights':
        get_insights()


def options(answers):
    options = []
    if answers['init'] == 'My status':
        print('Are you sure to continue ?')
        options.extend(['Yes', 'No'])
    elif answers['init'] == 'Top contributors':
        options.extend(['Overall', 'By project'])
    elif answers['init'] == 'Active maintainers':
        options.extend(['Overall', 'By project'])
    elif answers['init'] == 'Insights':
        print('Are you sure to continue ?')
        options.extend(['Yes', 'No'])
    return options


questions = [
    {
        'type': 'list',
        'name': 'init',
        'message': 'Command-line tool for winning Codeheat',
        'choices': [
            'My status',
            'Top contributors',
            'Active maintainers',
            Separator(),
            'Insights',
            {
                'name': 'Fun facts',
                'disabled': 'Under construction at this time'
            }
        ]
    },
    {
        'type': 'rawlist',
        'name': 'opts',
        'message': '',
        'choices': options,
    },
]

answers = prompt(questions)
handle(answers)