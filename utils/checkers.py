from models.models import Time, Class
from datetime import timedelta


def check_start_time_overlap(tutor_id, now_time):
    """
    :return: (Boolean) True if there is no need to add the current time-slot, False otherwise
    """
    # Check if there is already the same time-slot that the tutor's trying to add
    overlap_with_available = Time.query.filter(
        Time.tutor_id == tutor_id,
        Time.start_time == now_time,
    ).first() is not None

    # Check if the time overlaps with any registered classes
    classes = Class.query.filter(
        Class.tutor_id == tutor_id,
        Class.start_time <= now_time
    ).all()
    filtered_classes = [
        cls for cls in classes
        if cls.start_time + timedelta(minutes=cls.duration) > now_time
    ]

    return overlap_with_available or filtered_classes


def check_class_time_overlap(start_hour, start_minute, end_hour, end_minute, class_start_time):
    """
    Used to check if time-slot of tutor matches that requested by the tutee
    :return: (Boolean) True if time-slot matches, False otherwise
    """
    # Check if class_start_time is after or exactly at the start time
    after_start = (class_start_time.hour > start_hour or
                   (class_start_time.hour == start_hour and class_start_time.minute >= start_minute))

    # Check if class_start_time is before the end time
    before_end = (class_start_time.hour < end_hour or
                  (class_start_time.hour == end_hour and class_start_time.minute < end_minute))

    # The class time overlaps if it's after the start and before the end
    return after_start and before_end

