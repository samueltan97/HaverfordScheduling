from args import parse_args
import os
import re
from objects import TimeSlot, Room


def get_day_format(raw_days):
    if raw_days == "M-F":
        days = ["M", "T", "W", "Th", "F"]
        return days

    days = []
    index = 0
    while index != len(raw_days):
        current_day = raw_days[index]
        if current_day != "T":
            days.append(current_day)
        else:
            if index != len(raw_days) - 1 and raw_days[index+1] == "H":
                days.append("Th")
                index +=1
            else:
                days.append(current_day)
        index += 1

    return days


def parse_timeslots(c_data, num_class_times):
    """

    :param c_data: List[str] -> Each line fo the constraint file.
    :param num_class_times: Int -> Number of time slots to parse.
    :return: TimeSlot Objs.
    """
    timeslots = []
    for timeslot_line in range(1, 1 + num_class_times):
        timeslot_info = c_data[timeslot_line].split()
        id = timeslot_info[0]
        start_is_afternoon = timeslot_info[2] == "PM"
        if start_is_afternoon:
            start_time = int(timeslot_info[1].split(":")[0]) + 12
        else:
            start_time = int(timeslot_info[1].split(":")[0])
        end_is_afternoon = timeslot_info[4] == "PM"

        if end_is_afternoon:
            end_time = int(timeslot_info[3].split(":")[0]) + 12
        else:
            end_time = int(timeslot_info[3].split(":")[0])
        # TODO: Merge labs and normal classes.
        days = get_day_format(timeslot_info[5])
        start_times = [start_time] * len(days)
        end_times = [end_time] * len(days)

        new_slot = TimeSlot(id, days, start_times, end_times)
        timeslots.append(new_slot)

    return timeslots


def parse_rooms(c_data, num_class_times, num_rooms):
    end_room_index = num_class_times + num_rooms
    rooms = []

    for room_line in range(num_class_times + 2, end_room_index + 2):
        current_room_line = c_data[room_line]
        line_data = current_room_line.split()
        id = room_line - num_class_times - 2
        building = ""
        code = line_data[0]
        index = 0
        # seperate building and classroom
        while index < len(code) and not code[index].isnumeric():
            building += code[index]
            index += 1

        capacity = int(line_data[1])
        new_room = Room(id, building, capacity)
        rooms.append(new_room)
    return rooms


def read_preferences(pref_filename):
    """
    Same as other file.
    :param pref_filename:
    :return:
    """
    p_file = open(pref_filename, "r")
    p_data = p_file.readlines()
    p_file.close()
    student_dict = dict()
    num_students = int(p_data[0].strip().split()[1])
    p_data = p_data[1:]
    for row in p_data:
        row_data = row.strip().split()
        student_dict[int(row_data[0])] = [int(class_id) for class_id in row_data[1:]]
    return num_students, student_dict


def read_constraints(constraint_filename):

    c_file = open(constraint_filename, "r")
    c_data = c_file.readlines()  # Read constraint file into a list of lines
    c_file.close()

    class_dict = dict()
    num_class_times = int(c_data[0].strip().split()[2])
    assert type(num_class_times) == int
    timeslots = parse_timeslots(c_data, num_class_times)

    rooms_line = num_class_times + 1
    num_rooms = int(c_data[rooms_line].split()[1])
    assert type(num_rooms) == int
    rooms = parse_rooms(c_data, num_class_times, num_rooms)

    for line in c_data[num_class_times + num_rooms:]:
        # How to parse classes?
        print(line)


    # room_dict = dict()
    # for row in c_data[2:end_room_index]:
    #     row_data = row.strip().split()
    #     room_dict[int(row_data[0])] = int(row_data[1])
    # num_classes = int(c_data[end_room_index].strip().split()[1])
    # num_teachers = int(c_data[end_room_index + 1].strip().split()[1])
    # teacher_dict = dict()
    # class_dict = dict()
    # for row in c_data[end_room_index + 2:]:
    #     row_data = row.strip().split()
    #     if class_dict.get(int(row_data[0])) is None:
    #         class_dict[int(row_data[0])] = int(row_data[1])
    #     if teacher_dict.get(int(row_data[1])) is None:
    #         teacher_dict[int(row_data[1])] = {'class':[int(row_data[0])]}
    #     else:
    #         teacher_dict[int(row_data[1])]['class'].append(int(row_data[0]))
    # return num_rooms, num_classes, num_class_times, num_teachers, room_dict, class_dict, teacher_dict


if __name__ == "__main__":
    #args = parse_args("Parse real data.")
    constraint_file = "../data/constraints.txt"
    pref_file = "../data/student_pref.txt"

    prefs = read_preferences(pref_file)
    constraints = read_constraints(constraint_file)
    print(constraints)