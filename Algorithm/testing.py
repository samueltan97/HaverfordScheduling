from misc.var_loading import read_constraints, read_preferences
from Algorithm.objects import *


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
        if new_slot_end > 16:
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
    """
    Hard coded test case that can be used to look at variable loading into the objects. 
    """
    pref_filename = "../misc/k10r4c14t4s50/prefs_0"
    constraint_filename = "../misc/k10r4c14t4s50/constraints_0"
    result = load_variables_into_obj(pref_filename, constraint_filename)




