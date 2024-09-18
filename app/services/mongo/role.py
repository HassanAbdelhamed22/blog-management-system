from flask_pymongo import PyMongo

class RoleService:
    def __init__(self, mongo: PyMongo):
        self.mongo = mongo

    def insert_roles(self):
        roles = ['admin', 'author', 'user']
        
        for role_name in roles:
            if not self.mongo.db.roles.find_one({'name': role_name}):
                new_role = {
                    'name': role_name
                }
                self.mongo.db.roles.insert_one(new_role)
                print(f'Inserted role: {role_name}')
