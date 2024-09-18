from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo
from app.models.mongo.role import Role


class User:
    def __init__(self, username, email, password, role_id):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role_id = role_id
        self.authored_blogs = []

    def save(self):
        db = mongo.db
        db.users.insert_one({
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role_id': self.role_id,
            'authored_blogs': self.authored_blogs
        })

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        # Get the role document
        role = Role.get_role_by_name(role_name)
        if not role:
            return False

        # Compare role ID with the user's role ID
        db = mongo.db
        user = db.users.find_one({'username': self.username})
        if user:
            return user.get('role_id') == role.get('_id')

        return False
