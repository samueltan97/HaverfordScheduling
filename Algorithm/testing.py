from misc.var_loading import read_constraints, read_preferences


def test_load_variables():
    pass


if __name__ == "__main__":
    """
    Hard coded test case that can be used to look at variable loading into the objects. 
    """
    pref_filename = "../misc/k10r4c14t4s50/prefs_0"
    constraint_filename = "../misc/k10r4c14t4s50/constraints_0"
    print(read_constraints(constraint_filename))
    print(read_preferences(pref_filename))
