from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Username_Password.sqlite"
db = SQLAlchemy(app)


class username_password(db.Model):   
    id:int = db.Column(db.Integer, primary_key=True)
    Username:str = db.Column(db.String) #Username will be the name of the person 
    Password:str = db.Column(db.String)
    Student_Teacher_Admin = db.Column(db.String)
    #Students_Courses = db.relationship('Courses',secondary='Students_Courses', lazy='subquery', backref=db.backref('classes', lazy=True))
    courses = db.relationship('courses', secondary='Students_Courses', lazy='subquery', backref=db.backref('students', lazy=True))


class courses(db.Model):    
    id:int = db.Column(db.Integer, primary_key=True)
    Class_Name:str = db.Column(db.String)
    Teacher_Name:str = db.Column(db.String)
    Time:str = db.Column(db.String)
    Capacity:int = db.Column(db.Integer)

    #Students_Courses = db.relationship('Username_Password',secondary='Students_Courses', lazy='subquery', backref=db.backref('students', lazy=True))

#for teachers classes: select classname where teacher = name
 #many to many relationship
Students_Courses = db.Table('Students_Courses',
    db.Column('User_id', db.Integer, db.ForeignKey('username_password.id')),
    db.Column('Class_id', db.Integer, db.ForeignKey('courses.id')),
    db.Column('Grade',db.Integer)
)


with app.app_context():
    user = username_password(Username = "George", Password = "Secure", Student_Teacher_Admin = "student")
    db.session.add(user)

    Math_001 = courses(Class_Name = "Math001", Teacher_Name = "Prof A", Time = "Once A Year", Capacity = "40")
    db.session.add(Math_001)

    user = username_password.query.filter_by(Username="George").first()
    course = courses.query.filter_by(Class_Name="Math001").first()
    grade = 90
    if user and course:
        association_object = Students_Courses.insert().values(User_id=user.id, Class_id=course.id, Grade=grade)
        db.session.execute(association_object)
    

    db.session.commit()

    



    
