# the entry point of our application

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80), unique=True, nullable=False)
    student_cohort = db.Column(db.String(10), nullable=True)
    missions = db.relationship('Mission', backref='player', lazy=True)
    quests = db.relationship('Quest', backref='player', lazy=True)

    def __init__(self, player_name, student_cohort):
        self.player_name = player_name
        self.student_cohort = student_cohort

    def __repr__(self):
        return '<Player %r>' % self.player_name

# Define the Quest model
class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    due_date = db.Column(db.String(10), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    missions = db.relationship('Mission', backref='quest', lazy=True)

    def __init__(self, title, due_date, player_id):
        self.title = title
        self.due_date = due_date
        self.player_id = player_id

    def __repr__(self):
        return '<Quest %r>' % self.title

# Define the Mission model
class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.String(10), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

    def __init__(self, quest_id, title, description, due_date, player_id):
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.player_id = player_id

    def __repr__(self):
        return '<Mission %r>' % self.title


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

# CRUD operations for Player
# Create a new player
@app.route('/player/add', methods=['POST'])
def add_player():
    player_name = request.form['player_name']
    student_cohort = request.form['student_cohort']
    new_player = Player(player_name=player_name, student_cohort=student_cohort)
    db.session.add(new_player)
    db.session.commit()
    return redirect(url_for('index'))

# Read all players
@app.route('/players')
def list_players():
    players = Player.query.all()
    return render_template('players.html', players=players)

# Update a player
@app.route('/player/update/<int:player_id>', methods=['GET', 'POST'])
def update_player(player_id):
    player = Player.query.get_or_404(player_id)
    if request.method == 'POST':
        player.player_name = request.form['player_name']
        player.student_cohort = request.form['student_cohort']
        db.session.commit()
        return redirect(url_for('list_players'))
    return render_template('update_player.html', player=player)

# Delete a player
@app.route('/player/delete/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('list_players'))

# CRUD operations for Quest

# Create a new quest
@app.route('/quest/add', methods=['POST'])
def add_quest():
    title = request.form['title']
    due_date = request.form['due_date']
    player_id = request.form['player_id']
    new_quest = Quest(title=title, due_date=due_date, player_id=player_id)
    db.session.add(new_quest)
    db.session.commit()
    return redirect(url_for('index'))

# Read all quests
@app.route('/quests')
def list_quests():
    quests = Quest.query.all()
    return render_template('quests.html', quests=quests)

# Update a quest
@app.route('/quest/update/<int:quest_id>', methods=['GET', 'POST'])
def update_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    if request.method == 'POST':
        quest.title = request.form['title']
        quest.due_date = request.form['due_date']
        quest.player_id = request.form['player_id']
        db.session.commit()
        return redirect(url_for('list_quests'))
    return render_template('update_quest.html', quest=quest)

# Delete a quest
@app.route('/quest/delete/<int:quest_id>', methods=['POST'])
def delete_quest(quest_id):
    quest = Quest.query.get_or_404(quest_id)
    db.session.delete(quest)
    db.session.commit()
    return redirect(url_for('list_quests'))

# CRUD operations for Mission

# Create a new mission
@app.route('/mission/add', methods=['POST'])
def add_mission():
    quest_id = request.form['quest_id']
    title = request.form['title']
    description = request.form['description']
    due_date = request.form['due_date']
    player_id = request.form['player_id']
    new_mission = Mission(quest_id=quest_id, title=title, description=description, due_date=due_date, player_id=player_id)
    db.session.add(new_mission)
    db.session.commit()
    return redirect(url_for('index'))

# Read all missions for a quest
@app.route('/missions/<int:quest_id>')
def list_missions(quest_id):
    missions = Mission.query.filter_by(quest_id=quest_id).all()
    return render_template('missions.html', missions=missions, quest_id=quest_id)

# Update a mission
@app.route('/mission/update/<int:mission_id>', methods=['GET', 'POST'])
def update_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    if request.method == 'POST':
        mission.title = request.form['title']
        mission.description = request.form['description']
        mission.due_date = request.form['due_date']
        mission.player_id = request.form['player_id']
        db.session.commit()
        return redirect(url_for('list_missions', quest_id=mission.quest_id))
    return render_template('update_mission.html', mission=mission)

# Delete a mission
@app.route('/mission/delete/<int:mission_id>', methods=['POST'])
def delete_mission(mission_id):
    mission = Mission.query.get_or_404(mission_id)
    db.session.delete(mission)
    db.session.commit()
    return redirect(url_for('list_missions', quest_id=mission.quest_id))

# Route to display a specific quest by its ID
@app.route('/quest/<int:quest_id>')
def quest(quest_id):
    quest = Quest.query.filter_by(id=quest_id).first()
    if quest:
        return render_template('quest.html', quest=quest)
    else:
        return "Quest not found", 404

# Home route to display all quests, players, and missions
@app.route('/')
def index():
    quests = Quest.query.all()
    players = Player.query.all()
    missions = Mission.query.all()
    return render_template('index.html', quests=quests, players=players, missions=missions)

if __name__ == '__main__':
    app.run(debug=True)
