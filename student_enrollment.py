from flask import Flask, request,render_template
from flask_cors import CORS
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask_admin.contrib.sqla import ModelView
from flask import jsonify
import json
# flask --app student_enrollment run
app = Flask(__name__) 
CORS(app)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Username_Password.sqlite"
db = SQLAlchemy(app)
admin_instance = Admin(app)

@dataclass
class username_password(db.Model):   
    id:int = db.Column(db.Integer, primary_key=True)
    Username:str = db.Column(db.String) #Username will be the name of the person 
    Password:str = db.Column(db.String)
    Student_Teacher_Admin = db.Column(db.String)
    #Students_Courses = db.relationship('Courses',secondary='Students_Courses', lazy='subquery', backref=db.backref('classes', lazy=True))
    courses = db.relationship('courses', secondary='Students_Courses', lazy='subquery', backref=db.backref('students', lazy=True))

@dataclass
class courses(db.Model):    
    id:int = db.Column(db.Integer, primary_key=True)
    Class_Name:str = db.Column(db.String)
    Teacher_Name:str = db.Column(db.String)
    Time:str = db.Column(db.String)
    Capacity:int = db.Column(db.Integer)

    #Students_Courses = db.relationship('Username_Password',secondary='Students_Courses', lazy='subquery', backref=db.backref('students', lazy=True))

#for teachers classes: select classname where teacher = name
 #many to many relationship

# Students_Courses = db.Table('Students_Courses',
#      db.Column('User_id', db.Integer, db.ForeignKey('username_password.id')),
#      db.Column('Class_id', db.Integer, db.ForeignKey('courses.id')),
#      db.Column('Grade',db.Integer)
# )

class Students_Courses(db.Model):
    __tablename__ = 'Students_Courses'
    User_id = db.Column(db.Integer, db.ForeignKey('username_password.id'), primary_key=True)
    Class_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    Grade = db.Column(db.Integer)

class StudentsCoursesView(ModelView):
    column_hide_backrefs = False
    column_list = ['User_id', 'Class_id', 'Grade']
    form_columns = ['User_id', 'Class_id', 'Grade']

#@dataclass
#class Students_CoursesView(db.Model):
    # column_hide_backrefs = False
    # column_list = ['username_password.id', 'courses.id', 'Students_Courses.Grade']
    # form_columns = ['User_id', 'Class_id', 'Grade']
    #db.Column('User_id', db.Integer, db.ForeignKey('username_password.id')),
    #db.Column('Class_id', db.Integer, db.ForeignKey('courses.id')),
    #db.Column('Grade',db.Integer) 
    #User_id:int = db.Column(db.Integer,db.ForeignKey('username_password.id'))
    #Class_id:int = db.Column(db.Integer,db.ForeignKey('courses.id'))
    #Grade:int = db.Column(db.Integer)


admin_instance.add_view(ModelView(username_password, db.session))
admin_instance.add_view(ModelView(courses, db.session))
#admin.add_view(ModelView(Students_Courses, db.session))
admin_instance.add_view(StudentsCoursesView(Students_Courses, db.session))

@app.route('/')
def hello_world():
    return 'hello World'

@app.route('/admin')
def admin_routing():
    return render_template("admin_index.html")
#admin.init_app(app)

@app.route('/login/<person>')
def login(person):
    #all_Users = (username_password.query.all())
    print("asdsa")
    user = username_password.query.filter(username_password.Username == person).first()
    print(user)
    if(user != None):
        user_dict = {
            'password':user.Password,
            'Student_Teacher_Admin':user.Student_Teacher_Admin

        }
        return jsonify(user_dict)

    return "not found"


@app.route('/studentdata')
def studentdata():
    return "nothing so far"


if __name__ == '__main__':
    admin_instance.init_app(app)
    app.run(port=5000, debug = True)
    