from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from mongoengine import connect
from models.user_model import User  # Import the User model
from models.post_model import Post  # Assuming you have a post model
from models.reply_model import Reply  # Assuming you have a reply model

app = Flask(__name__)
app.secret_key = 'en_nenjil_kudiyirukum'  # random secret key
connect('the_forum')  # Connect to your MongoDB database

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.objects(username=username):
            flash('Username already exists.')
        else:
            user = User(username=username)
            user.set_password(password)
            user.save()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.objects(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))  # Redirect to the main page after login
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    posts = Post.objects()  # Fetch posts from the database
    return render_template('index.html', posts=posts, current_user=current_user)

@app.route('/create_post', methods=['POST'])
def create_post():
    title = request.form.get('title')
    content = request.form.get('content')
    
    # Create a new post and save to the database
    new_post = Post(title=title, content=content)
    new_post.save()
    
    return redirect('/')

@app.route('/reply/<post_id>', methods=['POST'])
def reply(post_id):
    content = request.form.get('content')
    post = Post.objects.get(id=post_id)  # Find the post to reply to
    
    # Create a new reply and link it to the post
    new_reply = Reply(content=content, post=post)
    new_reply.save()

    # Add the reply to the post's list of replies
    post.update(push__replies=new_reply)
    
    return redirect(url_for('index'))

@app.route('/like_post/<post_id>', methods = ['POST'])
@login_required
def like_post(post_id):
    post = Post.objects.get(id=post_id)
    user_id = str(current_user.id)

    if user_id in post.likes:
        post.update(pull__likes=user_id)
    else:
        post.update(push__likes=user_id)
    return redirect(url_for('index'))

@app.route('/like_reply/<reply_id>',methods = ['POST'])
@login_required
def like_reply(reply_id):
    reply = Reply.objects.get(id=reply_id)
    user_id = str(current_user.id)
    if user_id in reply.likes:
        reply.update(pull__likes=user_id)
    else:
        reply.update(push__likes=user_id)
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)
