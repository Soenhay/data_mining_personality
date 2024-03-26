class Personality:
    def __init__(self, id, name, description) -> None:
        self.id = id
        self.name =  name
        self.description = description
        
    def __repr__(self): 
        return "\n{id:%s, name:%s, description:%s}" % (self.id, self.name, self.description ) 
    
    def __str__(self): 
        return "{id:%s, name:%s, description:%s}" % (self.id, self.name, self.description ) 

