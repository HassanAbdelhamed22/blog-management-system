from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from flask_injector import inject
from app.services.blog import BlogService
from app.forms.likeForm import LikeForm  
from app.forms.dislikeForm import DislikeForm  

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/blogs')
@login_required
@inject
def view_blogs(blog_service: BlogService):
    if not current_user.has_role('user'):
        return redirect(url_for('auth.login_form'))
      
    blogs = blog_service.get_all_posts()
    
    like_form = LikeForm()
    dislike_form = DislikeForm()
    
    return render_template('user/view_blogs.html', blogs=blogs, like_form=like_form, dislike_form=dislike_form)

@user.route('/blogs/like/<int:blog_id>', methods=['POST'])
@login_required
@inject
def like_blog(blog_id, blog_service: BlogService):
    form = LikeForm()

    if not current_user.has_role('user'):
        return redirect(url_for('auth.login_form'))
   
    if form.validate_on_submit():   
        _, message = blog_service.like_blog(blog_id, current_user.id)
        if message:
            return redirect(url_for('user.view_blogs', error=message))
    return redirect(url_for('user.view_blogs'))

@user.route('/blogs/dislike/<int:blog_id>', methods=['POST'])
@login_required
@inject
def dislike_blog(blog_id, blog_service: BlogService):
    form = DislikeForm()

    if not current_user.has_role('user'):
        return redirect(url_for('auth.login_form'))

    if form.validate_on_submit():
        _, message = blog_service.dislike_blog(blog_id, current_user.id)
        if message:
            return redirect(url_for('user.view_blogs', error=message))
    return redirect(url_for('user.view_blogs'))