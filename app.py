from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
import iam_user_creation
import boto3
import launch_instance

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
@app.route('/aws', methods=['POST', 'GET'])
def aws():
    if request.method == 'POST':
        if 'create_user' in request.form:
            user_name = request.form.get('username')
            password = request.form.get('password')
            access_keys = iam_user_creation.create_iam_user_and_access_key(user_name=user_name, password=password)
            access_key_id = access_keys["AccessKey"]["AccessKeyId"]
            secret_access_key = access_keys["AccessKey"]["SecretAccessKey"]
            return redirect(url_for('iam_creation_user_result',
                                    user_name=user_name,
                                    password=password,
                                    access_key_id=access_key_id,
                                    secret_access_key=secret_access_key))
        elif 'launch_instance' in request.form:
            instance_name = request.form.get('instance_name')
            instance_type = request.form.get('instance_type')
            key_pair_name = request.form.get('key_pair_name')
            image_id = request.form.get('image_id')
            security_group_id = request.form.get('security_group_id')
            instance_count = int(request.form.get('instance_count'))
            for i in range(instance_count):
                launch_instance.launch_ec2_instance(instance_name=instance_name, InstanceType=instance_type, key_pair_name=key_pair_name, image_id=image_id, security_group_id=security_group_id,instance_count=instance_count)
            return redirect(url_for('ec2'))
    return render_template("aws.html")

@app.route('/iam_creation_user_result')
def iam_creation_user_result():
    user_name = request.args.get('user_name')
    password = request.args.get('password')
    access_key_id = request.args.get('access_key_id')
    secret_access_key = request.args.get('secret_access_key')
    return render_template("iam_creation_user_result.html",
                            user_name=user_name,
                            password=password,
                            access_key_id=access_key_id,
                            secret_access_key=secret_access_key)


@app.route('/ec2')
def ec2():
    return render_template("launched.html")

if __name__ == "__main__":   
    app.run(host="0.0.0.0", port=5000)
