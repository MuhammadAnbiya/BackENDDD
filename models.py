from app import db, bcrypt

class DataUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
