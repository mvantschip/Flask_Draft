from datetime import datetime
from flaskdraft import db

class bid(db.Model):
    bid_id = db.Column(db.Integer, primary_key = True)
    date_bid = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    player_id = db.Column(db.Integer, nullable = False)
    player_name = db.Column(db.String, nullable = False)
    player_value = db.Column(db.Float, nullable = False)
    username = db.Column(db.String, nullable = False)
    user_bid = db.Column(db.Float, nullable = False)

    #how our object is printed whenever we print it out
    def __repr__(self):
        return f"bid('{self.username}', '{self.player_name}', '{self.player_id}', '{self.user_bid}', '{self.date_bid}')"

class registration(db.Model):
    registration_id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String, nullable = False)
    user_email = db.Column(db.String(120), nullable = False)
    user_password = db.Column(db.String(60), nullable = False)
    date_email = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"registration('{self.username}', '{self.username_email}')"
