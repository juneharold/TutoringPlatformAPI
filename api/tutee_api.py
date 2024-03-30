from flask import Blueprint, request, jsonify
from models.models import db, Time, Class, Tutor, Tutee
from datetime import datetime, timedelta
from utils.validators import validate_find_classes_request, validate_find_tutors_request, \
    validate_register_class_request, validate_view_registered_class_request
from utils.checkers import check_class_time_overlap

tutee_api = Blueprint('tutee_api', __name__)


@tutee_api.route('/find_classes', methods=["GET"])
def find_classes():
    """
    Finds time (that any tutor) listed as available between the start_time and end_time requested by tutee
    :return: an error or a success response in json
    """
    # Validate request parameters
    validation_error = validate_find_classes_request(request)
    if validation_error:
        return validation_error

    # Retrieve query parameters
    start_time = datetime.strptime(request.args.get('start_time'), '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(request.args.get('end_time'), '%Y-%m-%d %H:%M:%S')
    duration = request.args.get('duration', type=int)

    # Query for matching classes
    if duration == 60:
        end_time = end_time - timedelta(minutes=30)

    possible_times = Time.query.filter(
        Time.start_time >= start_time,
        Time.start_time < end_time,
    ).all()
    time_list = [{
        'time_id': time.id,
        'start_time': time.start_time.strftime('%Y-%m-%d %H:%M:%S')
    } for time in possible_times]

    # Return response
    return jsonify(time_list)


@tutee_api.route('/find_tutors', methods=["GET"])
def find_tutors():
    """
    Finds tutor that has time available between the start_time and end_time of a day of a certain day of week
    :return: an error or a success response in json
    """
    # Validate query parameters
    validation_error = validate_find_tutors_request(request)
    if validation_error:
        return validation_error

    # Extract query parameters
    days_of_week = request.args.getlist('days_of_week', type=int)  # Expected to be a list of 0s and 1s
    start_hour, start_minute = map(int, request.args.get('start_time').split(':'))
    end_hour, end_minute = map(int, request.args.get('end_time').split(':'))
    duration = int(request.args.get('duration'))

    # Find matching tutors
    matching_tutors = []
    for tutor in Tutor.query.all():
        valid_classes = []
        for cls in tutor.available_times:
            cls_day_of_week = cls.start_time.weekday()

            # Check if the day matches one of the desired days
            if days_of_week[cls_day_of_week] == 1:
                # Check if the time of the class matches the desired start time
                if check_class_time_overlap(start_hour, start_minute, end_hour, end_minute, cls.start_time):
                    valid_classes.append(cls)

        # Check for consecutive classes if duration is 60
        if duration == 60:
            for i in range(len(valid_classes) - 1):
                if (valid_classes[i + 1].start_time - valid_classes[i].start_time) == timedelta(minutes=30):
                    matching_tutors.append(tutor)
                    break
        elif duration == 30 and valid_classes:
            matching_tutors.append(tutor)

    # Serialize the matching tutors to JSON and return response
    tutors_list = [{
        'tutor_id': tutor.id,
        'name': tutor.name,
    } for tutor in matching_tutors]

    return jsonify(tutors_list)


@tutee_api.route('/register_class', methods=["PUT"])
def register_class():
    """
    Tutee registers a class by s specific start_time, duration, and tutor
    :return: an error or a success response in json
    """
    # Parse incoming request
    data = request.get_json()
    validation_error = validate_register_class_request(data)
    if validation_error:
        return validation_error

    # Extract data
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
    duration = data.get('duration')
    tutor_id = data.get('tutor_id')
    tutee_id = data.get('tutee_id')

    # Find the matching time slot of the tutor and add the class
    time_slot = Time.query.filter_by(start_time=start_time, tutor_id=tutor_id).first()
    new_class = Class(start_time=start_time, duration=duration, tutor_id=tutor_id, tutee_id=tutee_id)
    db.session.add(new_class)
    db.session.delete(time_slot)  # Make sure to erase this time_slot from tutor's available times
    db.session.commit()

    # Returns success response
    return jsonify(
        {"message": "Successfully registered for class",
         "class_id": new_class.id,
         "start_time": new_class.start_time,
         "duration": new_class.duration,
         "tutor_id": new_class.tutor_id,
         "tutee_id": new_class.tutee_id,
         })


@tutee_api.route('/view_registered_class', methods=["GET"])
def view_registered_class():
    """
    Shows registered class, when given a tutee id
    :return: an error or a success response in json
    """
    # Validate query parameters
    validation_error = validate_view_registered_class_request(request)
    if validation_error:
        return validation_error

    # Extract tutee_id
    tutee_id = int(request.args.get('tutee_id'))

    # Find registered classes
    registered_classes = Class.query.filter_by(tutee_id=tutee_id).all()

    # Serialize the registered classes to JSON and return response
    classes_list = [{
        'class_id': cls.id,
        'start_time': cls.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'tutor_id': cls.tutor_id
    } for cls in registered_classes]

    return jsonify({"registered_classes": classes_list})
