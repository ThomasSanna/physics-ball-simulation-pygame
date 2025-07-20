class Entity:
    allEntities: list["Entity"] = []
    def __init__(self):
        Entity.allEntities.append(self)
        self.enabled = True

    def update(self, dt):
        pass
    def draw(self, surface):
        pass
    
    def disable(self):
        self.enabled = False
    