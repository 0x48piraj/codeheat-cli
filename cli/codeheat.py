# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from github import Github
import os, sys, argparse, textwrap, requests, datetime

"""CODEHEAT RUNS FROM SEPTEMBER 10TH, 2018 TO FEBRUARY 1ST, 2019"""
now = datetime.datetime.now()
CODEHEAT_START, CODEHEAT_END = datetime.date(now.year, 9, 10), datetime.date(now.year + 1, 2, 1)

ORG_NAME = 'fossasia'
REPOS =  [["connfa-android", "open-event-wsgen", "open-event-frontend", "open-event-organizer-android", "open-event-attendee-android", "open-event-ios", "open-event-legacy", "open-event-scraper", "open-event-server", "open-event-orga-iOS", "open-event-theme", "event-collect", "open-event-droidgen", "open-event"],
         ['pslab-desktop', 'pslab-android', 'pslab-python', 'pslab-firmware', 'pslab.io', 'pslab-webapp', 'pslab-hardware', 'pslab-documentation', 'pslab-case', 'pslab-expeyes', 'pslab-artwork', 'pslab-iOS', 'in.pslab.io', 'jp.pslab.io'],
         ["meilix.org", "meilix-systemlock", "meilix-artwork", "meilix-generator", "meilix"], "phimpme-android", "susper.com", "badge-magic-android", "badgeyay", "yaydoc"]

banner = textwrap.dedent('''\
    .===================================================================.
    ||      codeheat-cli - Command-line tool for winning Codeheat      ||
    '==================================================================='
    ''')

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=banner)
optional = parser._action_groups.pop() # popped opt args
optional = parser.add_argument_group('Options')
optional.add_argument("-c", "--cred", dest="creds", action='store_true', help= "for providing Github credentials (username and password)")
optional.add_argument("-t", "--token", dest="token", action='store_true', help= "for providing Github Developer Token")
bools = parser.parse_args()
print(banner)

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

def validate(username, password):

    r = requests.get('https://api.github.com', auth=(username, password))
    if r.status_code == 200:
        return True
    else:
        return False

if bools.token == True:
    print("[*] Token param was selected ...")
    print("[*] Enter the Github dev token ...")
    access_token = input("    ----> ")
    g = Github(access_token) # try, catch
    print('\n')
elif bools.creds == True:
    print("[*] Credentials param was selected ...")
    print("[*] Enter your Github credentials ...\n")
    creds = prompt(popauth)
    gbool = validate(creds['username'], creds['password'])
    if gbool == True:
        g = Github(creds['username'], creds['password'])
        print("[+] Login successful, Github instance correctly initialized.")
    else:
        print("[!] Wrong credentials, exiting ...")
        sys.exit(1)
    print('\n')
else:
    print("No parameter was provided, exiting ...")
    sys.exit(1)


def get_status(ghwd):
    ghwd


def handle(answers, g):
    main, sub = answers['init'], answers['opts']
    if main == 'My status':
        get_status(g)
    elif main == 'Top contributors':
        if sub == 'Overall':
            top_contributors(g, opt)
        else:
            top_contributors(g, opt)
    elif main == 'Active maintainers':
        if sub == 'Overall':
            active_maintainers(g, opt)
        else:
            active_maintainers(g, opt)
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
        'message': 'Enter option : ',
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


if CODEHEAT_START < datetime.date(now.year, now.month, now.day) < CODEHEAT_START:
    answers = prompt(questions)
    RATE = g.ratelimit_remaining
    handle(answers, g)
else:
    print("[*] Codeheat period has not started yet. Exiting.")
    sys.exit(1)