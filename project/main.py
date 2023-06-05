from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_required, current_user
from .dati import Utenti
from .dati import Moduli
from . import db
from flask.helpers import flash

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")

@main.route("/team")
def team():
    return redirect(url_for('home') + '#team')

@main.route("/contatti")
def contatti():
    return redirect(url_for('home') + '#contatti')

@main.route("/profilo")
@login_required
def profilo():
    return render_template("profilo.html")


@main.route("/moduli")
def moduli():

    moduli = Moduli.query.filter_by(utente=current_user.id).all()
    titoli = [i.titolo for i in moduli]
    lingua = [i.lingua for i in moduli]

    return render_template("moduli.html", titoli=titoli, num=len(titoli), lingua=lingua)


@main.route("/modulo")
@login_required
def modulo():
    return render_template("modulo.html")

@main.route("/test")
def test():
    return render_template("test.html")
