from flask import Flask, request, jsonify
import datetime
import uuid
from http import HTTPStatus
import math

from consts import *

app = Flask(__name__)

# In-memory store (for now)
tickets = {}  # ticket_id: {plate, parking_lot, entry_time}


@app.route('/entry', methods=['POST'])
def entry():
    plate = request.args.get('plate')
    parking_lot = request.args.get('parkingLot')

    if not plate or not parking_lot:
        return jsonify({'error': 'Missing plate or parkingLot'}), HTTPStatus.BAD_REQUEST

    ticket_id = str(uuid.uuid4())
    tickets[ticket_id] = {
        'plate': plate,
        'parking_lot': parking_lot,
        'entry_time': datetime.datetime.now(datetime.UTC)
    }

    return jsonify({'ticketId': ticket_id}), HTTPStatus.OK


@app.route('/exit', methods=['POST'])
def exit():
    ticket_id = request.args.get('ticketId')

    if not ticket_id:
        return jsonify({'error': 'Missing ticketId'}), HTTPStatus.BAD_REQUEST

    if ticket_id not in tickets:
        return jsonify({'error': 'Invalid ticketId'}), HTTPStatus.NOT_FOUND

    record = tickets.pop(ticket_id)
    now = datetime.datetime.now(datetime.UTC)
    duration = now - record['entry_time']
    total_minutes = duration.total_seconds() // 60
    units = math.ceil(total_minutes / MINUTES_PER_UNIT)
    charge = units * RATE_PER_UNIT

    return jsonify({
        'plate': record['plate'],
        'parkingLot': record['parking_lot'],
        'totalTimeMinutes': total_minutes,
        'charge': round(charge, 2)
    }), HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)
