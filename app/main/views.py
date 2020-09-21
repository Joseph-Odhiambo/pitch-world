from flask import render_template, redirect, url_for,abort,request
from . import main
from flask_login import login_required,current_user
from ..models import User,Pitch
from ..models import User,Pitch,Comment
from .form import UpdateProfile,PitchForm,CommentForm
from .. import db,photos

@main.route('/')
def index():
    pitches = Pitch.query.all()
    job = Pitch.query.filter_by(category = 'job')   
    return render_template('index.html', job = job, pitches=pitches)
@main.route('/new_pitch', methods = ['POST','GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_pitch = Pitch(post=post,user_id=current_user._get_current_object().id,category=category,title=title)
        new_pitch.save_p()
        return redirect(url_for('main.index'))
    return render_template('create_pitch.html', form = form)
@main.route('/new_comment/<int:pitch_id>')
@login_required
def comment(pitch_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = Pitch.query.get(pitch_id)
        user_id = current_user._get_current_object().id
        new_comment = 
        new_comment = Comment(comment = comment,user_id = user_id,pitch_id = pitch_id)

        new_comment.save_c()
        return redirect(url_for('.new_comment', pitch_id = pitch_id))
    return render_template('comment.html', form =form,)


@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)
@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_u()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)
@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))