from flask import Flask
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)

'''
FROM PYTHON
- getBoard
- isRowAvailable

SEND TO FRONT
- sendBoard
- currentPlayer
- isOver

PROCESS
- processMotion (do when have access to API)
- waitingForConfirm
'''

# CLASSES

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# ADDS
# api.add_resource(Resource, urls, endpoint=Resource.__name__.lower())
api.add_resource(HelloWorld, '/')

# RUN
if __name__ == '__main__':
    app.run(debug=True)