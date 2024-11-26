from flask import Flask , render_template , url_for , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__,template_folder="C:/Users/shripranav_s/Desktop/Flask/template")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)  # Task content (required)
    completed = db.Column(db.Boolean, default=False)  # Task status (default: not completed)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation

    def __repr__(self):
        return f'<Task {self.id}>'

@app.route('/', methods = ['POST','GET'])
def index():
    
    if request.method == "POST":
        task_content = request.form['content']  # Get the task content from the form
        # print(f"Task added: {task_content}")  # Just print the task content to the console for testing
        # return "POST request received!"  # Respond to the POST request
        new_task = Todo(content = task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Some issue is present'
            
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks = tasks)
@app.route('/delete/<int:id>')
def delete(id):
    del_task = Todo.query.get_or_404(id)
    try:
        db.session.delete(del_task)
        db.session.commit()
        return redirect('/')
    except:
        return ' Problem Deleting'
    


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Problemm Updating'
    else:
        return render_template('update.html', task = task)
    
# @app.route('/push/<int:id>', methods=['GET', 'POST'])

# def push(id):
    
    
    



if __name__ == "__main__":
    app.run()