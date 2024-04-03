from flask import request, json, render_template
from flask import Blueprint, json, request

import app.extensions

db = app.extensions.db
collection = app.extensions.collection

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=['POST'])
def api_gh_message():
    if request.headers['Content-Type'] == 'application/json':
        abc = json.dumps(request.json)
        x = json.loads(abc)
        # collection.insert_one(x)
        if('commits' in x.keys()):
            pushevent = {}
            pushevent['action'] = 'PUSH'
            pushevent['author'] = x['commits'][0]['author']['name']
            pushevent['to_branch'] = x['ref'][11:]
            pushevent['timestamp'] = str(x['commits'][0]['timestamp'])
            collection.insert_one(pushevent)
            print(pushevent)
        elif('pull_request' in x.keys() and x['action'] == 'opened'):
            pullevent={}
            pullevent['action'] = 'PULL REQUEST'
            pullevent['author'] = x['sender']['login']
            pullevent['to_branch'] = x['pull_request']['head']['ref']
            pullevent['from_branch'] = x['pull_request']['base']['ref']
            pullevent['timestamp'] = str(x['pull_request']['updated_at']).split('T')
            collection.insert_one(pullevent)
            print(pullevent)
        elif('pull_request' in x.keys() and x['action'] == 'closed'):
            mergeevent={}
            mergeevent['action'] = 'MERGE'
            mergeevent['author'] = x['sender']['login']
            mergeevent['to_branch'] = x['pull_request']['head']['ref']
            mergeevent['from_branch'] = x['pull_request']['base']['ref']
            mergeevent['timestamp'] = str(x['pull_request']['updated_at']).split('T')
            collection.insert_one(mergeevent)
            print(mergeevent)
        del x
        return json.dumps(request.json)

@webhook.route('/receiver', methods=['POST','GET'])
def display():
    allhook = collection.find()
    return render_template('index.html', allhook=allhook)