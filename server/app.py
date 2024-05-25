from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()

    if request.method == 'GET':
        messages_list = []
        for message in messages:
            messages_list.append(message.to_dict())
        
        response = make_response(messages_list, 200)
        return response
    elif request.method == 'POST':
        json_data = request.get_json()
        new_message = Message(
            body = json_data['body'],
            username = json_data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(new_message_dict, 201)
        return response

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        json_data = request.get_json()
        for attr in json_data:
            setattr(message, attr, json_data[f'{attr}'])
        
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(message_dict, 200)
        return response

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "message_deleted": True,
            "message": "Message deleted"
        }

        response = make_response(response_body, 200)
        return response

        

if __name__ == '__main__':
    app.run(port=5555)
