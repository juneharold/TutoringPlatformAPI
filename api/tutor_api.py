from flask import Blueprint, request, jsonify
from models.models import db, Time, Tutor
from datetime import datetime, timedelta
from utils.validators import validate_tutor_data
from utils.checkers import check_start_time_overlap

tutor_api = Blueprint('tutor_api', __name__)


@tutor_api.route('/add_time', methods=["POST"])
def add_time():
    """
    Adds one or more available time-slots to the requested tutor.
    :returns: an error or a success response in json
    """
    # Parse incoming request data
    data = request.get_json()
    validation_error = validate_tutor_data(data)
    if validation_error:
        return validation_error

    # Extract start time, end time, and tutor from data
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
    tutor = Tutor.query.get(data['tutor_id'])

    # Add time-slots between the given start time and end time
    # (if there wasn't one already and there isn't a registered class)
    now_time, delta = start_time, timedelta(minutes=30)
    while now_time < end_time:
        if not check_start_time_overlap(tutor.id, now_time):
            current_time_slot = Time(start_time=now_time, tutor_id=tutor.id)
            db.session.add(current_time_slot)
        now_time += delta

    db.session.commit()

    # Return success response
    return jsonify(
        {"message": "Available time added successfully.", "start_time": start_time, "end_time": end_time}), 201


@tutor_api.route('/delete_time', methods=["DELETE"])
def delete_time():
    """
    Removes available times that the tutor has listed
    :returns: an error or a success response in json
    """
    # Parse incoming request data
    data = request.get_json()
    validation_error = validate_tutor_data(data)
    if validation_error:
        return validation_error

    # Extract start time and tutor from data
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
    tutor = Tutor.query.get(data['tutor_id'])

    # Find and delete matching Class records
    matching_classes = Time.query.filter(Time.tutor_id == tutor.id,
                                         Time.start_time >= start_time,
                                         Time.start_time < end_time).all()
    for current_class in matching_classes:
        db.session.delete(current_class)
    db.session.commit()

    # Return success response
    return jsonify(
        {"message": "Available time removed successfully.", "start_time": start_time, "end_time": end_time}), 200
