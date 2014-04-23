import requests
from pattern import web
from Strategy import AbstractStrategy
from HTMLParser import HTMLParser
import re

class Game(object):
    # Takes in a string (url of the unprettified log), and a strategy class
    def __init__(self, log_url, strategy_class):
        if not issubclass(strategy_class, AbstractStrategy):
            raise Exception('strategy_class must inherit from AbstractStrategy')
        # The URL of the (unprettified) log
        self.log_url = log_url
        
        # The log as a block of text
        self.raw_log = self.get_raw_log()
        
        # The log itself, split by lines
        self.log = self.get_log()
        
        # e.g. [u'1st place: Perry Green', u'2nd place: Stef']
        self.standing = self.get_standing()
        
        # The names of the players. If there is a winner, p1 is the winner
        self.p1, self.p2 = self.get_players()
        
        # The name of the winner, or 'Tie'
        self.winner = self.get_winner()
        
        # HTML for kingdom (pictures in a grid)
        self.kingdom_html = self.get_kingdom_html()
        
        # List of cards in the supply
        self.supply = self.get_supply()
        
        # If there is a bane, the name of the bane card. None otherwise
        self.bane = self.get_bane()
        
        # Bool: true if shelters
        self.shelters = self.has_shelters()
        
        # Bool: true if colonies
        self.colonies = self.has_colonies()
        
        # The players respective strategies
        self.p1_strat, self.p2_strat = strategy_class(self, self.p1), strategy_class(self, self.p2)
    
    def get_raw_log(self):
        return web.Element(requests.get(self.log_url).text).content
    
    def get_log(self):
        return self.raw_log.split('\n')
    
    def get_standing(self):
        return self.log[-3:-1]
    
    def get_players(self):
        return map(lambda x: x[11:], self.standing)
    
    def get_winner(self):
        if self.standing[1][0] == '1':
            return 'Tie'
        return self.p1
    
    def get_kingdom_html(self):
        h = HTMLParser()
        url = "http://gokologs.drunkensailor.org/kingdom?logurl=%s" % self.log_url
        return re.sub('\n', '', h.unescape(web.Element(requests.get(url).text).by_tag('textarea')[-1].content))
    
    def get_supply(self):
        return self.log[1][14:].split(', ')
    
    def get_bane(self):
        if self.log[2][:4] == 'Bane':
            return self.log[2][11:]
        return None
    
    def has_shelters(self):
        return 'Hovel' in self.supply
    
    def has_colonies(self):
        return 'Colony' in self.supply
