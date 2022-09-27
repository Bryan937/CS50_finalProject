import os
import secrets
from PIL import Image
from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from website import app, db, bcrypt
from website.forms import SignupForm, LoginForm, UpdateProfileForm, PostForm, SearchForm
from website.models import User, Grade, Subject, Post


@app.route("/")
def index():
    """ Show index page """

    # If user is already loged in redirect him to his feed
    if current_user.is_authenticated:
        return redirect(url_for('feed'))

    return render_template("index.html", title='Welcome')
    

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """ Show signup page """

    # If user is already loged in redirect him to his feed
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    # Signup the user
    form = SignupForm()

    # Ensure the input the user wrote is valid
    if form.validate_on_submit():

        # Hash the password given by user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # Add user info into the database
        # If user inserts no grade, ignore the grade fields
        if form.grade.data is None:
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        else:
            user = User(username=form.username.data, grade=form.grade.data.name, grade_id=form.grade.data.id,
                   email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        # Show succes message and return to login page
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template("signup.html", title='Sign Up', form=form)  
      
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Show login page """

    # If user is already loged in redirect him to his feed
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    
    # Login the user
    form = LoginForm()

     # Ensure the input the user wrote is valid
    if form.validate_on_submit():

        # Ensure user email exists in the database
        user = User.query.filter_by(email=form.email.data).first()
        
        # Ensure user's email and password hash matches
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            # Redirect user to the page he was trying to go to
            next_page = request.args.get('next')

            # Redirect user to his feed (or the page he was trying to access)
            return redirect(next_page) if next_page else redirect(url_for('feed'))
       
        else:
                # Show error message and redirect user to login if login failed
                flash('Login failed. Please check your email and/or password!', 'danger')
                return redirect(url_for('login'))
  
    return render_template("login.html", title='Log In', form=form)  


@app.route("/logout")
def logout():
    #Log user out
    logout_user()

    # Redirect user to login form
    return redirect(url_for("index"))
   
# Save the profile pictures in a file with random generated file names    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    #Resize picture uploaded
    output_size = (145, 130)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    """ Show profile page """
    
    # Show post of the user currently connected
    page = request.args.get('page', 1, type=int)
    posts= Post.query.filter_by(user_id=current_user.id)\
           .order_by(Post.date_posted.desc())\
           .paginate(page=page, per_page=8)

    # Update profile form
    form = UpdateProfileForm()

    # Ensure the input the user wrote is valid
    if form.validate_on_submit():

        # Update email, username or profile picture if user chose to do so (If grade is None)
        if form.grade.data is None:
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.profile_pic = picture_file
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()
        
        # Update email, username, grade or profile picture if user chose to do so
        else:
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.profile_pic = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.grade = form.grade.data.name
            current_user.grade_id = form.grade.data.id
            db.session.commit()

        # Show success message and update the user's profile
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))

    # Show current user's email, grade, username and profile picture
    elif request.method == 'GET':
   
        if form.grade.data is None:
            form.username.data = current_user.username
            form.email.data = current_user.email
            profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

        else:
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.grade.data.name = current_user.grade
            profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)

    
    return render_template("profile.html", title=current_user.username, profile_pic=profile_pic, form=form, posts=posts)


@app.route("/user/<string:username>")
def user_profile(username):
    """ Show another user page """

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    anonymous = current_user.get_id()

    # If user is anonymous go to other user profile
    if anonymous is None:
        posts = Post.query.filter_by(author=user)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=5)
        profile_pic = url_for('static', filename='profile_pics/' + user.profile_pic)

        return render_template("user_profile.html", title=user.username, posts=posts, user=user, profile_pic=profile_pic)

    # Redirect to profile if user chosen is the current user
    elif user.id == current_user.id:
        return redirect(url_for('profile'))

    # Else go to the other user profile page
    else:
        posts = Post.query.filter_by(author=user)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=5)
        profile_pic = url_for('static', filename='profile_pics/' + user.profile_pic)

    return render_template("user_profile.html", title=user.username, posts=posts, user=user, profile_pic=profile_pic)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """ Show create new post page"""
    form = PostForm()

    # Ensure the input the user wrote is valid
    if form.validate_on_submit():
            post = Post(title=form.title.data, grade=form.grade.data.name, grade_id=form.grade.data.id,
                        subject=form.subject.data.name, subject_id=form.subject.data.id, question=form.question.data,
                        answer=form.answer.data, user_id=current_user.id, author=current_user)
            db.session.add(post)
            db.session.commit()

            # Show success message and rederect the user's to his feed
            flash('Your Worksheet has been created!', 'success')
            return redirect(url_for('feed'))

    return render_template("create_post.html", title='New Worksheet',
                          form=form, legend='New Worksheet')

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    # Show page of an individual post
    form = SearchForm()

    page = request.args.get('page', 1, type=int)

    # Show post who respects filter applied
    if form.validate_on_submit():
        posts= Post.query.filter_by(grade=form.grade.data.name, subject=form.subject.data.name)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=8)

        grade = Grade.query.filter_by(name=form.grade.data.name).first_or_404()
        subject = Subject.query.filter_by(name=form.subject.data.name).first_or_404()

        return render_template("worksheets.html", title="Filtered Worksheets",
                              posts=posts, subject=subject.name, separator=" & ", separator2="/",
                              form=form, legend="Worksheets", grade=grade.name)

    post = Post.query.get_or_404(post_id)
    return render_template("single_post.html", title=post.title, form=form, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Ensure Worksheet author is the only one able to modify his worksheet
    if post.author != current_user:
        abort(403)
    
    # Allow user to update his worksheet
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.subject = form.subject.data.name
        post.subject_id = form.subject.data.id
        post.grade = form.grade.data.name
        post.grade_id = form.grade.data.id
        post.question = form.question.data
        post.answer = form.answer.data
        db.session.commit()
        flash('Your Worksheet has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.grade.data = post.grade
        form.subject.data = post.subject
        form.question.data = post.question
        form.answer.data = post.answer

    return render_template("create_post.html", title='Update Worksheet',
                          form=form, legend='Update your Worksheet')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Ensure Worksheet author is the only one able to modify his worksheet
    if post.author != current_user:
        abort(403)
    
    # Delete post chosen
    db.session.delete(post)
    db.session.commit()
    flash('Your worksheet has been deleted', 'success')
    
    return redirect(url_for('profile'))


@app.route("/feed", methods=['GET', 'POST'])
@login_required
def feed():
    """ Show feed page """
    form = SearchForm()

    page = request.args.get('page', 1, type=int)

     # Show post who respects filtered
    if form.validate_on_submit():
        posts= Post.query.filter_by(grade=form.grade.data.name, subject=form.subject.data.name)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=8)

        grade = Grade.query.filter_by(name=form.grade.data.name).first_or_404()
        subject = Subject.query.filter_by(name=form.subject.data.name).first_or_404()

        return render_template("worksheets.html", title="Filtered Worksheets",
                              posts=posts, subject=subject.name, separator=" & ", separator2="/",
                              form=form, legend="Worksheets", grade=grade.name)

    # If user doesn't have a grade show all latest post
    if current_user.grade is None:
        posts= Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        
        return render_template("feed(no_grade).html", title='Feed', posts=posts)

    # Show posts base of the user grade (+/- 1)
    else:    
        posts= Post.query.filter_by(grade_id=current_user.grade_id)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=8)

        posts1 = Post.query.filter_by(grade_id=current_user.grade_id + 1)\
                .order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=8)

        posts2 = Post.query.filter_by(grade_id=current_user.grade_id - 1)\
                .order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=8)

        return render_template("feed.html", title='Feed', form=form, posts=posts, posts1=posts1, posts2=posts2)


@app.route("/worksheets", methods=['GET', 'POST'])
def worksheets():
    """ Show all worksheets """
    form = SearchForm()

    page = request.args.get('page', 1, type=int)
    
    # Show post who respects filtered
    if form.validate_on_submit():
        posts= Post.query.filter_by(grade=form.grade.data.name, subject=form.subject.data.name)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=8)

        grade = Grade.query.filter_by(name=form.grade.data.name).first_or_404()
        subject = Subject.query.filter_by(name=form.subject.data.name).first_or_404()

        return render_template("worksheets.html", title="Filtered Worksheets",
                              posts=posts, subject=subject.name, separator=" & ", separator2="/",
                              form=form, legend="Worksheets", grade=grade.name)

    # Show all post
    posts= Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    return render_template("worksheets.html", title='All Worksheets',
                          posts=posts, form=form, legend="Worksheets")


@app.route("/worksheets/<string:parameter>", methods=['GET', 'POST'])
def worksheets_parameter(parameter):
    """ Show worksheets of a specefic grade """
    form = SearchForm()

    page = request.args.get('page', 1, type=int)

    # Show post who respects filtered
    if form.validate_on_submit():
        posts= Post.query.filter_by(grade=form.grade.data.name, subject=form.subject.data.name)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=8)

        grade = Grade.query.filter_by(name=form.grade.data.name).first_or_404()
        subject = Subject.query.filter_by(name=form.subject.data.name).first_or_404()

        return render_template("worksheets.html", title="Filtered Worksheets",
                              posts=posts, subject=subject.name, separator=" & ",
                              form=form, legend="Worksheets", grade=grade.name)

    # Look for a grade
    post_grade = Grade.query.filter_by(name=parameter).first()

    if post_grade is not None:
        # Show all post of chosen grade
        posts= Post.query.filter_by(grade=post_grade.name)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=8)
        
        return render_template("worksheets.html", title=parameter + " Worksheets", description=post_grade.description,
                          posts=posts, form=form, legend=parameter + " Worksheet", parameter=parameter, dots=": ")

    # Look for a subject
    post_subject = Subject.query.filter_by(name=parameter).first()

    if post_subject is not None:
        # Show all post of a chosen subject
        posts= Post.query.filter_by(subject=post_subject.name)\
               .order_by(Post.date_posted.desc())\
               .paginate(page=page, per_page=8)

        return render_template("worksheets.html", title=parameter + " Worksheets", description=post_subject.description,
                          posts=posts, form=form, legend=parameter + " Worksheet", parameter=parameter, dots=": ")
    else:
        # If no grade/subject found display 404 error
        abort(404)

