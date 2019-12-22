# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from github import Github
import github3, webbrowser
import os, sys, argparse, textwrap, requests, datetime, operator
from threading import Thread

"""CODEHEAT RUNS FROM SEPTEMBER 15, 2019 TO FEBRUARY 2, 2020"""
now = datetime.datetime.now()
CODEHEAT_START, CODEHEAT_END = datetime.datetime(now.year, 9, 15), datetime.datetime(now.year + 1, 2, 2)

ORG_NAME = 'fossasia'

# ORDER: open-event, pslab, meilix, phimpme, susper, badgeyay, yaydoc
REPOS =  [["open-event-wsgen", "open-event-frontend", "open-event-organizer-android", "open-event-attendee-android", "open-event-ios", "open-event-legacy", "open-event-scraper", "open-event-server", "open-event-orga-iOS", "open-event-theme", "event-collect", "open-event-droidgen", "open-event"],
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
optional.add_argument("-c", "--cred", dest="creds", action='store_true', help= "for providing Github credentials")
optional.add_argument("-t", "--token", dest="token", action='store_true', help= "for providing Github Developer Token")
bools = parser.parse_args()
print(banner)


class retCThread(Thread): # https://stackoverflow.com/a/6894023
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


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

def options(answers):
    options = []
    mappings = {'Scrum Helper':['Visit Project', 'No'], 'Insights':['Yes', 'No'], 'My status':['Yes', 'No'], 'Top contributors':['Overall', 'By project'], 'Active maintainers':['Overall', 'By project']}
    options.extend(mappings[answers['init']])
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
            'Scrum Helper',
            {
                'name': 'Automatically put together Scrums based on your GitHub contributions',
                'disabled': 'https://github.com/fossasia/scrum_helper'
            },
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

def validate(username, password):
    if not username or not password:
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
        print("[+] Login successful")
        print("[+] Github instance correctly initialized.")
    else:
        print("[!] Wrong credentials, exiting ...")
        sys.exit(1)
    print('\n')
else:
    print("No parameter was provided (use [-h] flag for help), exiting ...")
    sys.exit(1)


def handle(answers, g):
    if answers['init'] == 'My status':
        get_status(g.get_user().login, curr_contrib)
    elif answers['init'] == 'Top contributors':
        if answers['opts'] == 'Overall':
            top_contributors(g, opt)
        else:
            top_contributors(g, opt)
    elif answers['init'] == 'Active maintainers':
        if answers['opts'] == 'Overall':
            active_maintainers(g, opt)
        else:
            active_maintainers(g, opt)
    elif answers['init'] == 'Insights':
        get_insights(JSON)
    elif answers['init'] == 'Scrum Helper' and answers['opts'] == 'Visit Project':
        webbrowser.open('https://github.com/fossasia/scrum_helper')

# https://developer.github.com/v3/repos/statistics/

#def get_insights(json):
    # json that has data of 2018, 2017, 2016, etc.

# curl -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/git/git/commits?sha=master&since=2019-03-18T11:00:00Z
# `since` and `until`
def ccontributors(data): # current year's contributors, func:tested
    codeheat_contrib = []
    for prop in data:
        try:
            cname, date = prop
            #date = date.replace(second=0, microsecond=0, minute=0, hour=0)
            if CODEHEAT_START < date < CODEHEAT_END:
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
            if cname == uname:
                 counter += 1
        except:
            print("%s contributions in %s\n\n" % (counter, prop))
            counter = 0
            pass

def total_commits(handler, org, repos):
    authors = []
    for repo in repos:
        repo = handler.get_organization(org).get_repo(repo)
        for commit in repo.get_commits():
            authors.append((commit.commit.author.name, commit.commit.author.date))
    return authors

if CODEHEAT_START < datetime.datetime(now.year, now.month, now.day) < CODEHEAT_END:
    t1 = retCThread(target=total_commits, args=(g, ORG_NAME, REPOS[0],))
    t1.start()
    t2 = retCThread(target=total_commits, args=(g, ORG_NAME, REPOS[1],))
    t2.start()
    t3 = retCThread(target=total_commits, args=(g, ORG_NAME, REPOS[2],))
    t3.start()
    t4 = retCThread(target=total_commits, args=(g, ORG_NAME, REPOS[3],))
    t4.start()
    t5 = retCThread(target=total_commits, args=(g, ORG_NAME, REPOS[4],))
    t5.start()
    t6 = retCThread(target=total_commits, args=(g, ORG_NAME, REPOS[5],))
    t6.start()
    t7 = retCThread(target=total_commits, args=(g, ORG_NAME, REPOS[6],))
    t7.start()
    answers = prompt(questions)
    # handle(answers, g)
    
    # Loading bar until all threads finished, progressbar()
    # wait till all data gets fetched, if t1.is_alive()
    print("[*] Grabbing, please wait.")    
    data = { "openevent":t1.join(), "pslab":t2.join(), "meilix":t3.join(), "phimpme":t4.join(), "susper":t5.join(), "badgeyay":t6.join(), "yaydoc":t7.join() }
    # saving the data for time being
    f = open("data", "w")
    f.write(data)
    f.close()
    # CHECK THE DATA/DATA AND SHOW THE RESULTS
    # all_contributors = worker(g, ORG_NAME, REPOS[2]) + ['meilix'] + worker(g, ORG_NAME, REPOS[0]) + ['open_event'] + worker(g, ORG_NAME, REPOS[1]) + ['pslab'] + worker(g, ORG_NAME, REPOS[3]) + ['phimpme'] + worker(g, ORG_NAME, REPOS[4]) + ['susper'] + worker(g, ORG_NAME, REPOS[5]) + ['badgeyay'] + worker(g, ORG_NAME, REPOS[6]) + ['yaydoc']
    all_contributors = data['openevent'] + data['pslab'] + data['meilix'] + data['phimpme'] + data['susper'] + data['badgeyay'] + data['yaydoc']
    curr_contrib = ccontributors(all_contributors) # format : [(contributor), (date), ..., 'repo', ...] if len(curr_contrib) == 7 : no contributors
    print("[*] Number of Requests : {}".format(g.ratelimit_remaining))
    handle(answers, g)
else:
    print("[-] Codeheat period has not started yet. Exiting.")
    sys.exit(1)