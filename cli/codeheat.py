# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from github import Github
import github3
import os, sys, argparse, textwrap, requests, datetime, operator

"""CODEHEAT RUNS FROM SEPTEMBER 10TH, 2018 TO FEBRUARY 1ST, 2019"""
now = datetime.datetime.now()
CODEHEAT_START, CODEHEAT_END = datetime.datetime(now.year, 9, 10), datetime.datetime(now.year + 1, 2, 1)

ORG_NAME = 'fossasia'
REPOS =  [["connfa-android", "open-event-wsgen", "open-event-frontend", "open-event-organizer-android", "open-event-attendee-android", "open-event-ios", "open-event-legacy", "open-event-scraper", "open-event-server", "open-event-orga-iOS", "open-event-theme", "event-collect", "open-event-droidgen", "open-event"],
         ['pslab-desktop', 'pslab-android', 'pslab-python', 'pslab-firmware', 'pslab.io', 'pslab-webapp', 'pslab-hardware', 'pslab-documentation', 'pslab-case', 'pslab-expeyes', 'pslab-artwork', 'pslab-iOS', 'in.pslab.io', 'jp.pslab.io'],
         ["meilix.org", "meilix-systemlock", "meilix-artwork", "meilix-generator", "meilix"], ["phimpme-android"], ["susper.com"], ["badge-magic-android", "badgeyay"], ["yaydoc"]]

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
    if username == "" or password == "":
        return False
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
    g3 = github3.login(token=access_token) 
    print('\n')
elif bools.creds == True:
    print("[*] Credentials param was selected ...")
    print("[*] Enter your Github credentials ...\n")
    creds = prompt(popauth)
    gbool = validate(creds['username'], creds['password'])
    if gbool == True:
        g = Github(creds['username'], creds['password'])
        g3 = github3.login(creds['username'], password=creds['password'])
        print("[+] Login successful, Github instance correctly initialized.")
    else:
        print("[!] Wrong credentials, exiting ...")
        sys.exit(1)
    print('\n')
else:
    print("No parameter was provided (use [-h] flag for help), exiting ...")
    sys.exit(1)

def ccontributors(data): # current year's contributors, func:tested
    codeheat_contrib = []
    for prop in data:
        try:
            cname, date = prop
            if CODEHEAT_START < date < CODEHEAT_START:
                 codeheat_contrib.append(prop)
        except:
            codeheat_contrib.append(prop) # appends seperators, eg. meilix ...
            pass
    return codeheat_contrib

def get_status(uname, data): # func:tested
    counter = 0
    for prop in data:
        try:
            cname, date = prop
            if cname == uname:  # BUG : username and name compare, will not work
                 counter += 1
        except:
            print("%s contributions in %s\n\n" % (counter, prop))
            counter = 0
            pass

def handle(answers, g):
    main, sub = answers['init'], answers['opts']
    if main == 'My status':
        get_status(creds['username'], curr_contrib)
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

def worker(g, org, repos):
    authors = []
    for repo in repos:
        for r in repo:
            repo = g.get_organization(org).get_repo(r)
            for commit in repo.get_commits():
                authors.append((commit.commit.author.name, commit.commit.author.date))
    return authors

if CODEHEAT_START < datetime.datetime(now.year, now.month, now.day) < CODEHEAT_START:
    answers = prompt(questions)
    all_contributors = worker(g, ORG, REPOS[2]) + ['meilix'] + worker(g, ORG, REPOS[0]) + ['open_event'] + worker(g, ORG, REPOS[1]) + ['pslab'] + worker(g, ORG, REPOS[3]) + ['phimpme'] + worker(g, ORG, REPOS[4]) + ['susper'] + worker(g, ORG, REPOS[5]) + ['badgeyay'] + worker(g, ORG, REPOS[6]) + ['yaydoc']
    # meilix, openevent, pslab, phimpme, susper, badgeyay, yaydoc list
    curr_contrib = ccontributors(all_contributors) # format : [(contributor), (date), ..., 'repo', ...] if len(curr_contrib) == 7 : no contributors
    print("[*] Number of Requests : {}".format(g.ratelimit_remaining))
    handle(answers, g)
else:
    print("[-] Codeheat period has not started yet. Exiting.")
    sys.exit(1)