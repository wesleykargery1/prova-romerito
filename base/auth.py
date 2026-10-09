from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        flash("Complete o cadastro usando database.py e generate_password_hash.")
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        procura = database.buscar_usuario_por_email(email)
        if nome == '' or not email or not senha:
           flash('erro de cadastro')
           return redirect(url_for('auth.registro'))
        if procura:
            flash('usuario ja registrado')
            return redirect(url_for('auth.registro'))
        senha_hash = generate_password_hash(senha)
        database.criar_usuario(nome,email,senha_hash)

        return redirect(url_for("auth.login"))

    return render_template("registro.html") 


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        flash("Complete o login usando check_password_hash e session.")
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = database.buscar_usuario_por_email(email= email)
        if usuario and check_password_hash(usuario.senha_hash, senha):
           session['usuario_id'] = usuario.id
           session['usuario_email'] = usuario.email
           return redirect(url_for('leituras.index'))
        flash('usuario ou senha invalidos')
        return redirect(url_for("auth.login"))

    return render_template('login.html')


@auth_bp.route("/logout")
def logout():
    flash("Complete o logout removendo os dados da session.")
    session.pop('usuario_id', None)
    session.pop('usuario_email', None)
    return redirect(url_for("auth.login"))
