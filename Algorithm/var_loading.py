import optparse
import sys
from args import parse_args
from objects import *

"""
Example runs from command line: 
Win: python .\var_loading.py -p .\misc\k10r4c14t4s50\prefs_0 -c .\misc\k10r4c14t4s50\constraints_0
Mac: python ./misc/var_loading.py -p ./misc/k10r4c14t4s50/prefs_0 -c ./misc/k10r4c14t4s50/constraints_0
python misc/var_loading.py -p ./misc/k10r4c14t4s50/prefs_0 -c ./misc/k10r4c14t4s50/constraints_0

"""


def read_preferences(pref_filename):
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
    c_data = c_file.readlines()
    c_file.close()
    class_dict = dict()
    num_class_times = int(c_data[0].strip().split()[2])
    assert type(num_class_times) == int
    num_rooms = int(c_data[1].strip().split()[1])
    assert type(num_rooms) == int
    end_room_index = 2+num_rooms
    room_dict = dict()
    for row in c_data[2:end_room_index]:
        row_data = row.strip().split()
        room_dict[int(row_data[0])] = int(row_data[1])
    num_classes = int(c_data[end_room_index].strip().split()[1])
    num_teachers = int(c_data[end_room_index + 1].strip().split()[1])
    teacher_dict = dict()
    class_dict = dict()
    for row in c_data[end_room_index + 2:]:
        row_data = row.strip().split()
        if class_dict.get(int(row_data[0])) is None:
            class_dict[int(row_data[0])] = int(row_data[1])
        if teacher_dict.get(int(row_data[1])) is None:
            teacher_dict[int(row_data[1])] = {'class':[int(row_data[0])]}
        else:
            teacher_dict[int(row_data[1])]['class'].append(int(row_data[0]))
    return num_rooms, num_classes, num_class_times, num_teachers, room_dict, class_dict, teacher_dict


def create_timeslots(num_slots):
    """
    Temporary function to create some realistic time slots for the algorithm to use.
    :param num_slots: Int -> number of different time slots we can schedule.
    :return: List[TimeSlot]
    """
    slots = []
    first_class_start = 8
    last_class_end = 16  # using 24 hour time

    mwf_counter = 0
    tth_counter = 0
    while mwf_counter+tth_counter < num_slots :
        new_slot_start = first_class_start + mwf_counter
        new_slot_end = first_class_start + mwf_counter + 1
        if new_slot_end > last_class_end:
            print("Error: create_timeslots ran out of slots to create.")
            raise IndexError
        new_slot_days = "MWF"
        new_id = mwf_counter + tth_counter + 1
        new_slot = TimeSlot(id=new_id, start_time=new_slot_start, end_time=new_slot_end, days=new_slot_days)
        slots.append(new_slot)
        mwf_counter += 1
        if mwf_counter+tth_counter == num_slots:
            break
        else:  # Add another one
            new_slot_days = "TTh"
            new_id = mwf_counter + tth_counter + 1
            new_slot = TimeSlot(id= new_id, start_time=new_slot_start, end_time=new_slot_end, days=new_slot_days)
            slots.append(new_slot)
            tth_counter += 1

    return slots


def load_variables_into_obj(pref_filename, constraint_filename):
    """

    :param pref_filename: str -> path to preference file
    :param constraint_filename: str -> path to constraint file
    :return: Tuple[List[Obj]] -> Objects needed for the algorithm (Rooms, Classes, Professors, Students, TimeSlots)
    """
    num_rooms, num_classes, num_class_times, num_teachers, room_dict, class_dict, teacher_dict = read_constraints(
        constraint_filename)

    num_students, student_dict = read_preferences(pref_filename)

    R = [Room(id=r[0], capacity=r[1]) for r in room_dict.items()]
    C = [Class(id=c[0], professor=c[1]) for c in class_dict.items()]
    P = [Professor(id=key, classes=teacher_dict[key]['class']) for key in list(teacher_dict.keys())]
    S = [Student(id=s[0], preferences=s[1]) for s in student_dict.items()]
    T = create_timeslots(num_class_times)
    return R, C, P, S, T


if __name__ == "__main__":
    args = parse_args('Set up student dictionary')
    # print(read_constraints(args.constraint_filename))
    # print(read_preferences(args.pref_filename))

    objs = load_variables_into_obj(args.pref_filename, args.constraint_filename)