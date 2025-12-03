from flask import Flask, render_template, redirect, request
from models import db, Entry
from datetime import datetime
import utils
import os

app = Flask(__name__)
# Load configuration from environment with sensible defaults for local dev
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI', os.environ.get('DATABASE_URL', 'sqlite:///database.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
db.init_app(app)

@app.route('/')
def index():
    entries = Entry.query.order_by(Entry.date.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        data = request.form
        new_entry = Entry(
            amount=float(data['amount']),
            category=data['category'],
            type=data['type'],
            note=data['note'],
            date=datetime.strptime(data['date'], '%Y-%m-%d')
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect('/')
    return render_template('add_entry.html')

@app.route('/report')
def report():
    summary = utils.get_monthly_summary()
    return render_template('report.html', summary=summary)

if __name__ == '__main__':
    # Allow runtime configuration via env vars for host/port/debug
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    with app.app_context():
        db.create_all()
    app.run(debug=debug, host=host, port=port)