from flask import Blueprint, request, jsonify
from models import *
from datetime import datetime

ta = Blueprint("ta", __name__)

@ta.route('/api/doubts', methods=['GET'])
def get_doubts():
    doubts = StudentDoubts.query.all()
    doubt_list = []
    for doubt in doubts:
        student = Users.query.get(doubt.student_id)
        doubt_list.append({
            'doubt_id': doubt.id,
            'student_name': f"{student.first_name} {student.last_name}",
            'doubt': doubt.doubt,
            'status': 'answered' if doubt.response else 'pending',
            'created_at': doubt.created_at.isoformat()
        })
    return jsonify(doubt_list)

@ta.route('/api/chat/ta', methods=['GET'])
def get_chat_history():
    student_id = request.args.get('student_id')
    ta_id = request.args.get('ta_id')
    chat_history = ChatbotInteractions.query.filter(
        (ChatbotInteractions.user_id == student_id) | (ChatbotInteractions.user_id == ta_id)
    ).order_by(ChatbotInteractions.created_at).all()
    
    messages = [
        {'query': interaction.query, 'response': interaction.response, 'timestamp': interaction.created_at.isoformat()}
        for interaction in chat_history
    ]
    return jsonify({'messages': messages})

@ta.route('/api/chat/ta', methods=['POST'])
def send_message():
    data = request.json
    new_message = ChatbotInteractions(
        user_id=data['ta_id'],
        query=data['message'],
        response=data['response'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'}), 201
