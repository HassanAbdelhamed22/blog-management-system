from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from flask_injector import inject
from app.forms.postForm import PostForm
from app.services.sql.user import UserService
from app.services.sql.blog import BlogService

author = Blueprint('author', __name__, url_prefix='/author')

@author.route('/')
@login_required
@inject
def view_posts(blog_service: BlogService):
  if not current_user.has_role('author'):
      return redirect(url_for('auth.login_form'))
    
  posts = blog_service.get_author_posts(current_user.id)
  return render_template('author/posts.html', posts=posts)  

@inject
@author.route('/posts/create', methods=['GET', 'POST'])
@login_required
def create_post(blog_service: BlogService):
    form = PostForm()

    if not current_user.has_role('author'):
        return redirect(url_for('auth.login_form'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
        post, error_message = blog_service.create_post(title, content, current_user.id)
        if post:
            return redirect(url_for('author.view_posts'))
        else:
            return render_template('author/create_post.html', error_message=error_message, title=title, content=content, form=form)
    
    return render_template('author/create_post.html', form=form)
  
@inject
@author.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id, blog_service: BlogService):
    form = PostForm()

    if not current_user.has_role('author'):
        return redirect(url_for('auth.login_form'))
    
    post = blog_service.get_post(post_id)
    if post.author_id != current_user.id:
        return redirect(url_for('author.view_posts'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
        post, error_message = blog_service.update_post(post_id, current_user.id, title, content)
        if post:
            return redirect(url_for('author.view_posts'))
        else:
            return render_template('author/edit_post.html', post=post, error_message=error_message, form=form)
    
    return render_template('author/edit_post.html', post=post, form=form)

@inject
@author.route('/posts/delete/<int:post_id>')
@login_required
def delete_post(blog_service: BlogService, post_id):
    if not current_user.has_role('author'):
      return redirect(url_for('auth.login_form'))
    
    blog_service.delete_post(post_id, author_id=current_user.id)
    return redirect(url_for('author.view_posts')) 