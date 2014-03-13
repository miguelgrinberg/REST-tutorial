#!flask/bin/python

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension and using MongoDB via pymongo for storing tasks."""

from flask import Flask, abort
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
api = Api(app)

# setting up access to MongoDB
client = MongoClient("localhost")
database = client.taskapi
tasks = database.tasks
 

# helper structure for the marshaling of JSON objects
task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task', absolute=True)
}


class TaskListAPI(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True, help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = "", location = 'json')
        super(TaskListAPI, self).__init__()
    
    
    def get(self):
        tasks_array=[]
        for task in tasks.find():
            # Set the 'id' attribute as the string representation of the ObjectId in the database (needed to properly reference the 'task' endpoint)
            task['id'] = str(task['_id'])
            tasks_array.append(task)
        return { 'tasks': marshal(tasks_array, task_fields) }

    def post(self):
        args = self.reqparse.parse_args()
                
        task = {
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        
        tasks.insert(task);
        
        # Set the 'id' attribute as the string representation of the ObjectId in the database (needed to properly reference the 'task' endpoint)
        task['id'] = str(task['_id'])
        response = marshal(task, task_fields)
        
        return {'task' : response}, 201, {'Location' : response['uri']}
    
    
class TaskAPI(Resource):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        
        
    def get(self, id):
                
        task = tasks.find_one({"_id": ObjectId(id)});

        if task == None:
            abort(404)
        
        # Set the 'id' attribute as the string representation of the ObjectId in the database (needed to properly reference the 'task' endpoint)
        task['id'] = str(task['_id'])
        return {'task' : marshal(task, task_fields)}

    def put(self, id):
        
        # parse the arguments
        args = self.reqparse.parse_args()
        
        # remove arguments that are optional or which value is None or Null, so that these do not overwrite existing values in the database
        for k, v in args.items():
            if args[k] == None:
                args.pop(k)
        
        # Find and modify the task
        task = tasks.find_and_modify(query={"_id": ObjectId(id)}, update={"$set": args}, new=True)
        
        # Set the 'id' attribute as the string representation of the ObjectId in the database (needed to properly reference the 'task' endpoint)
        task['id'] = str(task['_id'])

        # return the task in marshaled in JSON format
        return {'task' : marshal(task, task_fields)}

    def delete(self, id):
        tasks.remove({"_id": ObjectId(id)});
        return "", 204;

api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint = 'tasks')
# note that the type of "id" is now a string instead of an integer (since mongo object IDs are strings)
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<string:id>', endpoint = 'task')



if __name__ == '__main__':
    app.run(debug = True)


