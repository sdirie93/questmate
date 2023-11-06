# the entry point of our application

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary data store. In a real app, this should be replaced with database storage.
quests = [
    {'id': 1, 'title': 'Weekly Goals', 'due_date': '10.11.23', 'progress': '0 / 100%', 'player': None},
    {'id': 2, 'title': 'House chores', 'due_date': '12.11.23', 'progress': '15 / 100%', 'player': None},
    {'id': 3, 'title': 'Finish CV', 'due_date': '10.11.23', 'player': 'Sasha'},
    {'id': 4, 'title': 'Book Mock Interview', 'due_date': '10.11.23', 'player': 'Arjun'}
]

@app.route('/')
def index():
    return render_template('index.html', quests=quests)

@app.route('/quest/<int:quest_id>')
def quest(quest_id):
    quest = next((q for q in quests if q['id'] == quest_id), None)
    if quest:
        return render_template('quest.html', quest=quest)
    else:
        return "Quest not found", 404

if __name__ == '__main__':
    app.run(debug=True)