from flask import Flask, request, jsonify
import datetime
import uuid
from http import HTTPStatus
import math

from consts import *
from tickets_manager import save_ticket, get_active_ticket, mark_ticket_inactive

app = Flask(__name__)


@app.route('/entry', methods=['POST'])
def entry():
    plate = request.args.get('plate')
    parking_lot = request.args.get('parkingLot')

    if not plate or not parking_lot:
        return jsonify({'error': 'Missing plate or parkingLot'}), HTTPStatus.BAD_REQUEST

    ticket_id = str(uuid.uuid4())
    entry_time = datetime.datetime.now(datetime.UTC)

    save_ticket(ticket_id, plate, parking_lot, entry_time)

    return jsonify({'ticketId': ticket_id}), HTTPStatus.OK


@app.route('/exit', methods=['POST'])
def exit():
    ticket_id = request.args.get('ticketId')

    if not ticket_id:
        return jsonify({'error': 'Missing ticketId'}), HTTPStatus.BAD_REQUEST

    record = get_active_ticket(ticket_id)

    if not record:
        return jsonify({'error': 'Invalid or already used ticketId'}), HTTPStatus.NOT_FOUND

    entry_time = datetime.datetime.fromisoformat(record['entry_time'])
    now = datetime.datetime.now(datetime.UTC)
    duration = now - entry_time
    total_minutes = duration.total_seconds() // 60
    units = math.ceil(total_minutes / MINUTES_PER_UNIT)
    charge = units * RATE_PER_UNIT

    mark_ticket_inactive(ticket_id)

    return jsonify({
        'plate': record['plate'],
        'parkingLot': record['parking_lot'],
        'totalTimeMinutes': int(total_minutes),
        'charge': round(charge, 2)
    }), HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)
