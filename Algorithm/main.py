from var_loading import load_variables_into_obj
from args import parse_args
from output import *


def get_obj_by_id(obj_list, id):
    """
    :param obj_list: List[Obj]
    :param id: Int
    :return: Obj -> Return the object with corresponding id.
    """

    for obj in obj_list:
        if obj.id == id:
            return obj
    return None


def sort_classes(S,C):
    """
    :param S: List[Student]
    :param C: List[Class]
    :return: List[Class] -> C sorted by total interest.
    """

    class_interest_count = {}
    for s in S:
        for p in s.preferences:
            #  and p is not a first year seminar
            if p in class_interest_count.keys():
                class_interest_count[p] = 1
            else:
                #i  f p first year seminar, classInterestCount[p] = 0
                class_interest_count[p] = 1
    #  sort by highest interest, descending order
    sorted_class_interest_count = sorted(C, key=lambda c: class_interest_count[c.id], reverse=True)
    return sorted_class_interest_count


def sort_class_times(T):
    """
    :param T: List[TimeSlot]
    :return: List[TimeSlot] -> sorted by potential conflicts with other time slots.
    """

    T_sorted = sorted(T, key=lambda x: x.start_time, reverse=True)
    for t in T_sorted:
        T_copy  = T_sorted
        T_copy.remove(t)
        for t_1 in T_copy:
            if does_conflict(t, t_1):
                t_1.conflicts += 1
    sorted_class_times = sorted(T, key=lambda x: x.conflicts)
    return sorted_class_times


def identify_rooms_for_class(R,C):
    """
    :param R: List[Room]
    :param C: List[Class]
    :return: Dict[Class : List[Rooms] -> the rooms that each class can occupy.
    """
    rooms_for_classes = {}
    sorted_rooms = sorted(R, key=lambda r: r.capacity, reverse=True)
    for cur_class in C:
        rooms_for_classes[cur_class] = sorted_rooms

    return rooms_for_classes


def set_up_availabilty(input, sorted_class_times):
    """
    :param input: List[Obj] either rooms or professors
    :param sorted_class_times:
    :return: Dict[Obj : Dict[TimeSlot : True]] -> Initialize all professors and rooms to be available at all time slots.
    """
    availability = {}
    for r in input:
        isOpen = {}
        for t in sorted_class_times:
            isOpen[t] = True
        availability[r] = isOpen
    return availability


def does_conflict(first_slot, second_slot):
    """

    :param first_slot: Timeslot Object
    :param second_slot: Timeslot Object
    :return: Whether or not they conflict. (Assuming second slot starts after first slot.)
    """

    if first_slot.end_time > second_slot.start_time:
        return True
    else:
        return False


def interval_scheduling(matches, preferences, C):
    """
    :param matches: Dict[Class : Dict[str : Obj]]
    :param preferences: List[Class] the classes that some student s wishes to take.
    :return: a list of classes, representing their optimal schedule without conflicts.

    """

    scheduled = []
    sorted_preferences = sorted(preferences, key=lambda class_id: matches[get_obj_by_id(C, class_id)]["timeslot"].end_time)
    previous_class = None
    for current_class_id in sorted_preferences:
        current_class = get_obj_by_id(C, current_class_id)
        current_time_slot = matches[current_class]["timeslot"]

        if previous_class is None:
            scheduled.append(current_class)
            previous_class = current_class

        else:

            previous_time_slot = matches[previous_class]["timeslot"]

            if not does_conflict(previous_time_slot, current_time_slot):
                scheduled.append(current_class)
                previous_class = current_class

    return scheduled


def enroll_students(matches, S, R, T, C):
    """
    :param matches: Dictionary of dictionaries containing rooms, timeslots, professors assigned to each class.
    :param S: List[Student]
    :param R: List[Room]
    :param T: List[TimeSlot]
    :return: # of classes we were able to enroll students in and the updated matches dictionary that has the students enrolled in each class.
    """

    room_capacities = {}
    score = 0

    for room in R:
        room_capacities[room] = {}
        for timeslot in T:
            room_capacities[room][timeslot] = room.capacity

    for student in S:

        enrolled_classes = interval_scheduling(matches, student.preferences, C)

        for desired_class in enrolled_classes:  # Attempt to enroll student in each class from interval scheduling.
            room = matches[desired_class]["room"]
            timeslot = matches[desired_class]["timeslot"]
            if room_capacities[room][timeslot] > 0:  # There is still room in this class.
                score += 1
                room_capacities[room][timeslot] -= 1
                if matches[desired_class].get("students") is None:
                    matches[desired_class]["students"] = [student]
                else:
                    matches[desired_class]["students"].append(student)

    return score, matches


def class_schedule(T,S,C,R,P):
    """

    :param T: List[TimeSlot]
    :param S: List[Student]
    :param C: List[Classes]
    :param R: List[Rooms]
    :param P: List[Professor]
    :return: Tuple[Int, Dict[Class : Dict[str : Obj]]] Score of the schedule + the matches it generated.
    """
    sorted_class = sort_classes(S,C)
    sorted_class_times = sort_class_times(T)
    rooms_for_classes = identify_rooms_for_class(R,C)
    room_availability = set_up_availabilty(R, sorted_class_times)
    prof_availability = set_up_availabilty(P, sorted_class_times)
    matches = {}
    for c in sorted_class:
        #  define professor
        p_id = c.professor
        p = get_obj_by_id(P, p_id)
        for t in sorted_class_times:
            if c in matches.keys():
                break
            elif prof_availability[p][t] == True:
                for r in rooms_for_classes[c]:
                    if room_availability[r][t] == True:
                        matches[c] = {"timeslot": t, "room": r}
                        room_availability[r][t] = False
                        prof_availability[p][t] = False
                        # TODO: Confused what # of students refers to pseudocode. Also, This line is broken.
                        # t.conflicts *= min(r.capacity, sorted_class[c])
                        t.conflicts *= r.capacity
                        #  time conflicts
                        break

        sorted_class_times = sorted(sorted_class_times, key=lambda x: x.conflicts)
    score, matches = enroll_students(matches, S, R, T, C)
    return score, matches


if __name__ == "__main__":
    """
    example run: python main.py -p ./misc/k10r4c14t4s50/prefs_0 -c ./misc/k10r4c14t4s50/constraints_0
    """

    args = parse_args('Set up student dictionary')

    R, C, P, S, T = load_variables_into_obj(args.pref_filename, args.constraint_filename)
    score, matches = class_schedule(T, S, C, R, P)
    file = (matches, "schedule_file.txt")
    str_matches = matches_to_string(matches)
    print(str_matches)
    print("Wrote to file: "+file)


