from app import mongo


class Role:
    def __init__(self, name):
        self.name = name

    def save(self):
        db = mongo.db
        db.roles.insert_one({
            'name': self.name
        })
        
    def get_role_by_name(name):
        db = mongo.db
        role = db.roles.find_one({'name': name})
        return role
