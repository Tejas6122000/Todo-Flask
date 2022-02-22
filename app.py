from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///posts.db'
db = SQLAlchemy(app)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(30), nullable=False)

    def __repr__(self) -> str:
        return 'Task ID '+ str(self.id)



@app.route('/')
@app.route('/todolist', methods=['GET', 'POST'])
def todolist():
    if request.method == 'POST':
        if request.form['submit'] == "Submit": 
            new_task = request.form['task']
            new_list = List(task=new_task)
            db.session.add(new_list)
            db.session.commit()
            return redirect('/todolist')
        elif request.form['submit']=='Search':
            searchword = request.form['task']
            task = List.query.filter(List.task.like("%"+searchword+"%")).all()
            return render_template('index.html', tasks=task)
    else:    
        tasks = List.query.all()
        return render_template('index.html', tasks=tasks)


@app.route('/todolist/edit/<int:id>',  methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        task = List.query.get_or_404(id)
        task.task = request.form['task']
        db.session.commit()
        return redirect('/todolist')
    else:
        tasks = List.query.all()
        etask = List.query.get_or_404(id)
        return render_template('index.html',etask=etask,tasks=tasks)



@app.route('/todolist/delete/<int:id>')
def delete(id):
    task = List.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/todolist')


if __name__ == '__main__':
    app.run(debug=True)