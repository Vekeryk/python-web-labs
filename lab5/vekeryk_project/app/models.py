from . import db

class Person(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(225), unique=True, nullable=False)
   
    def repr(self):
        return f"Name : {self.name}, Email: {self.email}"