from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func
from .dati import Utenti
from .dati import Moduli
from .testo import testo
from . import db
import ast

auth = Blueprint("auth", __name__)


@auth.route("/accedi")
def accedi():
    return render_template("accedi.html")


@auth.route("/accedi", methods=["POST"])
def post_accedi():
    email = request.form.get("email")
    password = request.form.get("password")
    ricordami = True if request.form.get("ricordami") else False

    utente = Utenti.query.filter_by(email=email).first()

    if not utente or not check_password_hash(utente.password, password):
        flash("Email o password errati.")
        return redirect(url_for("auth.accedi"))

    login_user(utente, remember=ricordami)
    flash("Successo")
    return redirect(url_for("main.moduli"))


@auth.route("/registrati")
def registrati():
    return render_template("registrati.html")


@auth.route("/registrati", methods=["POST"])
def post_registrati():

    nome = request.form.get("nome")
    cognome = request.form.get("cognome")
    email = request.form.get("email")
    indirizzo = request.form.get("indirizzo")
    password = request.form.get("password")

    utente = Utenti.query.filter_by(email=email).first()

    if utente:
        flash("L\'email è già registrata.")
        return redirect(url_for("auth.registrati"))

    nuovo_utente = Utenti(nome=nome, cognome=cognome, email=email, indirizzo=indirizzo,
                    password=generate_password_hash(password, method="sha256"))

    db.session.add(nuovo_utente)
    db.session.commit()

    flash("Successo")
    return redirect(url_for("auth.accedi"))


@auth.route("/esci")
@login_required
def esci():
    logout_user()
    return redirect(url_for("main.home"))


@auth.route("/moduli", methods=["POST"])
@login_required
def post_modulo():

    nuovo = request.form.get("titolo-nuovo")
    modifica = request.form.get("modifica-modulo")
    elimina = request.form.get("elimina-modulo")
    modulo = request.form.get("index")

    if modulo:
        classi = ast.literal_eval(Moduli.query.filter_by(utente=current_user.id)[eval(modulo)[0]].classi)
        if Moduli.query.filter_by(utente=current_user.id)[eval(modulo)[0]].dati:
            dati = ast.literal_eval(Moduli.query.filter_by(utente=current_user.id)[eval(modulo)[0]].dati)
            return render_template("modulo.html", lingua=eval(modulo)[1], index=eval(modulo)[0], dati=dati, classi=classi, testo=testo)
        else:
            return render_template("modulo.html", lingua=eval(modulo)[1], index=eval(modulo)[0], dati="", classi=classi, testo=testo)

    elif modifica != None:
        index = int(modifica)
        titolo = request.form.get("titolo-modifica")
        lingua = True if request.form.get("lang") == "ita" else False
        modulo = Moduli.query.filter_by(utente=current_user.id)[index]

        modulo.titolo = titolo
        modulo.lingua = lingua

        db.session.commit()

        return redirect(url_for("main.moduli"))

    elif nuovo != None and modifica == None:
        titolo = request.form.get("titolo-nuovo")
        lingua = True if request.form.get("lang") == "ita" else False

        classi = {}
        for i in range(1, 28):
            classi['c' + str(i)] = "icone bi bi-x-lg me-3"
            classi['textareac' + str(i)] = "hidden comp mt-1"
        for i in range(1, 23):
            classi['t' + str(i)] = "icone bi bi-x-lg"
            classi['textareat' + str(i)] = "textarea hidden form-control"

        nuovo_modulo = Moduli(utente=current_user.id,
                            titolo=titolo, lingua=lingua, classi=str(classi))
        db.session.add(nuovo_modulo)
        db.session.commit()

        return redirect(url_for("main.moduli"))

    else:
        index = int(elimina)

        modulo = Moduli.query.filter_by(utente=current_user.id)[index]

        db.session.delete(modulo)
        db.session.commit()

        return redirect(url_for("main.moduli"))


@auth.route("/modifica", methods=["POST"])
@login_required
def modifica():

    nome = request.form.get("nome")
    cognome = request.form.get("cognome")
    email = request.form.get("email")
    indirizzo = request.form.get("indirizzo")

    emaildb = Utenti.query.filter_by(email=email).first()

    if emaildb and email != current_user.email:
        flash("True")
        return redirect(url_for("main.profilo"))
    else:
        utente = Utenti.query.filter_by(email=current_user.email).first()
        utente.nome = nome
        utente.cognome = cognome
        utente.email = email
        utente.indirizzo = indirizzo

        db.session.commit()

        flash("Hai modificato con successo i tuoi dati.")
        return redirect(url_for("main.profilo"))


@auth.route("/profilo", methods=["POST"])
@login_required
def cambio_pass():

    vecchia_pass = request.form.get("vecchia_pass")
    nuova_pass = request.form.get("nuova_pass")

    utente = Utenti.query.filter_by(email=current_user.email).first()
    if not check_password_hash(current_user.password, vecchia_pass):
        return render_template("profilo.html", modal=True)
    else:
        utente.password = generate_password_hash(nuova_pass, method="sha256")
        db.session.commit()
        flash("Hai modificato con successo i tuoi dati.")
        return render_template("profilo.html", modal=False)


@auth.route("/salva", methods=["POST"])
@login_required
def salva():

    dati = request.form.to_dict()

    classi = dati.pop("classi")
    classi = classi.split(',')
    it = iter(classi)
    classi = dict(zip(it, it))

    modulo = Moduli.query.filter_by(utente=current_user.id)[int(dati["i"])]
    modulo.dati = str(dati)
    modulo.classi = str(classi)

    db.session.commit()
    return redirect(url_for("main.moduli"))
