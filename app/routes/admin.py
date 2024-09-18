from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from flask_injector import inject
from app.forms.RoleForm import RoleForm
from app.forms.postForm import PostForm
from app.services.sql.user import UserService
from app.services.sql.blog import BlogService
from flask_wtf import FlaskForm

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
    form = PostForm()
    
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))

    post = blog_service.get_post(post_id)

    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
        post, error_message = blog_service.update_post(post_id, title=title, content=content, is_admin=True)

        if post:
            return redirect(url_for('admin.manage_posts'))
        else:
            return render_template('/admin/edit_blog.html', post=post, error_message=error_message, form=form)

    return render_template('/admin/edit_blog.html', post=post, form=form)


@admin.route('/posts/delete/<int:post_id>')
@login_required
@inject
def delete_post(post_id, blog_service: BlogService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))
    
    blog_service.delete_post(post_id, is_admin=True)
    return redirect(url_for('admin.manage_posts'))

@admin.route('/users')
@login_required
@inject
def manage_users(user_service: UserService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))
    
    users = user_service.get_all_users()
    form = RoleForm()
    return render_template('/admin/manage_users.html', users=users, form=form)

@admin.route('/users/promote/<int:user_id>', methods=['POST'])
@login_required
@inject
def promote_user(user_id, user_service: UserService):
    if not current_user.has_role('admin'):
        return redirect(url_for('auth.login_form'))

    form = RoleForm()
    if form.validate_on_submit():
        new_role = form.role.data
        if new_role:
            user = user_service.promote_user(user_id, new_role)
            if user:
                return redirect(url_for('admin.manage_users'))
    return redirect(url_for('admin.manage_users'))
