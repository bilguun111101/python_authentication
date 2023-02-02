from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

basedir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

api = Api(app)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(40), nullable = False)
    password = db.Column(db.String(40), nullable = False)
    date_added = db.Column(db.DateTime(), default = datetime.utcnow)
    
    def __repr__(self):
        return self.email
    
user_model = api.model(
    'User',
    {
        'id': fields.Integer(),
        'name': fields.String(),
        'email': fields.String(),
        'password': fields.String(),
        'date_joined': fields.String()
    }
)


@api.route('/users')
class Books(Resource):
    
    @api.marshal_list_with(user_model,code=200,envelope="users")
    def get(self):
        users = User.query.all()
        return users
    
    @api.marshal_with(user_model,code=201,envelope="user")
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        new_user = User(email = email, author = name, password = password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    

@api.route('/book/<int:id>')
class UserResource(Resource):
    @api.marshal_with(user_model,code=200,envelope="book")
    def get(self, id):
        user = User.query.get_or_404(id)
        return user
    def put(self, id):
        pass
    def delete(self, id):
        pass
    
    

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User
    }
    
if __name__ == "__main__":
    app.run(debug=True)