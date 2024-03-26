
import json
from models.personality import Personality as personality

class ConfigService:
    def __init__(self) -> None:
        with open('config/config.json') as config_file:
            data = json.load(config_file)
        
        self.questCount = data['quest_count']
        self.playerCount = data['player_count']
        self.personalities = []
        for idx, p in enumerate(data['personalities']):
            np = personality(idx, p['type'], p['description'])
            self.personalities.append(np)
