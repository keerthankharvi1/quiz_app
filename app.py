from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Quiz, Question, Response
from forms import CreateQuizForm, JoinQuizForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    form = CreateQuizForm()
    if form.validate_on_submit():
        quiz = Quiz(title=form.title.data)
        db.session.add(quiz)
        db.session.commit()

        questions = form.questions.data.split('\n')
        for q in questions:
            question_text, answer = q.split('? ')
            question = Question(content=question_text, answer=answer, quiz_id=quiz.id)
            db.session.add(question)
        
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('create_quiz.html', form=form)

@app.route('/join_quiz', methods=['GET', 'POST'])
def join_quiz():
    form = JoinQuizForm()
    if form.validate_on_submit():
        username = form.username.data
        # Logic for joining a quiz
        return redirect(url_for('quiz', username=username))
    
    return render_template('join_quiz.html', form=form)

@app.route('/quiz/<username>', methods=['GET', 'POST'])
def quiz(username):
    # Logic for displaying and answering questions
    return render_template('quiz.html', username=username)

@app.route('/leaderboard')
def leaderboard():
    # Logic for displaying the leaderboard
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(debug=True)
