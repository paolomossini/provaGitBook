#!home/paolo/flask/bin/python
from flask import Flask, jsonify, abort
from flask import request
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth();
app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@auth.get_password
def get_password(username):
	if username == 'Paolo':
		return 'PaoloPassword'
	return None

@auth.error_handler
def unauthorized():
	return jsonify({'error': 'Unauthorized'})

@app.route('/')
@auth.login_required
def index():
	print('Hello World!\n')
	return "Hello World!\n"

@app.route('/postjson', methods=['POST'])
def post():
	#Stampa true se la request e' un json
	print(request.is_json)
	content = request.get_json()
	print(content['id'])
	print(content['name'])
	return 'JSON posted'

@app.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
	return jsonify({'tasks': tasks})

@app.route('/newtask', methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
		abort(400)

	task = {
		'id': tasks[-1]['id'] + 1,
		'title': request.json['title'],
		'description': request.json.get('description', ""),
		'done': False
	}
	#content = request.get_json()
	tasks.append(task)
	return jsonify({'tasks': tasks})

@app.route('/gettask/<int:task_id>', methods=['GET'])
def get_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
		abort(400)
	return jsonify({'task': task[0]})

@app.errorhandler(400)
def notfount(error):
	return jsonify({'error': 'Not Found!'})


if __name__ == '__main__':
	app.run(debug = True)
