"""problem : create a system where user can add, modify, delete cctv camera.

python libraries to use:
1. flask
2. sqlalchemy/flask-sqlalchemy

database to use(use any one):
1. sqlite
2. mysql
3. mongodb

api structure:
1. /add : camera will get added into database
2. /modify: details of the camera will get updated
3. /remove: details of the camera will be removed from database
4. /all: returns details of all the cameras to user

database fields:

id
camera name
camera ip
camera port
camera username
camera password"""


from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#We'll use the popular SQLite database, which comes bundled with the standard installation of Python.
# It is a file-based database, so we can store our data in a file on our file system,
# without needing to install a huge Relational Database Management System (RDBMS).


# We'll use SQLite through SQLAlchemy, which provides a higher level abstraction

#"sqlite:///" prefix to tell SQLAlchemy which database engine we're using.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cameras.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#creating object of app
db = SQLAlchemy(app)


#This will also make SQLAlchemy create a table called cameras,
# which it will use to store our camera objects.
class cameras(db.Model):
    __tablename__ = "cameras"
    camera_id = db.Column('camera_id', db.Integer,unique=True, nullable=False, primary_key = True)
    camera_name = db.Column('camera_name',db.String(20),unique=True, nullable=False)
    camera_ip = db.Column('camera_ip',db.String(20),unique=True, nullable=False)
    camera_port = db.Column('camera_port',db.Integer,unique=True, nullable=False)
    camera_username= db.Column('camera_username',db.String(15),unique=True, nullable=False)
    camera_password= db.Column('camera_password',db.String(10),unique=True, nullable=False)


    def __init__(self, camera_name, camera_ip, camera_port, camera_username, camera_password):
        self.camera_name = camera_name
        self.camera_ip = camera_ip
        self.camera_port = camera_port
        self.camera_username = camera_username
        self.camera_password = camera_password

#this function calls home.html file
@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html')

#creates new camera entry in database
@app.route('/new', methods=['GET','POST'])
def new():
    if request.method == 'POST':

        #if all entries like camera_id, camera_name, camera_ip, camera_port, camera_username, camera_password are not given ,
        # then it will flash "Please enter all the fields"
        if not request.form['camera_name'] or not request.form['camera_ip'] or not request.form['camera_port'] or not request.form['camera_username'] or not request.form['camera_password']:
            flash('Please enter all the fields\n', 'error')
            return redirect(url_for('new'))
        else:
            camera = cameras(request.form['camera_name'], request.form['camera_ip'],
                             request.form['camera_port'], request.form['camera_username'], request.form['camera_password'])

            db.session.add(camera)
            db.session.commit()
            flash('camera successfully added')

            return redirect(url_for('all'))
    return render_template('new.html', cameras=cameras.query.all())

#this fuction show all the camera details from database
@app.route('/all', methods = ['GET'])
def all():
    return render_template('all.html', cameras = cameras.query.all())


#this function is used to modify the camera record only based on camera_id
@app.route("/modify", methods=['GET','POST'])
def modify():
    if request.method == 'POST':
        if not request.form['camera_id']:
            flash('Please enter camera_id', 'error')
            return redirect(url_for('modify'))
        else:
            camera_id = request.form['camera_id']
            data = cameras.query.filter_by(camera_id=camera_id).first()
            data.camera_name = request.form['camera_name']
            data.camera_ip = request.form['camera_ip']
            data.camera_port = request.form['camera_port']
            data.camera_username = request.form['camera_username']
            data.camera_password = request.form['camera_password']
            db.session.commit()
            flash('Camera details was successfully updated')

            return redirect(url_for('all'))
    return render_template('modify.html')

#to delete camera record from database only on the basis of input of camera_id
@app.route("/remove", methods=['GET','POST'])
def remove():
    if request.method == 'POST':
        if not request.form['camera_id']:
            flash('Please enter camera_id', 'error')
            return redirect(url_for('remove'))
        else:
            camera_id = request.form.get("camera_id")
            camera = cameras.query.filter_by(camera_id= camera_id).first()
            db.session.delete(camera)
            db.session.commit()
            flash('Camera details was successfully deleted')
            return redirect(url_for("remove"))
    return render_template('remove.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)