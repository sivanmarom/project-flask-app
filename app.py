from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import iam_user_creation

app = Flask(__name__)
my_users = []

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    def __str__(self):
        return f"Username: {self.user_name}, password:{self.password}"
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_name = request.form.get("username")
        password = request.form.get("password")
        my_users.append(user_name)
        p = Profile(user_name=user_name, password=password)
        db.session.add(p)
        db.session.commit()
        return redirect("/homepage")
    return render_template("signup.html")

@app.route('/homepage')
def homepage():
    return render_template("homepage.html", my_users=my_users)
@app.route('/aws',methods=['POST', 'GET'])
def aws():
    if request.method == 'POST':
        user_name = request.form.get('username')
        password = request.form.get('password')
        response = iam_user_creation.create_iam_user(user_name, password)
        access_key_id = response["access_key_id"]
        secret_access_key = response["secret_access_key"]
        return render_template("iam_creation_user_result.html",
                               user_name=user_name, password=password,
                               access_key_id=access_key_id,
                               secret_access_key=secret_access_key)
    return render_template("aws.html")

if __name__ == "__main__":   
    app.run(host="0.0.0.0", port=5000)
