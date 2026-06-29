"""Notification service for creating system notifications."""
from app import db
from app.models.notification import Notification


def create_notification(user_id, title, message, notification_type='info'):
    """
    Create and save a new notification for a user.

    Args:
        user_id: The ID of the user to notify.
        title: Short notification title.
        message: Notification body text.
        notification_type: One of 'info', 'success', 'warning', 'error'.
    """
    try:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    except Exception as e:
        db.session.rollback()
        print(f"[NotificationService] Failed to create notification: {e}")
        return None


def notify_loan_applied(farmer_user_id, amount):
    """Notify farmer that loan application was submitted."""
    create_notification(
        farmer_user_id,
        'Loan Application Submitted',
        f'Your loan application for ₹{amount:,.2f} has been submitted successfully. A bank officer will review it shortly.',
        'info'
    )


def notify_loan_approved(farmer_user_id, amount, bank_name):
    """Notify farmer that their loan was approved."""
    create_notification(
        farmer_user_id,
        '🎉 Loan Approved!',
        f'Congratulations! Your loan application for ₹{amount:,.2f} has been approved by {bank_name}.',
        'success'
    )


def notify_loan_rejected(farmer_user_id, amount, remarks):
    """Notify farmer that their loan was rejected."""
    create_notification(
        farmer_user_id,
        'Loan Application Update',
        f'Your loan application for ₹{amount:,.2f} was not approved. Reason: {remarks}',
        'warning'
    )


def notify_query_answered(farmer_user_id, subject):
    """Notify farmer that their query was answered."""
    create_notification(
        farmer_user_id,
        'Query Answered',
        f'An agricultural expert has answered your query: "{subject}". Check the Queries section to view the response.',
        'success'
    )


def notify_complaint_reply(farmer_user_id, subject):
    """Notify farmer that admin replied to their complaint."""
    create_notification(
        farmer_user_id,
        'Complaint Update',
        f'An admin has responded to your complaint: "{subject}". Check the Complaints section for details.',
        'info'
    )


def notify_new_query_to_expert(expert_user_id, farmer_name, subject):
    """Notify expert that a new query has been submitted."""
    create_notification(
        expert_user_id,
        'New Farmer Query',
        f'Farmer {farmer_name} has submitted a new query: "{subject}". Please check the Queries section.',
        'info'
    )


def notify_new_loan_to_bank(bank_user_id, farmer_name, amount):
    """Notify bank officer of a new loan application."""
    create_notification(
        bank_user_id,
        'New Loan Application',
        f'Farmer {farmer_name} has applied for a loan of ₹{amount:,.2f}. Review the application.',
        'info'
    )
