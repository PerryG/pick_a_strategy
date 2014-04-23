from pattern import web
import random
import requests
from game import Game
from strategy import OpeningStrategy

# Returns a list of the names of top n players
def top_n_players(n):
    leaderboard = web.Element(requests.get('http://gokologs.drunkensailor.org/leaderboard/').text)
    return [person.by_tag('td')[-1].content for person in leaderboard.by_tag('tr')[1:n+1]]

# Returns a list of links to most recent max_results logs of games between
# p1 and p2, or p1 and anyone if p2 is ''
def get_log_links(p1, p2 = '', max_results = 100):
    template = "http://gokologs.drunkensailor.org/logsearch?p1name=%s&p2name=%s&rating=pro&pcount=2&bot=false&submitted=true&limit=%d"
    url = template % (p1, p2, max_results)
    query = web.Element(requests.get(url).text)
    return [l.href for l in query.by_tag('a') if l.content == u'Log']

# Picks a random game between 2 players in the top n where players had
# different strategies according to strategy_class
def random_interesting_game(n, strategy_class):
    if not n >= 2:
        raise Exception('Must choose from at least 2 players')

	# pick 2 random players
    players = top_n_players(n)
    p1 = random.choice(players)
    p2 = None
    while p2 == None:
        p2 = random.choice(players)
        if p2 == p1:
            p2 = None

    # Get games for those players
    links = get_log_links(p1, p2)
    random.shuffle(links)
    found_game = False

	# See if any of the links are interesting
    for link in links:
        game = Game(link, strategy_class)
        if game.p1_strat != game.p2_strat:
            found_game = True
            break

    # If none are interesting, start over
    if not found_game:
        return random_interesting_game(n, strategy_class)

    return game

def game_page(game):
    template_file = open('template.html')
    template = template_file.read()
    template_file.close()
    bane_line = ''
    if game.bane:
        bane_line = 'Bane: %s' % game.bane
    return template % (game.kingdom_html, str(game.colonies), str(game.shelters), bane_line, game.p1_strat, game.p2_strat)

def main():
    game = random_interesting_game(100, OpeningStrategy)
    print game_page(game)


if __name__ == "__main__":
    main()
