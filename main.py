from app import create_app, db
from flask_injector import FlaskInjector, singleton
from app.services.user import UserService
from app.services.role import RoleService
from app.services.blog import BlogService
from app.models.user import User
from app.models.blog import Blog
from flask import Flask, request, jsonify


# Configuration of Dependency Injection
def configure(binder):
    binder.bind(UserService, to=UserService(db), scope=singleton)
    binder.bind(BlogService, to=BlogService(db), scope=singleton)
    binder.bind(RoleService, to=RoleService(db), scope=singleton)

app = create_app()

# @app.route('/update_user_role/<int:user_id>/<int:role_id>', methods=['POST'])
# def update_user_role(user_id, role_id):
#     user = User.query.get(user_id)
#     if user:
#         user.role_id = role_id
#         db.session.commit()
#         return f"User {user_id}'s role updated to {role_id}!", 200
#     else:
#         return f"User {user_id} not found", 404

@app.route('/add_blog', methods=['POST'])
def add_blog():
    data = request.get_json()
    
    # Debugging: Print received data
    print("Received data:", data)
    
    title = data.get('title')
    content = data.get('content')
    author_id = data.get('author_id')

    if title and content and author_id:
        try:
            # Convert author_id to integer
            author_id = int(author_id)
            new_blog = Blog(title=title, content=content, author_id=author_id)
            db.session.add(new_blog)
            db.session.commit()
            return jsonify(message=f"Blog '{title}' added successfully!"), 200
        except ValueError:
            return jsonify(message="Invalid author ID."), 400
    else:
        return jsonify(message="Missing data."), 400


if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Insert predefined roles (admin, author, user)
        #RoleService.insert_roles()

    # Set up FlaskInjector for Dependency Injection
    FlaskInjector(app=app, modules=[configure])
    
    # Run the application
    app.run()
