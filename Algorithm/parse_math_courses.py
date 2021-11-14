import os
import pprint


def parse_timeslots(c_data):
    num_class_times = int(c_data[0].split()[2])
    time_slots = []
    for i in range(1, num_class_times+2):
        time_slots.append("-".join(c_data[i].split()[1:]))

    return time_slots, num_class_times

def parse_rooms(c_data, offset):
    num_rooms = int(c_data[offset].split()[1])
    rooms = []
    for i in range(offset+1, offset+num_rooms+1):
        rooms.append(c_data[i].split()[0])
    return rooms

if __name__ == "__main__":

    input_file = "math_courseS2015.txt"
    sched_file = "sched.txt"
    constraints_file = "../data/parsed_data/Spring2015/constraints.txt"
    math_courses = {}
    sched_math_courses = {}
    with open(input_file, "r") as math_course_file:
        raw_lines = math_course_file.readlines()

    for line in raw_lines:
        course = line.split("-")
        course_id = str(int(course[0]))
        course_name = course[1]
        course_label = course[2]
        course_room = course[3]
        course_start = course[4]
        course_end = course[5]
        course_days = course[6]

        math_courses[course_id] = {
            "course_name": course_name,
            "course_label": course_label,
            "course_start": course_start,
            "course_room": course_room,
            "course_end": course_end,
            "course_days": course_days
        }

    with open(constraints_file, "r") as constr_file:
        data = constr_file.readlines()


    real_time_slots, num_of_time_slots = parse_timeslots(data)
    real_rooms = parse_rooms(data, num_of_time_slots+1)

    with open(sched_file, "r") as sched:
        sched_raw_lines = sched.readlines()

    for line in sched_raw_lines[1:]:
        data = line.split()
        course_id = data[0]
        room = real_rooms[int(data[1])]
        time = real_time_slots[int(data[3])]
        if course_id in math_courses:
            entry = {
                "room": room,
                "time": time
            }
            sched_math_courses[course_id] = entry
    print("OUR ALGORITHM:")
    pprint.pprint(sched_math_courses)
    print("THE SCHEDULE")
    pprint.pprint(math_courses)


