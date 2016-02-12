"""
This script runs the DesafioConcreteSolutions application using a development server.
"""

from os import environ
from DesafioConcreteSolutions import app, api, rest

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000

    api.add_resource(rest.UsersRestGet, '/<string:user_id>')
    api.add_resource(rest.UsersRestPost, '/')
    api.add_resource(rest.UsersRestLogin, '/login/')
    api.add_resource(rest.UsersRestProfile, '/profile/')
    # app.run(HOST, PORT, debug=True)
    app.run(debug=True)