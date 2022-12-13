from application import app
from application import db
from flask import render_template, request, url_for, redirect, jsonify

import json

# Index form
@app.route('/', methods=['POST', 'GET'])
def home():
    all_disciplines = db.get_all_disciplines()

    print(request.method)
    if request.method == 'POST':
        form_data = request.json

        to_search = form_data['to_search']
        desc_search = form_data['description_search']

        checked_disciplines = []

        for discipline in all_disciplines:
            if (form_data[str(discipline['id'])]):
                checked_disciplines.append(discipline['name'])

        if (len(checked_disciplines) == 0 and not desc_search):
            result = db.get_all_nodes_by_name(to_search)

        elif(len(checked_disciplines) == 0 and desc_search):
            result = db.get_all_nodes_by_name_and_description(to_search)

        elif(len(checked_disciplines) != 0 and not desc_search):
            result = db.get_discipline_nodes_by_name(to_search, checked_disciplines)

        elif(len(checked_disciplines) != 0 and desc_search):
            result = db.get_discipline_nodes_by_name_and_description(to_search, checked_disciplines)

        print(result)

        checked = {}

        if (desc_search is not None):
            checked['description_search'] = 'On'

        for discipline in checked_disciplines:
            checked[discipline] = 'On'

        return jsonify(result)

    elif request.method == 'GET':
        return render_template('index.html', disciplines=all_disciplines, results=[], checked={})


@app.route('/info/<id>/')
def get_description(id):
    return render_template('info.html', info=db.get_by_id(id))
