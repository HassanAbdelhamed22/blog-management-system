from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from bson.objectid import ObjectId

class UserService:
    def __init__(self, mongo: PyMongo):
        self.mongo = mongo

    def login(self, username, password):
        user = self.mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password_hash'], password):
            login_user(user)
            return True
        return False

    def register(self, username, email, password):
        user = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password),
            'role_id': ObjectId(self.mongo.db.roles.find_one({'name': 'user'})['_id'])
        }
        result = self.mongo.db.users.insert_one(user)
        return self.mongo.db.users.find_one({'_id': result.inserted_id})

    def username_exists(self, username: str) -> bool:
        return self.mongo.db.users.find_one({'username': username}) is not None

    def email_exists(self, email: str) -> bool:
        return self.mongo.db.users.find_one({'email': email}) is not None
    
    def get_user(self, user_id):
        return self.mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    def get_all_users(self):
        return list(self.mongo.db.users.find())
    
    def get_user_role(self, user_id):
        user = self.get_user(user_id)
        return self.mongo.db.roles.find_one({'_id': user['role_id']}) if user else None

    def promote_user(self, user_id, new_role_name):
        user = self.get_user(user_id)
        if user:
            new_role = self.mongo.db.roles.find_one({'name': new_role_name})
            if new_role:
                self.mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'role_id': new_role['_id']}})
                return self.get_user(user_id)
        return None
