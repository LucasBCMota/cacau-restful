from flask import Flask, jsonify, make_response, request, url_for

app = Flask(__name__)

states = [
	{
		'id': 1,
		'title': u'Start',
		'description': u'Everything stopped',
		'command': 1
	},
	{
		'id': 2,
		'title': u'BA',
		'description': u'Up and down all the way',
		'command': 2
	}
]

@app.route('/')
def index():
	return "Hello World!"

@app.route('/cacau/api/v1.0/states', methods=['GET'])
def get_states():
	return jsonify({'states': [make_public_state(state) for state in states]})

@app.route('/cacau/api/v1.0/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
	state = [state for state in states if state['id'] == state_id][0]
	if len(state) == 0:
		abort(404)
	return jsonify({'state': state})

@app.route('/cacau/api/v1.0/states', methods=['POST'])
def create_state():
	if not request.json or not 'command' in request.json:
		abort(400)
	state = {
		'id': states[-1]['id'] + 1,
		'title': request.json.get('title', "Untitled"),
		'description': request.json.get('description', ""),
		'command': request.json['command']
	}
	states.append(state)
	return jsonify({'state': state}), 201

@app.route('/cacau/api/v1.0/states/<int:state_id>', methods=['PUT'])
def update_state(state_id):
	state = [state for state in states if state['id'] == state_id][0]
	if len(state) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'title' in request.json and type(request.json['title']) is not unicode:
		abort(400)
	if 'command' in request.json and type(request.json['command']) is not unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
	state['title'] = request.json.get('title', state['title'])
	state['description'] = request.json.get('description', state['description'])
	state['command'] = request.json.get('command', state['command'])
	return jsonify({'state': state})

@app.route('/cacau/api/v1.0/states/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
	state = [state for state in states if state['id'] == state_id][0]
	if len(state) == 0:
		abort(404)
	states.remove(state)
	return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

def make_public_state(state):
	new_state = {}
	for field in state:
		if field =='id':
			new_state['uri'] = url_for('get_state', state_id=state['id'], _external=True)
		else:
			new_state[field] = state[field]

	return new_state

if __name__ == '__main__':
	app.run(debug=True)