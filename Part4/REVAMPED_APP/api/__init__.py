
'''
    Package where endpoints and type validations are made.
'''

from flask import Flask
from flasgger import Swagger
from api.swagger import template
from flask import render_template, request, redirect, url_for

app = Flask("AirBnB-MWA")
from flask import render_template, request, redirect, url_for
from .users import get_user_by_email  # adjust based on your actual user logic

from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Example logic — replace with actual DB lookup
        if email == 'test@example.com' and password == 'password123':
            return redirect(url_for('dashboard'))  # Assume a dashboard route exists
        else:
            flash('Invalid email or password.')
            return render_template('login.html')

    return render_template('login.html')

swagger = Swagger(app, template=template)

import api.amenities
import api.cities
import api.countries
import api.places
import api.reviews
import api.users
