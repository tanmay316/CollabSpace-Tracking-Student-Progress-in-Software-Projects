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


@ta.route('/api/viva_slots', methods=['POST'])
def create_viva_slot():
    data = request.get_json()
    try:
        viva_slot = VivaSlots(
            time=data['time'],
            student_id=data['student_id'],
            examiner_name=data['examiner_name'],
            status=False  # Initially set to False
        )
        db.session.add(viva_slot)
        db.session.commit()
        return jsonify({"message": "Viva slot created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@ta.route('/api/viva_slots', methods=['GET'])
def fetch_viva_slots():
    slots = VivaSlots.query.all()
    result = [{"id": slot.id, "time": slot.time, "student_id": slot.student_id,
               "examiner_name": slot.examiner_name, "status": slot.status} for slot in slots]
    return jsonify(result)


@ta.route('/api/viva_slots/<int:slot_id>', methods=['PUT'])
def update_viva_slot(slot_id):
    data = request.get_json()
    try:
        viva_slot = VivaSlots.query.get(slot_id)
        if viva_slot:
            viva_slot.time = data.get('time', viva_slot.time)
            viva_slot.status = data.get('status', viva_slot.status)
            viva_slot.examiner_name = data.get('examiner_name', viva_slot.examiner_name)
            db.session.commit()
            return jsonify({"message": "Viva slot updated successfully."})
        else:
            return jsonify({"error": "Viva slot not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@ta.route('/api/viva_slots/<int:slot_id>', methods=['DELETE'])
def delete_viva_slot(slot_id):
    try:
        viva_slot = VivaSlots.query.get(slot_id)
        if viva_slot:
            db.session.delete(viva_slot)
            db.session.commit()
            return jsonify({"message": "Viva slot deleted successfully."})
        else:
            return jsonify({"error": "Viva slot not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
