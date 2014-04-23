from abc import ABCMeta 
from abc import abstractmethod

# Represents a players strategy during a single game
class AbstractStrategy(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self, game, player):
        pass
    
    @abstractmethod
    def __repr__(self):
        pass
    
    @abstractmethod
    def __eq__(self, other):
        pass
    
    def __ne__(self, other):
        return not self.__eq__(other)

# A players strategy is taken to be their buys during the first suffle
class OpeningStrategy(AbstractStrategy):
    
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.buys = self.get_opening_buys()
    
    def __eq__(self, other):
        return sorted(self.buys) == sorted(other.buys)
    
    def __repr__(self):
        return '/'.join(sorted(self.buys))
    
    def get_opening_buys(self):
        buys = []
        turns = 0
        i = 0
        try:
            while turns < 2:
                bought = False
                # Find the beginning of a turn
                while str(self.game.log[i]) != ('---------- %s: turn %d ----------' % (self.player, turns+1)):
                    i += 1
                # Find the buys. Note that nomad camp makes my life hard, since it is possible to get 3 buys
                i += 1
                while self.game.log[i][:10] != '----------':
                    i += 1
                    if self.game.log[i][:len(self.player)+8] == ('%s - buys ' % self.player):
                        buys.append(self.game.log[i][len(self.player)+8:])
                        bought = True
                if not bought:
                    buys.append('Nothing')
                turns += 1
            return buys

        except IndexError:
            print 'INDEX ERROR'
            return ['Nothing', 'Nothing']

