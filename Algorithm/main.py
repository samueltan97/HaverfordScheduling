
class Class:
    def __init__(self, id, professor, writing_seminar, language):
        self.id = id
        self.professor = professor
        self.writing_seminar = writing_seminar
        self.language = language

    def copy(self):
        return self.__init__(self.id, self.professor, self.writing_seminar, self.language)


class TimeSlot:
    def __init__(self, id, days, start_time, end_time):
        self.id = id
        self.days = days
        self.start_time = start_time
        self.end_time = end_time


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
    matches[class][room] gives me the room object matched with that class ojbect. 
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
    class_time_conflicts = {}
    sorted_class_times = []
    T.sort(key=lambda x: x[3])
    for t in T:
        class_time_conflicts[t] = 0
        for


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
            isOpen[t] = "True"
