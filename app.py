from flask import Flask, jsonify, make_response, request, url_for

app = Flask(__name__)

states = [
	{
		'id': 1,
		'title': u'StartTop',
		'description': u'All wires to highest position',
		'commands': {
			'nano1': {
				'motor1': '1 highest_position',
				'motor2': '2 highest_position',
				'motor3': '3 highest_position',
				'motor4': '4 highest_position'
			},
			'nano2': {
				'motor1': '1 highest_position',
				'motor2': '2 highest_position',
				'motor3': '3 highest_position',
				'motor4': '4 highest_position'
			}
		}
	},
	{
		'id': 2,
		'title': u'StartBottom',
		'description': u'All wires to lowest position',
		'commands': {
			'nano1': {
				'motor1': '-1 lowest_position',
				'motor2': '-2 lowest_position',
				'motor3': '-3 lowest_position',
				'motor4': '-4 lowest_position'
			},
			'nano2': {
				'motor1': '-1 lowest_position',
				'motor2': '-2 lowest_position',
				'motor3': '-3 lowest_position',
				'motor4': '-4 lowest_position'
			}
		}
	}
]

actual_state_id = 1

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
		'commands': request.json['commands']
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
	if 'commands' in request.json and type(request.json['commands']) is not unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
	state['title'] = request.json.get('title', state['title'])
	state['description'] = request.json.get('description', state['description'])
	state['commands'] = request.json.get('commands', state['commands'])
	return jsonify({'state': state})

@app.route('/cacau/api/v1.0/states/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
	state = [state for state in states if state['id'] == state_id][0]
	if len(state) == 0:
		abort(404)
	states.remove(state)
	return jsonify({'result': True})

@app.route('/cacau/api/v1.0/state', methods=['GET'])
def get_actual_state():
	state = [state for state in states if state['id'] == actual_state_id][0]
	if len(state) == 0:
		abort(404)
	return jsonify({'state': make_public_state(state)})

@app.route('/cacau/api/v1.0/state', methods=['POST'])
def update_actual_state():
	global actual_state_id
	if not request.json:
		abort(400)
	if 'id' in request.json and request.json['id'] <= states[-1]['id']:
		actual_state_id = request.json['id']
	elif 'commands' in request.json:
		actual_state_id = [state for state in states if state['commands'] == request.json['commands']][0]['id']
	elif 'title' in request.json:
		actual_state_id = [state for state in states if state['title'] == request.json['title']][0]['id']
	else:
		abort(400)
	if actual_state_id < 1:
		actual_state_id = 1
	return get_state(actual_state_id)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)

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