from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db, bcrypt

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
        
    def generate_token(self, expires_sec=1800):  
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return DataUser.query.get(user_id)
