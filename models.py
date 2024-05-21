from app import db

class DataUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()
