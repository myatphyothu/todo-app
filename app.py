from flask import Flask, render_template, request, redirect, url_for
from models import db, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




@app.route('/')
def index():
    task_list = Task.query.all()
    return render_template('index.html', task_list=task_list)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    new_task = Task(title=title, completed=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_task/<int:task_id>')
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


def create_sample_task():
    new_task = Task(title='An example task', completed=False)
    db.session.add(new_task)
    db.session.commit()

if __name__ == '__main__':
    db.app = app
    db.init_app(app)
    db.create_all()

    #create_sample_task()

    app.run(debug=True)
