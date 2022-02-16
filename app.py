from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/",methods=['GET','POST'])
def home():
    if request.method == 'POST':
        user_todo = Todo(title = request.form['title'], desc =request.form['desc'])
        db.session.add(user_todo)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template('index.html', all_todo = all_todo)

@app.route("/update/<int:snum>",methods=['GET','POST'])
def update(snum):
    update_todo = Todo.query.filter_by(sno=snum).first()
    db.session.delete(update_todo)
    db.session.commit()
    return render_template('update.html', update_todo = update_todo)

@app.route("/delete/<int:snum>")
def delete(snum):
    delete_todo = Todo.query.filter_by(sno=snum).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)