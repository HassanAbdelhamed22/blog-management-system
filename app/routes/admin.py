from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from flask_injector import inject
from app.services.user import UserService
from app.services.blog import BlogService

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@login_required
@inject
def admin_dashboard(user_service: UserService, blog_service: BlogService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))
    
    total_users = len(user_service.get_all_users())  
    total_blogs = len(blog_service.get_all_posts()) 

    return render_template('/admin/dashboard.html', total_users=total_users, total_blogs=total_blogs)

@admin.route('/posts')
@login_required
@inject
def manage_posts(blog_service: BlogService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))
    
    posts = blog_service.get_all_posts()
    return render_template('/admin/manage_posts.html', posts=posts)

@admin.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@inject
def edit_post(post_id, blog_service: BlogService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))

    post = blog_service.get_post(post_id)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post, error_message = blog_service.update_post(post_id, title=title, content=content, is_admin=True)

        if post:
            return redirect(url_for('admin.manage_posts'))
        else:
            return render_template('/admin/edit_blog.html', post=post, error_message=error_message)

    return render_template('/admin/edit_blog.html', post=post)

@admin.route('/posts/delete/<int:post_id>')
@login_required
@inject
def delete_post(post_id, blog_service: BlogService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))
    
    blog_service.delete_post(post_id)
    return redirect(url_for('admin.manage_posts'))

@admin.route('/users')
@login_required
@inject
def manage_users(user_service: UserService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))
    
    users = user_service.get_all_users()
    return render_template('/admin/manage_users.html', users=users)

@admin.route('/users/promote/<int:user_id>', methods=['POST'])
@login_required
@inject
def promote_user(user_id, user_service: UserService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))

    new_role = request.form.get('role')
    if new_role:
        user = user_service.promote_user(user_id, new_role)
        if user:
            return redirect(url_for('admin.manage_users'))
    return redirect(url_for('admin.manage_users'))
