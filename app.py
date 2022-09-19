import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)

# migrate - bootstrp database migrate commands
migrate = Migrate(app, db)

# commit changes before migrate
db.create_all()


class Swim(db.Model):
    __tablename__ = 'swims'
    id = db.Column(db.Integer(), primary_key=True)
    timestamp = db.Column(db.DateTime(), nullable=False)
    kraulen_bahnen = db.Column(db.Integer(), nullable=False)
    kraulen_bahnen_zeit = db.Column(db.Float(), nullable=True)
    brust_bahnen = db.Column(db.Integer(), nullable=False)
    brust_bahnen_zeit = db.Column(db.Float(), nullable=True)
    ruecken_bahnen = db.Column(db.Integer(), nullable=False)
    ruecken_bahnen_zeit = db.Column(db.Float(), nullable=True)
    kommentar = db.Column(db.String(), nullable=True)
    bahnlaenge = db.Column(db.Integer(), nullable=False)
    kcal = db.Column(db.Integer(), nullable=True)


@app.route('/')
def index():
    return redirect(url_for('swims_index'))


@app.route('/swims', methods=['GET'])
def swims_index():
    swims = Swim.query.all()
    kraulen_bahnen, brust_bahnen, ruecken_bahnen = 0, 0, 0
    kraulen_bahnen_zeit, brust_bahnen_zeit, ruecken_bahnen_zeit = [], [], []
    timestamps = []

    for swim in swims:
        kraulen_bahnen += swim.kraulen_bahnen
        kraulen_bahnen_zeit.append(swim.kraulen_bahnen_zeit)
        brust_bahnen += swim.brust_bahnen
        brust_bahnen_zeit.append(swim.brust_bahnen_zeit)
        ruecken_bahnen += swim.ruecken_bahnen
        ruecken_bahnen_zeit.append(swim.ruecken_bahnen_zeit)
        timestamps.append(swim.timestamp.strftime("%Y-%m-%d"))

    kraulen_bahnen_zeit = sum(kraulen_bahnen_zeit) / len(kraulen_bahnen_zeit) if len(kraulen_bahnen_zeit) != 0 else 0
    brust_bahnen_zeit = sum(brust_bahnen_zeit) / len(brust_bahnen_zeit) if len(brust_bahnen_zeit) != 0 else 0
    ruecken_bahnen_zeit = sum(ruecken_bahnen_zeit) / len(ruecken_bahnen_zeit) if len(ruecken_bahnen_zeit) != 0 else 0

    gesamt_bahnen = kraulen_bahnen + brust_bahnen + ruecken_bahnen

    print(timestamps)

    return render_template(
        'swims/index.html',
        swims=Swim.query.all(),
        first=[kraulen_bahnen / gesamt_bahnen if gesamt_bahnen != 0 else 0, brust_bahnen / gesamt_bahnen if gesamt_bahnen != 0 else 0, ruecken_bahnen / gesamt_bahnen if gesamt_bahnen != 0 else 0],
        second=[kraulen_bahnen_zeit, brust_bahnen_zeit, ruecken_bahnen_zeit],
        third=timestamps
    )


@app.route('/swims/create', methods=['GET'])
def swims_create():
    return render_template('swims/create.html')


@app.route('/swims', methods=['POST'])
def swims_store():
    print(request)
    print(request.get_json())

    timestamp = request.get_json()['timestamp']
    timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")
    kraulen_bahnen = request.get_json()['kraulen_bahnen']
    kraulen_bahnen_zeit = request.get_json()['kraulen_bahnen_zeit']
    brust_bahnen = request.get_json()['brust_bahnen']
    brust_bahnen_zeit = request.get_json()['brust_bahnen_zeit']
    ruecken_bahnen = request.get_json()['ruecken_bahnen']
    ruecken_bahnen_zeit = request.get_json()['ruecken_bahnen_zeit']
    kommentar = request.get_json()['kommentar']
    bahnlaenge = request.get_json()['bahnlaenge']
    kcal = request.get_json()['kcal']

    swim = Swim(
        timestamp=timestamp,
        kraulen_bahnen=kraulen_bahnen,
        kraulen_bahnen_zeit=kraulen_bahnen_zeit,
        brust_bahnen=brust_bahnen,
        brust_bahnen_zeit=brust_bahnen_zeit,
        ruecken_bahnen=ruecken_bahnen,
        ruecken_bahnen_zeit=ruecken_bahnen_zeit,
        kommentar=kommentar,
        bahnlaenge=bahnlaenge,
        kcal=kcal)

    db.session.add(swim)
    db.session.commit()

    return render_template('swims/index.html')


@app.route('/swims/<swim_id>', methods=['GET'])
def swims_show():
    pass


@app.route('/swims/<swim_id>/edit', methods=['GET'])
def swims_edit(swim_id):
    print(swim_id)
    return render_template('swims/edit.html', swim=Swim.query.get(swim_id))


@app.route('/swims/<swim_id>', methods=['PUT'])
def swims_update(swim_id):
    try:
        timestamp = request.get_json()['timestamp']
        timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M")
        kraulen_bahnen = request.get_json()['kraulen_bahnen']
        kraulen_bahnen_zeit = request.get_json()['kraulen_bahnen_zeit']
        brust_bahnen = request.get_json()['brust_bahnen']
        brust_bahnen_zeit = request.get_json()['brust_bahnen_zeit']
        ruecken_bahnen = request.get_json()['ruecken_bahnen']
        ruecken_bahnen_zeit = request.get_json()['ruecken_bahnen_zeit']
        kommentar = request.get_json()['kommentar']
        bahnlaenge = request.get_json()['bahnlaenge']
        kcal = request.get_json()['kcal']
        swim = Swim.query.get(swim_id)
        swim.timestamp = timestamp if timestamp else swim.timestamp
        swim.kraulen_bahnen = kraulen_bahnen if kraulen_bahnen else swim.kraulen_bahnen
        swim.kraulen_bahnen_zeit = kraulen_bahnen_zeit if kraulen_bahnen_zeit else swim.kraulen_bahnen_zeit
        swim.brust_bahnen = brust_bahnen if brust_bahnen else swim.brust_bahnen
        swim.brust_bahnen_zeit = brust_bahnen_zeit if brust_bahnen_zeit else swim.brust_bahnen_zeit
        swim.ruecken_bahnen = ruecken_bahnen if ruecken_bahnen else swim.ruecken_bahnen
        swim.ruecken_bahnen_zeit = ruecken_bahnen_zeit if ruecken_bahnen_zeit else swim.ruecken_bahnen_zeit
        swim.kommentar = kommentar if kommentar else swim.kommentar
        swim.bahnlaenge = bahnlaenge if bahnlaenge else swim.bahnlaenge
        swim.kcal = kcal if kcal else swim.kcal
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('swims/index.html')


@app.route('/swims/<swim_id>', methods=['DELETE'])
def swims_destroy(swim_id):
    Swim.query.filter(Swim.id == swim_id).delete()
    db.session.commit()
    return render_template('swims/index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
