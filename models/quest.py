class Quest:
    def __init__(self, id, isStory = None, requiredPlayerCount = None, personalities = None) -> None:
        self.id = id
        self.isStory = isStory if isStory is not None else False
        self.requiredPlayerCount = requiredPlayerCount if requiredPlayerCount is not None else 1
        self.personalities = personalities if personalities is not None else [] 
        self.totalCompletionsCount = 0
        self.players = []
        self.totalPlayersCount = 0

    def __repr__(self): 
        return "\n{id:%s, isStory:%s, requiredPlayerCount:%s, completionsCount:%s, \n\tpersonalities:%s, \n\tplayers:%s}" % (self.id, self.isStory, self.requiredPlayerCount, self.totalCompletionsCount, [p.id for p in self.personalities], [p.id for p in self.players]) 
    
    def __str__(self): 
        return "{id:%s, isStory:%s, requiredPlayerCount:%s, completionsCount:%s, \n\tpersonalities:%s, \n\tplayers:%s}" % (self.id, self.isStory, self.requiredPlayerCount, self.totalCompletionsCount, [p.id for p in self.personalities], [p.id for p in self.players] ) 
        
    def canComplete(self):
        return  len(self.players) >= self.requiredPlayerCount

    def submitForAllPlayers(self):
        self.totalCompletionsCount += 1
        self.totalPlayersCount += len(self.players)
        for p in self.players:
            p.submit()

        self.players = []
