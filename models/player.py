class Player:
    def __init__(self, id, personality = None, idleCount = 0) -> None:
        self.id = id
        self.idleCount = idleCount
        self.personality = personality
        self.choice = None
        self.quests = []
        
    def __repr__(self): 
        return "\n{id:%s, idleCount:%s, personality:%s}" % (self.id, self.idleCount, self.personality ) 
    
    def __str__(self): 
        return "{id:%s, idleCount:%s, personality:%s}" % (self.id, self.idleCount, self.personality ) 

    def accept(self, quest):
        quest.players.append(self)
        self.quests.append(quest)
        self.idleCount = 0

    def submit(self):
        self.quests = []
        self.idleCount = 0

    def idle(self):
        self.idleCount += 1

