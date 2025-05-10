from typing import Optional, Dict
from datetime import datetime
from google.cloud import firestore

db = firestore.Client()


def save_ticket(ticket_id: str, plate: str, parking_lot: str, entry_time: datetime) -> None:
    """
    Save a new parking ticket to Firestore.

    Args:
        ticket_id (str): Unique ID for the ticket.
        plate (str): License plate number.
        parking_lot (str): Parking lot identifier.
        entry_time (datetime): UTC datetime when the vehicle entered.
    """
    db.collection('tickets').document(ticket_id).set({
        'plate': plate,
        'parking_lot': parking_lot,
        'entry_time': entry_time.isoformat(),
        'status': 'active'
    })


def get_active_ticket(ticket_id: str) -> Optional[Dict[str, str]]:
    """
    Retrieve an active ticket from Firestore by its ID.

    Args:
        ticket_id (str): The ticket's unique ID.

    Returns:
        dict: Ticket data (plate, parking_lot, entry_time, status) if active.
        None: If the ticket doesn't exist or is not active.
    """
    ref = db.collection('tickets').document(ticket_id)
    doc = ref.get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    if data.get('status') != 'active':
        return None
    return data


def mark_ticket_inactive(ticket_id: str) -> None:
    """
    Mark a ticket as inactive in Firestore (soft-delete).

    Args:
        ticket_id (str): The ID of the ticket to update.
    """
    db.collection('tickets').document(ticket_id).update({
        'status': 'inactive'
    })
