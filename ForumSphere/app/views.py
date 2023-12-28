from flask import render_template, request, redirect, url_for, session
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi
from flask_login import LoginManager, UserMixin

from app import app, db
from app.models import Thread, Comment, Reply 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_thread', methods=['GET', 'POST'])
def create_thread():
    if request.method == 'POST':
        # Process the form submission and add the thread
        title = request.form.get('title')
        content = request.form.get('content')

        # Example: Creating a new thread
        new_thread = Thread(title=title, content=content)
        db.session.add(new_thread)
        db.session.commit()

        return redirect(url_for('view_threads'))

    return render_template('create_thread.html')

@app.route('/view_threads')
def view_threads():
    threads = Thread.query.all()
    return render_template('view_threads.html', threads=threads)

@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    thread = Thread.query.get(thread_id)
    return render_template('view_thread.html', thread=thread)

@app.route('/create_comment/<int:thread_id>', methods=['GET', 'POST'])
def create_comment(thread_id):
    if request.method == 'POST':
        content = request.form['content']
        thread = Thread.query.get(thread_id)

        new_comment = Comment(content=content, thread=thread)
        db.session.add(new_comment)
        db.session.commit()
        
        return redirect(url_for('view_thread', thread_id))

    return render_template('create_comment.html', content=content, thread=thread)

@app.route('/like_thread/<int:thread_id>', methods=['GET'])
def like_thread(thread_id):
    thread = Thread.query.get(thread_id)

    if thread:
        print(f"Current likes: {thread.like}")
        thread.like = thread.like + 1
        db.session.commit()
        print(f"Updated likes: {thread.like}")
        return redirect(url_for('view_thread', thread_id=thread.id))
    else:
        # Handle the case where the thread with the specified ID is not found
        return render_template('error.html', error_message='Thread not found')
    
