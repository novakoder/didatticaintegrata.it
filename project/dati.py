# from project import db, create_app
# db.create_all(app=create_app())

from flask_login import UserMixin
from . import db


class Utenti(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cognome = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    indirizzo = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Moduli(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utente = db.Column(db.Integer)
    titolo = db.Column(db.String(100))
    lingua = db.Column(db.Boolean)
    dati = db.Column(db.Text)
    classi = db.Column(db.Text)
