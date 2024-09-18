from app import db
from app.models.sql.role import Role
from flask_injector import inject

class RoleService:
    @inject
    def __init__(self, db):
        self.db = db

    def insert_roles(self):
        roles = ['admin', 'author', 'user']
        
        for role_name in roles:
            role = Role.query.filter_by(name=role_name).first()
            
            if role is None:
                new_role = Role(name=role_name)
                self.db.session.add(new_role)
                print(f'Inserted role: {role_name}')
        
        self.db.session.commit()
