from flask import Flask, request,render_template
from flask_cors import CORS
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask_admin.contrib.sqla import ModelView
from flask import jsonify

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

@app.route('/store')
def stor():
    contents = ""
    print("ran")
    with open('storage.txt', 'r') as file:
    # Read the contents of the file
        contents = file.read()
        print("contents: " + contents)
    return contents

@app.route('/store/<n>', methods = ['POST'])
def store(n):
    print(n)
    with open('storage.txt', 'w') as file:
        file.write(n)
        print("stored")
    return "stored"
    
@app.route('/login/<person>')
def login(person):
    #all_Users = (username_password.query.all())
    #print("asdsa")
    user = username_password.query.filter(username_password.Username == person).first()

    print("user: " + user.Username)
    if(user != None):
        user_dict = {
            'username': user.Username,
            'password':user.Password,
            'Student_Teacher_Admin':user.Student_Teacher_Admin,
            'not_found' : False 
        }
        return jsonify(user_dict)

    user_dict = {
            'not_found' : True 
        }
    return jsonify(user_dict)


@app.route('/studentdata/<name>')
def studentdata(name):
    print("name: " + name)
    myId = username_password.query.filter(username_password.Username == name).first()
    
    myId = myId.id
    print(myId)
    classes = Students_Courses.query.filter(Students_Courses.User_id == myId).all()
    serialized_classes = []


    for x in classes:
        class_name = courses.query.filter(courses.id == x.Class_id).first()

        enrolled = Students_Courses.query.filter(Students_Courses.Class_id == x.Class_id).count()

        print("class_id: " + str(x.Class_id))
        serialized_class = {
            'Class_id': class_name.id,
            'Class': class_name.Class_Name,
            'Teacher_Name' : class_name.Teacher_Name,
            'Time' : class_name.Time,
            'Capacity' : class_name.Capacity,
            'Students_Enrolled' : enrolled,
            'Grade': x.Grade
        }
        serialized_classes.append(serialized_class)
    
    return jsonify(serialized_classes)

@app.route('/allcourses')
def allCourses():

    serialized_classes = []

    allClasses =  courses.query.filter()
    for x in allClasses:
        enrolled = Students_Courses.query.filter(Students_Courses.Class_id == x.id).count()
        serialized_class = {
            'Class_id': x.id,
            'Class': x.Class_Name,
            'Teacher_Name' : x.Teacher_Name,
            'Time' : x.Time,
            'Capacity' : x.Capacity,
            'Students_Enrolled' : enrolled,
        }
        serialized_classes.append(serialized_class)

    return jsonify(serialized_classes)

@app.route('/delete/<id>/<name>',  methods = ['GET', 'PUT','OPTIONS','DELETE'])
def deleteCourse(id,name):
    try:
        user = username_password.query.filter(username_password.Username == name).first()
        print(user.id)
        toDelete = Students_Courses.query.filter((Students_Courses.Class_id == id) & (Students_Courses.User_id == user.id)).first()
        print(toDelete)
        db.session.delete(toDelete)
        db.session.commit()
        print("it worked")
    except:
        print("it failed")
        return "failed to delete"
    return "deleted"


@app.route('/add/<id>/<name>',  methods = ['POST'])
def addCourse(id,name):
    try:
        thisClass =  courses.query.filter(courses.id == id).first()
        enrolled = Students_Courses.query.filter(Students_Courses.Class_id == thisClass.id).count()
        if (thisClass.Capacity == enrolled):
            return "Capacity at Max!"
        
        else:
            addclass = username_password.query.filter(username_password.Username == name).first()
            toAdd = Students_Courses(User_id = addclass.id, Class_id = id, Grade = 100)
            db.session.add(toAdd)
            db.session.commit()
            return "added"
        

    except:
        print("it failed")
        return "failed to add"
    return "added"


@app.route('/mycourses/<name>')
def myCourses(name):

    serialized_classes = []
    classes = courses.query.filter(courses.Teacher_Name == name)
    print(name)
    
    for x in classes:
        print(x)
        class_name = courses.query.filter(courses.id == x.id).first()

        enrolled = Students_Courses.query.filter(Students_Courses.Class_id == x.id).count()
        
        print("class_id: " + str(x.id))
        serialized_class = {
            'Class_id': class_name.id,
            'Class': class_name.Class_Name,
            'Teacher_Name' : class_name.Teacher_Name,
            'Time' : class_name.Time,
            'Capacity' : class_name.Capacity,
            'Students_Enrolled' : enrolled,
           
        }
        serialized_classes.append(serialized_class)
    
    return jsonify(serialized_classes)

@app.route('/indvcourse/<name>/<id>')
def indvCourse(name,id):
    serialized_classes = []
    #myClass = courses.query.filter(courses.Teacher_Name == name and courses.id == id)
    myStudents = Students_Courses.query.filter(Students_Courses.Class_id == id)
    print(name)
    
    for x in myStudents:
        print(x.User_id)
        stu_name = username_password.query.filter(username_password.id == x.User_id).first()
        print("student name")
        print(stu_name)
        
        serialized_class = {
            'name': stu_name.Username,
            'Grade': x.Grade
           
        }
        serialized_classes.append(serialized_class)
    
    return jsonify(serialized_classes)

@app.route('/editGrade/<name>/<classId>/<grade>', methods = ['POST'])
def editGrade(name,classId,grade):
    student = username_password.query.filter(username_password.Username == name).first()
    student_in_class = Students_Courses.query.filter(Students_Courses.Class_id == classId and Students_Courses.User_id == student.id ).first()
    print(student_in_class)
    student_in_class.Grade = grade
    db.session.commit()
    print("changed")
    return "edited"

if __name__ == '__main__':
    admin_instance.init_app(app)
    app.run(port=5000, debug = True)
    