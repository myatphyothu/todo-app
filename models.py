from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


TASK_STATUS = ('Not started', 'In progress', 'Completed')

class Status(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    #completed = db.Column(db.Boolean)
    status = db.Column(db.String(50), db.ForeignKey(Status.name))



