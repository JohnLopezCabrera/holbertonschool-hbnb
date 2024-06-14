class Database:
    def __init__(self):
        self.users = {}
        self.places = {}
        self.reviews = {}
        self.amenities = {}
        self.next_id = 1

    def generate_id(self):
        id = self.next_id
        self.next_id += 1
        return id

