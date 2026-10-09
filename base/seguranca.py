from flask import flash, redirect, session, url_for


def exigir_login():
    if 'usuario_id' not in session:
        flash('faça login para acessar a pagina')
        return redirect(url_for('auth.login'))
        
