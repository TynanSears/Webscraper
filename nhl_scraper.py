"""
Web scraping tool to get fantasy players and stats*

References: https://realpython.com/python-web-scraping-practical-introduction/
            https://html.python-requests.org/
"""

import requests
from lxml import html
from requests_html import HTMLSession 
import json
import time

# class NHLScraper():
#     def __init__(self):
#         self.get_teams()

session = requests.session()
teams_list = []

def get_page(url):
    try:
        response = session.get(url)  
        with response as resp:
            if is_good_response(resp):
                return resp
            else: 
                return None

            response.close()
            print(response.closed())

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def get_teams(url):
    teams_page_response = get_page(url)
    print('Ye')
    team_tree = html.fromstring(teams_page_response.content)
    teams = team_tree.find_class('team-name')

    for team in teams:
        teams_list.append(team.text_content().lower().replace(" ", "")) # append team names to list, ensure names are lowercase and have no spaces
    
    print(teams_list)

def get_team_rosters():
    team_url_list = []
    all_team_rosters = []
    # Make list of team urls
    for team in teams_list:
        url = 'https://www.nhl.com/' + team + "/roster"
        team_url_list.append(url)
    # 
    for url in team_url_list:
        team_roster = []
        team = url.split("/")[3].upper()
        team_roster_response = get_page(url)
        roster_tree = html.fromstring(team_roster_response.content)
        
        first_names = roster_tree.find_class('name-col__firstName')
        last_names = roster_tree.find_class('name-col__lastName')

        for i in range(len(first_names)):
            full_name = first_names[i].text_content() + " " + last_names[i].text_content()
            team_roster.append(full_name)

        all_team_rosters.append({
            "team": team,
            "roster": team_roster
        })

    print(json.dumps(all_team_rosters, indent=4))
    
get_teams("https://www.nhl.com/info/teams")
get_team_rosters()


# x = NHLScraper()
# x.get_teams("https://www.nhl.com/info/teams")