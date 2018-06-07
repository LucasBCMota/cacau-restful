from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

states = [
	{
		'id': 1,
		'title': u'AB',
		'description': u'Sobe ate limite',
		'command': 1
	},
	{
		'id': 2,
		'title': u'BA',
		'description': u'Desce e sobe',
		'command': 2
	}
]

@app.route('/')
def index():
	return "Hello World!"

@app.route('/cacau/api/v1.0/states', methods=['GET'])
def get_states():
	return jsonify({'states': states})

@app.route('/cacau/api/v1.0/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
	state = [state for state in states if state['id'] == state_id]
	if len(state) == 0:
		abort(404)
	return jsonify({'state': state[0]})

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

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug=True)