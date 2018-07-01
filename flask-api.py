from flask import Flask,Response, stream_with_context
from flask_restful import reqparse, abort, Resource, Api
from flask_restful.utils import cors
import requests


app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    @cors.crossdomain(origin='vantoan.me')
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

class ProxyHttp(Resource):
    @cors.crossdomain(origin='*')
    def get(self,url):
        """ Request to this like /p/www.google.com
        """
        # url = 'http://{}'.format(url)
        r = get_response(url)
        print("TEST_PROXY")
        responseD = Response(stream_with_context(r.iter_content()), 
                        content_type=r.headers['content-type'])
        print(responseD)
        return responseD

def get_response(target_url):
    print(target_url)

    proxies = {
        'http': 'http://botnlu:toanloc96%23_@206.189.94.233:3128',
        'https': 'http://botnlu:toanloc96%23_@206.189.94.233:3128',
    }
    return requests.get(target_url, proxies=proxies)

class DemoUrl(Resource):
    def get(self, url):
        # requests_function = method_requests_mapping[flask.request.method]
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        request = requests.get(url, headers=headers, stream=True)
        response = Response(stream_with_context(request.iter_content()),
                                content_type=request.headers['content-type'],
                                status=request.status_code)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(ProxyHttp, '/proxy/<path:url>')
api.add_resource(DemoUrl, '/url/<path:url>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')