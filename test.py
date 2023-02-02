from flask import Flask,jsonify,request
from flask_restx import Api, Resource,fields
from flask_sqlalchemy import SQLAlchemy
import os
from passlib.hash import sha256_crypt
from passlib.hash import sha256_crypt


basedir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=True

api=Api(app,doc='/',title="A user API", description="A simple REST API for books")


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.String(1000), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)


    def __repr__(self):
        return self.username


user_model = api.model(
    'User',
    {
        'id': fields.String(),
        'username': fields.String(),
        'email': fields.String(),
        'password': fields.String(),
    }
)



@api.route('/users')
class User(Resource):
    @api.marshal_list_with(user_model,code=200,envelope="users")
    def get(self):
        ''' Get all users '''
        users = User.query.all()
        return users

    @api.marshal_with(user_model, code=201, envelope="user")
    def post(self):
        ''' Create a new user '''
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        id = data.get('id')
        password = data.get('password')

        print("----------------------------------------------------------------------------", id)

        new_book = User(username = username, email = email, id = id, password = password)

        db.session.add(new_book)

        db.session.commit()

        return new_book


@api.route('/user/<int:id>')
class UserResource(Resource):

    @api.marshal_with(user_model,code=200, envelope="user")
    def get(self,id):

        ''' Get a user by id '''
        user = User.query.get_or_404(id)

        return user, 200

    @api.marshal_with(user_model,envelope="book",code=200)
    def put(self,id):

        ''' Update a book'''
        user_to_update = User.query.get_or_404(id)

        data = request.get_json()

        user_to_update.username = data.get('username')

        user_to_update.email = data.get('email')

        db.session.commit()

        return user_to_update, 200

    @api.marshal_with(user_model, envelope="user_deleted", code=200)
    def delete(self, id):
        '''Delete a user'''
        user_to_delete=User.query.get_or_404(id)

        db.session.delete(user_to_delete)

        db.session.commit()

        return user_to_delete,200


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User
    }

if __name__ == "__main__":
    app.run(port=3000, debug=True)