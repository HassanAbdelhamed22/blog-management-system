from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
from flask_login import login_user
from app.models.user import User
from app.models.role import Role
from werkzeug.security import check_password_hash

class UserService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def login(self, username, password):
        user = self.db.session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return True
        return False

    def register(self, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)  
        self.db.session.add(user)
        self.db.session.commit()
        return user
    
    def username_exists(self, username: str) -> bool:
        return User.query.filter_by(username=username).first() is not None

    def email_exists(self, email: str) -> bool:
        return User.query.filter_by(email=email).first() is not None
    
    def get_user(self, user_id):
        return User.query.get(user_id)
    
    def get_all_users(self):
        return User.query.all()
    
    def get_user_role(self, user_id):
        user = self.get_user(user_id)
        return user.role if user else None

    def promote_user(self, user_id, new_role):
        user = self.get_user(user_id)
        if user:
            new_role = Role.query.filter_by(name=new_role).first()
            if new_role:
                user.role = new_role
                self.db.session.commit()
                return user
        return None
