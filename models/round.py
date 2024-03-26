import copy

class Round:
    def __init__(self, id, players, quests) -> None:
        self.id = id
        self.players = copy.deepcopy(players)
        self.quests =  copy.deepcopy(quests)
        
    def __repr__(self): 
        return "\n{id:%s, \nplayers:%s, \nquests:%s}" % (self.id, self.players, self.quests ) 
    
    def __str__(self): 
        return "{id:%s, \nplayers:%s, \nquests:%s}" % (self.id, self.players, self.quests ) 