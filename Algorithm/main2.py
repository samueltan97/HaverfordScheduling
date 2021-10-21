
def does_conflict(first_slot, second_slot):
    """

    :param first_slot: Timeslot Object
    :param second_slot: Timeslot Object
    :return: Whether or not they conflict. (Assuming second slot starts after first slot.)
    """

    if first_slot.start_time < second_slot.end_time:
        return True
    else:
        return False


def interval_scheduling(matches, preferences):
    """

    :param preferences: List[Class] the classes that some student s wishes to take.
    :return: a list of classes, representing their optimal schedule without conflicts.

    """

    scheduled = []
    sorted_preferences = sorted(preferences, key=lambda class_name: matches[class_name]["time_slot"].end_time)
    previous_class = None
    for current_class in preferences:
        previous_time_slot = matches[previous_class]["time_slot"]
        current_time_slot = matches[current_class]["time_slot"]

        if not does_conflict(previous_time_slot, current_time_slot):
            scheduled.append(current_class)
            previous_class = current_class.copy()

    return scheduled


def enroll_students(matches, S, R, T):
    """

    :param matches: Dictionary of dictionaries containing rooms, timeslots, professors assigned to each class.
    :param S: List[Student]
    :param R: List[Room]
    :param T: List[TimeSlot]
    :return: # of classes we were able to enroll students in.
    """
    room_capacities = {}
    score = 0

    for room in R:
        room_capacities[room] = {}
        for timeslot in T:
            room_capacities[room][timeslot] = room.capacity

    for student in S:
        enrolled_classes = interval_scheduling(matches, student.preferences)

        for desired_class in enrolled_classes:  # Attempt to enroll student in each class from interval scheduling.
            room = matches[desired_class]["room"]
            timeslot = matches[desired_class]["timeslot"]
            if room_capacities[room][timeslot] > 0:  # There is still room in this class.
                score += 1
                room_capacities[room][timeslot] -= 1
    return score



