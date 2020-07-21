# (c) 2020 Alexander Schremmer <alex@alexanderweb.de>
# Licensed under GPL v3.

import html
import logging
import pwd

import bcrypt
import click
from flask import Flask, redirect, url_for, send_from_directory, request
from werkzeug.utils import secure_filename


logging.basicConfig()
app = Flask(__name__)
ALIASES_FILE = "/etc/aliases"
USERS_FILE = "/tmp/users"


def used_aliases():
    users = {user[0] for user in pwd.getpwall()}
    with open(ALIASES_FILE, "rb") as f:
        for line in f:
            segments = line.split(b"#", 1)[0].decode("utf8").strip().split(":", 1)
            if len(segments) == 2:
                users.add(segments[0])
    return users


def add_alias(alias, to_addr):
    with open(ALIASES_FILE, "a") as f:
        f.write(("%s: %s\n" % (alias, to_addr)))


def check_user(username, password):
    password_states = []
    with open(USERS_FILE, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            l_username, l_pwdhash = line.split()
            if username.lower() == l_username.decode("utf8").lower():
                password_states.append(bcrypt.checkpw(password.encode("utf8"), l_pwdhash))
    return password_states and password_states[-1]


@app.cli.command("set-password")
@click.argument("username")
@click.argument("password")
def set_password(username, password):
    with open(USERS_FILE, "a") as f:
        f.write(("%s %s\n" % (username, bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()).decode("ascii"))))
    print("Done.")


def heading(s):
    return "<h1><a href='/'>" + html.escape(s, quote=True) + "</a></h1>"


def render_page(l):
    s = """
input {
    width: 50%;
}
"""
    return (
        "<html><head><title>Aliasverwaltung</title><style>%s</style></head><body>%s</body></html>"
        % (s, "\n".join(l))
    )


@app.route("/", methods="GET POST".split())
def root():
    alias = request.form.get("alias", "")
    addr = request.form.get("addr", "")
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if username and password:
        if check_user(username, password):
            if alias and addr and "@" in addr:
                if alias not in used_aliases():
                    add_alias(alias, addr)
                else:
                    return render_page([
                        heading("Alias schon vergeben!")
                    ])
                return render_page([
                    heading("Weiterleitung eingerichtet!")
                ])
            else:
                return render_page([
                    heading("Alias oder Adresse nicht angegeben!")])
        return heading("Benutzername oder Passwort falsch!")
    return render_page(
        [
            heading("Weiterleitung einrichten"),
            """<p><form method='POST'>
                <input name='username' placeholder='Benutzername' required><br>
                <input name='password' type="password" placeholder='Passwort' required><br>
                <input name='alias' placeholder='E-Mail-Alias' required><br>
                <input name='addr' placeholder='Vorhandene E-Mail-Adresse' required><br>
                <input type='submit'>
                </form></p>""",
        ]
    )
