from datetime import datetime

import requests
from bs4 import BeautifulSoup


def get_matches(team_name: str):
    url = f'https://en.game-tournaments.com/dota-2/team/{team_name.replace(" ", "-")}'
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                      'Safari/537.36 '
    }

    req = requests.get(url, headers=headers)
    if req.status_code == 404:
        return None

    soup = BeautifulSoup(req.text, 'lxml')
    block_matches_current = soup.find('div', id='block_matches_current')
    if block_matches_current is None:
        return None

    matches = block_matches_current.findAll('tr')
    result = []
    for m in matches:
        columns = m.findAll('td')
        link = 'https://en.game-tournaments.com' + columns[1].find('a')['href']
        title = columns[1].find('a')['title']
        event_date = columns[2].findAll('span')[1].find('span').text
        try:
            event_date = datetime.strptime(event_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            event_date = datetime.now()

        match = {
            'team_name': team_name,
            'link': link,
            'title': title,
            'event_date': event_date,
        }
        result.append(match)

    return result
