from flask import Flask
from flask_restx import Api # type: ignore

app = Flask(__name__)
api = Api(app)

@api.route('/hello')
class HelloWorldResource:
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)
