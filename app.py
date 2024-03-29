from flask import Flask, render_template, request, redirect, url_for
from models import db, Task, Status, TASK_STATUS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




@app.route('/')
def index():
    task_list = Task.query.all()
    total_tasks = len(task_list)
    return render_template('index.html', task_list=task_list, total_tasks=total_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    new_task = Task(title=title, status=TASK_STATUS[0])
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_task/<int:task_id>')
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.status == TASK_STATUS[0]:
        task.status = TASK_STATUS[1]
    elif task.status == TASK_STATUS[1]:
        task.status = TASK_STATUS[2]

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/progress_task/<int:task_id>')
def progress_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.status == TASK_STATUS[0]:
        task.status = TASK_STATUS[1]
    elif task.status == TASK_STATUS[1]:
        task.status = TASK_STATUS[2]

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/regress_task/<int:task_id>')
def regress_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task.status == TASK_STATUS[2]:
        task.status = TASK_STATUS[1]
    elif task.status == TASK_STATUS[1]:
        task.status = TASK_STATUS[0]

    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


def create_sample_task():
    new_task = Task(title='An example task', status=TASK_STATUS[0])
    db.session.add(new_task)
    db.session.commit()

def create_status():
    for status in TASK_STATUS:
        exists = db.session.query(Status.name).filter_by(name=status).first()
        if not exists:
            db.session.add(Status(name=status))
    db.session.commit()

def init_db():
    db.app = app
    db.init_app(app)
    db.create_all()

init_db()
create_status()

if __name__ == '__main__':

    app.run()
