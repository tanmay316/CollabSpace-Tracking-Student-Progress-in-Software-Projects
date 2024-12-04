from app import celery  # Import only the Celery instance

@celery.task
def send_reminder_emails(name='send_reminder_emails'):
    from flask_mail import Message
    from models import Milestones, Users
    from datetime import datetime, timedelta

    today = datetime.today().date()
    reminder_date = today + timedelta(days=1)

    with celery.app.app_context():
        milestones = Milestones.query.filter(Milestones.deadline == reminder_date).all()
        for milestone in milestones:
            users = Users.query.all()
            for user in users:
                msg = Message(
                    subject=f"Reminder: Milestone '{milestone.title}' Due Tomorrow!",
                    sender='noreply@example.com',
                    recipients=[user.email],
                    body=f"Hello {user.first_name},\n\n"
                         f"Milestone '{milestone.title}' is due tomorrow.\n"
                         f"Description: {milestone.description}\nDeadline: {milestone.deadline}\n\n"
                         f"Best regards,\nYour Team"
                )
                mail.send(msg)
                print(f"Sent reminder to {user.email}")
