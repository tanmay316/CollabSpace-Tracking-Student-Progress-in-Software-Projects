from celery import shared_task
from mail_service import send_email
from models import Milestones, Users
from datetime import datetime, timedelta

@shared_task(ignore_result=True)
def send_deadline_reminder():
    today = datetime.today().date()
    reminder_date = today + timedelta(days=1)

    milestones = Milestones.query.filter(Milestones.deadline == reminder_date).all()
    
    for milestone in milestones:
        users = Users.query.all()
        for user in users:
            message = f"""
                <html>
                    <body>
                        <h2 style="color: #2C3E50; font-family: Arial, sans-serif;">Hello {user.first_name},</h2>
                        <p style="font-family: Arial, sans-serif; font-size: 16px;">
                            We hope you're doing well! We wanted to remind you that the following milestone is due tomorrow:
                        </p>

                        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                            <tr>
                                <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Milestone</th>
                                <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Description</th>
                                <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Deadline</th>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #BDC3C7;">{milestone.title}</td>
                                <td style="padding: 10px; border: 1px solid #BDC3C7;">{milestone.description}</td>
                                <td style="padding: 10px; border: 1px solid #BDC3C7;">{milestone.deadline}</td>
                            </tr>
                        </table>

                            <p style="font-family: Arial, sans-serif; font-size: 16px; margin-top: 20px;">
                                Please make sure to complete it on time. If you have any questions, feel free to reach out.
                            </p>
    
                            <p style="font-family: Arial, sans-serif; font-size: 16px;">
                                Best regards,<br>
                                <strong>Collabspace</strong>
                            </p>
                    </body>
                </html>
                """
            send_email(user.email, "Reminder: Your Book deadline is near", message)
    
    return "Done!"
                
                
                

