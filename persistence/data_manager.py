# data_manager.py
from persistence_interface import IPersistenceManager

class DataManager(IPersistenceManager):
    def __init__(self):
        self.storage = {
            'User': {},
            'Place': {},
            'Review': {}
        }
        self.next_id = {
            'User': 1,
            'Place': 1,
            'Review': 1
        }

    def save(self, entity):
        entity_type = type(entity).__name__
        entity_id = self.next_id[entity_type]
        entity.id = entity_id  # Assuming each entity has an id attribute
        self.storage[entity_type][entity_id] = entity
        self.next_id[entity_type] += 1
        return entity

    def get(self, entity_id, entity_type):
        return self.storage[entity_type].get(entity_id)

    def update(self, entity):
        entity_type = type(entity).__name__
        if entity.id in self.storage[entity_type]:
            self.storage[entity_type][entity.id] = entity
            return entity
        else:
            raise ValueError(f"{entity_type} with ID {entity.id} not found.")

    def delete(self, entity_id, entity_type):
        if entity_id in self.storage[entity_type]:
            del self.storage[entity_type][entity_id]
        else:
            raise ValueError(f"{entity_type} with ID {entity_id} not found.")
