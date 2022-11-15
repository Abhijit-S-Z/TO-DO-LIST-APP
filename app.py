from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask("_name__")

app.app_context().push()  #Adding this line removed (RuntimeError: working outside of application context) this ERROR.
#NO IDEA HOW DOES THAT HAPPENED (It has to run every time.)

#To Create DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Class to create table with columns with id, title and complete
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    #Show all Todos(It'll get executed in cmd)
    todo_list = Todo.query.all()
    print(type(todo_list))
    return render_template('base.html', todo_list=reversed(todo_list))

#why it doesn't create any path /add on web and gives ERROR after manually entering it.
@app.route('/add', methods=["POST"])
def add():
    #add new item
    title = request.form.get("title")              #taking value of title from FORM(hmtl)
    new_todo = Todo(title=title, complete=False)   #creating object with class Todo & passing value of title to it
    db.session.add(new_todo)                       #adding above object to the database
    db.session.commit()                            #comminting the changes(insertion of data)
    return redirect(url_for("index"))              #Redirecting to the same page

@app.route("/update/<int:todo_id>")
def update(todo_id):
    #add new item
    todo = Todo.query.filter_by(id=todo_id).first()        
    todo.complete = not todo.complete               
    db.session.commit()                           
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #add new item
    todo = Todo.query.filter_by(id=todo_id).first()        
    db.session.delete(todo)            
    db.session.commit()                           
    return redirect(url_for("index"))

if __name__ =="__main__":
    db.create_all()
    app.run(debug=True)