from . import db

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=True)
    email = db.Column(db.String(40), unique=False, nullable=True)
    phone = db.Column(db.String(15), unique=False, nullable=True)
    subject = db.Column(db.Integer, unique=False, nullable=True)
    message = db.Column(db.Text, unique=False, nullable=True)
   
    def repr(self):
        return f"""Message : {self.message}, Email: {self.email}"""