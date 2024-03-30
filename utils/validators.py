"""
All functions here checks if the incoming data/request is in valid format to perform the request.
"""
from models.models import *
from flask import jsonify
from datetime import datetime, timedelta


def validate_tutor_data(data):
    # Check for required fields
    required_fields = ['start_time', 'end_time', 'tutor_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Try to parse the start and end times
    try:
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(data['end_time'], '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        return jsonify({"error": "Invalid date format, expected 'YYYY-MM-DD HH:MM:SS'."}), 400

    # Validate start_time is before end_time
    if start_time >= end_time:
        return jsonify({"error": "start_time must be before end_time."}), 400

    # Check if tutor_id is valid
    tutor_id = data.get('tutor_id')
    if tutor_id is not None:
        try:
            tutor_id = int(tutor_id)  # Ensure tutor_id can be cast to an integer
        except ValueError:
            return jsonify({"error": "tutor_id must be an integer."}), 400

        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return jsonify({"error": "Tutor with provided tutor_id does not exist."}), 404

    return None  # Indicates that validation passed


def validate_find_classes_request(request):
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')
    duration_str = request.args.get('duration')

    # Check for missing parameters
    if not all([start_time_str, end_time_str, duration_str]):
        missing = [param for param in ["start_time", "end_time", "duration"] if not request.args.get(param)]
        return jsonify({"error": f"Missing required parameters: {', '.join(missing)}"}), 400

    # Validate and convert start_time and end_time
    try:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid datetime format for start_time or end_time. Use 'YYYY-MM-DD HH:MM:SS'."}), 400

    # Validate start_time is before end_time
    if start_time >= end_time:
        return jsonify({"error": "start_time must be before end_time."}), 400

    # Validate duration is an integer and either 30 or 60
    try:
        duration = int(duration_str)
        if duration not in [30, 60]:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid duration. Must be 30 or 60."}), 400

    # If all validations pass, return None
    return None


def validate_find_tutors_request(request):
    # Attempt to extract and validate days_of_week, start_time, end_time, and duration from request
    try:
        days_of_week = request.args.getlist('days_of_week', type=int)
        if not all(day in [0, 1] for day in days_of_week) or len(days_of_week) != 7:
            raise ValueError("Invalid days_of_week format. Expected a list of 7 integers (0 or 1).")

        start_time_parts = [int(part) for part in request.args.get('start_time').split(':')]
        end_time_parts = [int(part) for part in request.args.get('end_time').split(':')]
        if any(part < 0 or part >= 60 for part in start_time_parts[1:] + end_time_parts[1:]) or \
                any(part < 0 or part >= 24 for part in [start_time_parts[0], end_time_parts[0]]):
            raise ValueError("Invalid time format for start or end time.")

        duration = int(request.args.get('duration'))
        if duration not in [30, 60]:
            raise ValueError("Invalid duration. Must be 30 or 60.")

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # All validations passed, return None indicating no error
    return None


def validate_register_class_request(data):
    # Check for missing fields
    required_fields = ['start_time', 'duration', 'tutor_id', 'tutee_id']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    # Validate start_time format
    try:
        start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"error": "Invalid start_time format, expected 'YYYY-MM-DD HH:MM:SS'."}), 400

    # Validate duration
    if data['duration'] not in [30, 60]:
        return jsonify({"error": "Invalid duration. Must be 30 or 60."}), 400

    # Validate tutor_id
    if not Tutor.query.get(data['tutor_id']):
        return jsonify({"error": "Tutor not found"}), 404

    # Validate tutee_id
    if not Tutee.query.get(data['tutee_id']):
        return jsonify({"error": "Tutee not found"}), 404

    # Calculate the end time of the new class based on the duration
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
    end_time = start_time + timedelta(minutes=data['duration'])

    # Check for overlapping classes
    classes = Class.query.filter(
        Class.tutor_id == data['tutor_id'],
        Class.start_time < end_time
    ).all()
    overlapping_classes = [
        cls for cls in classes
        if cls.start_time + timedelta(minutes=cls.duration) > start_time
    ]
    if overlapping_classes:
        return jsonify({"error": "Time slot overlaps with an existing class."}), 409

    # Check if the class times are available
    time_to_register1 = Time.query.filter_by(tutor_id=data['tutor_id'], start_time=start_time).first()
    time_to_register2 = None
    if data['duration'] == 60:
        end_time = start_time + timedelta(minutes=30)
        time_to_register2 = Time.query.filter_by(tutor_id=data['tutor_id'], start_time=end_time).first()

    if not time_to_register1 or (data['duration'] == 60 and not time_to_register2):
        return jsonify({"error": "Tutor's time slot is not available"}), 404

    time_slot = Time.query.filter_by(start_time=start_time, tutor_id=data['tutor_id']).first()
    if not time_slot:
        return jsonify({"error": "Tutor's time slot is not available."}), 404

    return None  # Indicate that validation passed


def validate_view_registered_class_request(request):
    # Attempt to extract and validate tutee_id from request
    try:
        tutee_id = request.args.get('tutee_id', type=int)
        if not tutee_id:
            raise ValueError("Missing tutee_id.")

        # Check if the Tutee exists
        tutee = Tutee.query.get(tutee_id)
        if not tutee:
            raise ValueError("Tutee not found.")

    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    # All validations passed, return None indicating no error
    return None