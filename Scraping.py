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