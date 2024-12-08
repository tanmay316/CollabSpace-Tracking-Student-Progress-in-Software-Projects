from flask import Blueprint, request, jsonify
from models import db, Users, Conversations, Messages

chat = Blueprint("chat", __name__)

@chat.route('/conversations/<int:user_id>', methods=['GET'])
def get_conversations(user_id):
    conversations = Conversation.query.filter((Conversation.user1_id == user_id) | 
                                              (Conversation.user2_id == user_id)).all()
    response = []
    for conv in conversations:
        other_user_id = conv.user1_id if conv.user2_id == user_id else conv.user2_id
        other_user = User.query.get(other_user_id)
        response.append({
            'conversation_id': conv.id,
            'other_user': {
                'id': other_user.id,
                'name': f"{other_user.first_name} {other_user.last_name}",
                'email': other_user.email,
                'role': other_user.role
            },
            'last_message': conv.last_message,
            'last_updated': conv.last_updated
        })
    return jsonify(response)

@chat.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message_text = data['message']
    
    # Add message
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, message=message_text)
    db.session.add(new_message)

    # Update or create conversation
    conversation = Conversation.query.filter(
        ((Conversation.user1_id == sender_id) & (Conversation.user2_id == receiver_id)) |
        ((Conversation.user1_id == receiver_id) & (Conversation.user2_id == sender_id))
    ).first()
    if not conversation:
        conversation = Conversation(user1_id=sender_id, user2_id=receiver_id)
        db.session.add(conversation)
    conversation.last_message = message_text
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Message sent.'})