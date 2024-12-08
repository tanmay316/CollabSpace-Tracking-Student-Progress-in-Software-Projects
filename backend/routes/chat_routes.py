from flask import Blueprint, request, jsonify
from models import db, Users, Conversations, Messages
from flask_cors import CORS

chat = Blueprint("chat", __name__)
CORS(
    chat, resources={r"/api/chat/*": {"origins": "*"}}
)  # Enable CORS for this Blueprint


@chat.route("/users", methods=["GET"])
def get_users():
    current_user_id = request.args.get("current_user_id")
    if not current_user_id:
        return jsonify({"error": "current_user_id is required"}), 400
    try:
        current_user_id_int = int(current_user_id)
    except ValueError:
        return jsonify({"error": "current_user_id must be an integer"}), 400

    current_user = Users.query.get(current_user_id_int)

    if not current_user:
        return jsonify({"error": "User not found"}), 404

    if current_user.role == "student":
        # Show TAs and Instructors to the student
        users = Users.query.filter(Users.role.in_(["ta", "instructor"])).all()
    elif current_user.role in ["ta", "instructor"]:
        # Show students to the TA/Instructor
        users = Users.query.filter(Users.role == "student").all()
    else:
        return jsonify({"error": "Invalid role"}), 400

    user_list = [
        {
            "id": user.id,
            "name": f"{user.first_name} {user.last_name}",
            "role": user.role,
            "email": user.email,
            
        }
        for user in users
    ]

    return jsonify(user_list), 200


@chat.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    print(f"Received Data: {data}")  # Log received data

    sender_id = data.get("sender_id")
    receiver_id = data.get("receiver_id")
    message = data.get("message")

    # Check if any required field is missing
    if not sender_id or not receiver_id or not message:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        sender_id_int = int(sender_id)
        receiver_id_int = int(receiver_id)
    except ValueError:
        return jsonify({"error": "sender_id and receiver_id must be integers"}), 400

    # Ensure sender and receiver are valid users
    sender = Users.query.get(sender_id_int)
    receiver = Users.query.get(receiver_id_int)

    if not sender or not receiver:
        return jsonify({"error": "Invalid sender or receiver"}), 400

    # Create and save the message
    new_message = Messages(
        sender_id=sender_id_int, receiver_id=receiver_id_int, message=message
    )
    db.session.add(new_message)

    # Update conversation last message
    conversation = Conversations.query.filter(
        (
            (Conversations.user1_id == sender_id_int)
            & (Conversations.user2_id == receiver_id_int)
        )
        | (
            (Conversations.user1_id == receiver_id_int)
            & (Conversations.user2_id == sender_id_int)
        )
    ).first()

    if conversation:
        conversation.last_message = message
        conversation.last_updated = new_message.timestamp
    else:
        new_conversation = Conversations(
            user1_id=sender_id_int, user2_id=receiver_id_int, last_message=message
        )
        db.session.add(new_conversation)

    db.session.commit()

    return jsonify({"message": "Message sent successfully"}), 200


@chat.route("/get_messages", methods=["GET"])
def get_messages():
    sender_id = request.args.get("sender_id")
    receiver_id = request.args.get("receiver_id")

    # Log sender_id and receiver_id for debugging
    print(f"Received sender_id: {sender_id}, receiver_id: {receiver_id}")

    if not sender_id or not receiver_id:
        return jsonify({"error": "Sender ID and Receiver ID are required"}), 400

    try:
        sender_id_int = int(sender_id)
        receiver_id_int = int(receiver_id)
    except ValueError:
        return jsonify({"error": "sender_id and receiver_id must be integers"}), 400

    sender = Users.query.get(sender_id_int)
    receiver = Users.query.get(receiver_id_int)

    if not sender or not receiver:
        return jsonify({"error": "Invalid sender or receiver"}), 400

    # Get messages between the sender and receiver
    messages = (
        Messages.query.filter(
            (
                (Messages.sender_id == sender_id_int)
                & (Messages.receiver_id == receiver_id_int)
            )
            | (
                (Messages.sender_id == receiver_id_int)
                & (Messages.receiver_id == sender_id_int)
            )
        )
        .order_by(Messages.timestamp.asc())
        .all()
    )

    # Prepare response data
    messages_data = [
        {
            "id": msg.id,
            "sender_id": msg.sender_id,
            "receiver_id": msg.receiver_id,
            "message": msg.message,
            "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "isSent": msg.sender_id == sender_id_int,
        }
        for msg in messages
    ]

    return jsonify({"messages": messages_data}), 200


# @chat.route("/conversations/<int:user_id>", methods=["GET"])
# def get_conversations(user_id):
#     conversations = Conversations.query.filter(
#         (Conversations.user1_id == user_id) | (Conversations.user2_id == user_id)
#     ).all()
#     response = []
#     for conv in conversations:
#         other_user_id = conv.user1_id if conv.user2_id == user_id else conv.user2_id
#         other_user = Users.query.get(other_user_id)
#         response.append(
#             {
#                 "conversation_id": conv.id,
#                 "other_user": {
#                     "id": other_user.id,
#                     "name": f"{other_user.first_name} {other_user.last_name}",
#                     "email": other_user.email,
#                     "role": other_user.role,
#                 },
#                 "last_message": conv.last_message,
#                 "last_updated": conv.last_updated,
#             }
#         )
#     return jsonify(response)


# @chat.route("/messages", methods=["POST"])
# def send_message():
#     data = request.json
#     sender_id = data["sender_id"]
#     receiver_id = data["receiver_id"]
#     message_text = data["message"]

#     # Add message
#     new_message = Messages(
#         sender_id=sender_id, receiver_id=receiver_id, message=message_text
#     )
#     db.session.add(new_message)

#     # Update or create conversation
#     conversation = Conversations.query.filter(
#         (
#             (Conversations.user1_id == sender_id)
#             & (Conversations.user2_id == receiver_id)
#         )
#         | (
#             (Conversations.user1_id == receiver_id)
#             & (Conversations.user2_id == sender_id)
#         )
#     ).first()
#     if not conversation:
#         conversation = Conversations(user1_id=sender_id, user2_id=receiver_id)
#         db.session.add(conversation)
#     conversation.last_message = message_text
#     db.session.commit()

#     return jsonify({"success": True, "message": "Message sent."})
