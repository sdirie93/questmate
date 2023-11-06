# the entry point of our application

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the Quest model
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    due_date = db.Column(db.String(10), nullable=False)
    progress = db.Column(db.String(10), nullable=False)
    player = db.Column(db.String(80), nullable=True)

    def __init__(self, title, due_date, progress, player=None):
        self.title = title
        self.due_date = due_date
        self.progress = progress
        self.player = player

    def __repr__(self):
        return '<Quest %r>' % self.title

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quests.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    return app  # This line is important!

app = create_app()

@app.route('/quest/<int:quest_id>')
def quest(quest_id):
    quest = Quest.query.filter_by(id=quest_id).first()
    if quest:
        return render_template('quest.html', quest=quest)
    else:
        return "Quest not found", 404

# CRUD:

#Read all quests
@app.route('/')
def index():
    quests = Quest.query.all()
    return render_template('index.html', quests=quests)

# Create a new quest

@app.route('/add', methods=['GET'])
def show_add_quest_form():
    return render_template('add_quest.html')

@app.route('/add', methods=['POST'])
def add_quest():
    title = request.form['title']
    due_date = request.form['due_date']
    progress = request.form.get('progress', '0 / 100%')
    player = request.form.get('player', '')

    new_quest = Quest(title=title, due_date=due_date, progress=progress, player=player)
    db.session.add(new_quest)
    db.session.commit()

    return redirect(url_for('index'))

#Update a quest
@app.route('/update/<int:quest_id>', methods=['GET', 'POST'])
def update_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    if request.method == 'POST':
        quest.title = request.form['title']
        quest.due_date = request.form['due_date']
        quest.progress = request.form['progress']
        quest.player = request.form['player']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', quest=quest)


# Delete a quest
@app.route('/delete/<int:quest_id>', methods=['POST'])
def delete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    db.session.delete(quest)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)