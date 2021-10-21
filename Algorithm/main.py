
class Class:
    def __init__(self, id, professor, writing_seminar, language):
        self.id = id
        self.professor = professor
        self.writing_seminar = writing_seminar
        self.language = language

    def copy(self):
        return self.__init__(self.id, self.professor, self.writing_seminar, self.language)


class TimeSlot:
    def __init__(self, id, days, start_time, end_time, conflicts = 0):
        self.id = id
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.conflicts = conflicts


class Room:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity


class Student:
    def __init__(self, id, preferences):
        self.id = id
        self.preferences = preferences # A list of class objects.

"""
For the matches datastructure, i assumed a dictionary keyed by classes, with values being another dictionary. 
The inner dictionary is then keyed with the rooms, timeslot, professor and so on. 
Ex.
    matches[class][room] gives me the room object matched with that class object. 
    matches[class][time] gives me the timeslot object matched with that class. 
"""


def sort_classes(S,C):
    """

    :param S: List[Student]
    :param C: List[Class]
    :return: List[Class] -> C sorted by total interest.
    """

    class_interest_count = {}
    for s in S:
        for p in S[s]:
            #  and p is not a first year seminar
            if p in class_interest_count.keys():
                class_interest_count[p] = 1
            else:
                #i  f p first year seminar, classInterestCount[p] = 0
                class_interest_count[p] = 1
    #  sort by highest interest, descending order
    sorted_class_interest_count = sorted(class_interest_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_class_interest_count


def sort_class_times(T):
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
    :return: List[Class] -> rooms sorted by their capacity in reverse.
    """

    sorted_rooms = sorted(R, key=lambda r: r.capacity, reverse=True)
    return sorted_rooms

def set_up_availabilty(input, sorted_class_times):
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
    for current_class in sorted_preferences:
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


def classSchedule(T,S,C,R,P):
    sortedClass = sort_classes(S,C)
    sortedClassTimes = sort_class_times(T)
    roomsForClasses = identify_rooms_for_class(R,C)
    roomAvailability = set_up_availabilty(C, sortedClassTimes)
    profAvailability = set_up_availabilty(P, sortedClassTimes)

    matches = {}
    for c in sortedClass:
        #define professor
        p = c.professor
        for t in sortedClassTimes:
            if c in matches.keys():
                break
            elif profAvailability[p][t] == True:
                for r in roomsForClasses[c]:
                    if roomAvailability[r][t] == True:
                        matches[c] = {"timeslot": t, "room": r}
                        roomAvailability[r][t] = False
                        profAvailability[r][t] = False
                        t.conflicts *= min(r.capacity, sortedClass[c])
                        #time conflicts
                        break

        sortedClassTimes = sorted(sortedClassTimes, key=lambda x: x[1])
    score = enroll_students(matches, S, R, T)
    return score, matches


if __name__ == "__main__":

    #define objects and run class scheduling

