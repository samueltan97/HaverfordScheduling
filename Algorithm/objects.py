import json

class Class:
    def __init__(self, id, class_level=None, department=None, professor=None, corresponding_class=[],
                 stem=False, humanities=False,
                 writing_seminar=False, language=False):

        """
        :param id: Int
        :param professor: Professor that teaches given class.
        :param valid_buildings: List[str] -> buildings
        :param writing_seminar: Bool
        :param language: Bool
        """
        self.id = id
        self.professor = professor
        self.writing_seminar = writing_seminar
        self.language = language
        self.stem = stem
        self.humanities = humanities
        self.class_level = class_level
        self.department = department
        self.corresponding_class = corresponding_class

    def copy(self):
        return self.__init__(self.id, self.professor, self.writing_seminar, self.language)

    def valid_buildings(self):
        valid_buildings_dict = json.load("valid_buildings.json")
        return valid_buildings_dict[self.department]

    def __str__(self):
        return "(Class: {}, " \
            "Professor: {}, " \
            "WritingSem: {}, " \
            "Lang: {}, " \
            "Department: {}, " \
            "Class Level: {}) ".format(self.id, self.professor, self.writing_seminar, self.language, self.department, self.class_level)



class TimeSlot:
    def __init__(self, id, days, start_times, end_times, conflicts=0):

        """
        :param id: Int
        :param days: List[str] days
        :param start_times: List[List[int]] start times per day
        :param end_times: List[List[int]] end times per day
        :param conflicts: int -> counter used to sort timeslots by # of conflicts.

        for start_time and end_time are list of lists in case multiple slots per day.
        Len(days) = len(start_time) = len(end_time)
        """

        if len(days) != len(start_times) != len(end_times):
            print("Invalid input to Timeslot: days, start_time, \
            and end_time must be same length: (days, start_time, end_time)", days, start_times, end_times)
            raise ValueError

        self.id = id
        self.days = days  # List of days where the class happens.
        self.start_times = start_times
        self.end_times = end_times
        self.conflicts = conflicts

    def __str__(self):
        return "(TimeSlot:{} {}:{}-{})".format(self.id, self.days, self.start_times[0], self.end_times[0])


class Room:
    def __init__(self, id, building_code, capacity, stem_valid=False, humanities_valid=False, art_valid=False, music_valid=False):
        """
        :param id: Int
        :param capacity: Int
        :param stem_valid: Bool
        :param humanities_valid: Bool
        :param art_valid: Bool
        :param music_valid: Bool
        """
        self.id = id
        self.capacity = capacity
        self.building_code = building_code
        self.stem_valid = stem_valid
        self.humanities_valid = humanities_valid
        self.art_valid = art_valid
        self.music_valid = music_valid

    def __str__(self):
        return "(Room:{}, Capacity: {}, Building: {})".format(self.id, self.capacity, self.building_code)


class Student:
    def __init__(self, id, preferences):
        """
        :param id: Int
        :param preferences: List[Int] -> list of class ids the student is interested in.
        """
        self.id = id
        self.preferences = preferences  # A list of class objects.

    def __str__(self):
        return "(Student:{}, preferences: {})".format(self.id, self.preferences)


class Professor:
    def __init__(self, id, classes):
        """
        :param id: Int
        :param classes: List[Int] -> list of classes the professor is able to teach.
        """
        self.id = id
        self.classes = classes

    def __str__(self):
        return "(Professor:{}, classes: {})".format(self.id, self.classes)
