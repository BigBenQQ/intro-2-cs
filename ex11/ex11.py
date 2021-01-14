from collections import Counter
from copy import copy


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.__data = data
        self.__positive_child = positive_child
        self.__negative_child = negative_child

    def get_value(self):
        return self.__data

    def get_pos_child(self):
        return self.__positive_child

    def set_pos_child(self, pos_child):
        self.__positive_child = pos_child

    def get_neg_child(self):
        return self.__negative_child

    def set_neg_child(self, neg_child):
        self.__negative_child = neg_child

    def set_data(self, data):
        self.__data = data

    def set_child(self, child):
        self.__negative_child = copy(child)
        self.__positive_child = copy(child)

    def __copy__(self):
        return Node(self.get_value(), self.get_pos_child(), self.get_neg_child())


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


def sort_list_by_popularity(lst: list):
    lst.sort(key=Counter(lst).get, reverse=True)  # sorting by number of item
    return list(dict.fromkeys(lst))  # removing repeated elements


class Diagnoser:
    def __init__(self, root: Node):
        self.__root = root

    def diagnose(self, symptoms: list):
        if self.__root.get_pos_child() is None:
            return self.__root.get_value()

        is_symptom_found_flag = False
        for symptom in symptoms:
            if symptom == self.__root.get_value():
                is_symptom_found_flag = True
                new_diagnosis = Diagnoser(self.__root.get_pos_child())
                symptoms.remove(symptom)
                illness = new_diagnosis.diagnose(symptoms)
                break

        if not is_symptom_found_flag:
            new_diagnosis = Diagnoser(self.__root.get_neg_child())
            illness = new_diagnosis.diagnose(symptoms)

        return illness

    def calculate_success_rate(self, records: list):
        correct_diagnosis_counter = 0
        for record in records:
            if record[0] == self.diagnose(record[1]):
                correct_diagnosis_counter += 1

        return correct_diagnosis_counter / len(records)

    def all_illnesses(self):
        illness_lst = self.all_illnesses_helper()
        return sort_list_by_popularity(illness_lst)

    def all_illnesses_helper(self, illnesses_lst=None):
        if illnesses_lst is None:
            illnesses_lst = list()

        if self.__root.get_pos_child() is None:  # is an illness (leaf)
            illnesses_lst.append(self.__root.get_value())

        else:
            new_diagnoser = Diagnoser(self.__root.get_pos_child())
            new_diagnoser.all_illnesses_helper(illnesses_lst)

            new_diagnoser = Diagnoser(self.__root.get_neg_child())
            new_diagnoser.all_illnesses_helper(illnesses_lst)

        return illnesses_lst

    def paths_to_illness(self, illness: str):
        return self.paths_to_illness_helper(illness)

    def paths_to_illness_helper(self, illness: str, path_candidate=None, paths_lst=None):
        if paths_lst is None and path_candidate is None:
            paths_lst = list()
            path_candidate = list()

        if self.__root.get_pos_child() is None:  # is an illness (leaf)
            if self.__root.get_value() == illness:
                paths_lst.append(path_candidate[:])

        else:
            new_diagnoser = Diagnoser(self.__root.get_pos_child())
            path_candidate.append(True)
            new_diagnoser.paths_to_illness_helper(illness, path_candidate, paths_lst)

            new_diagnoser = Diagnoser(self.__root.get_neg_child())
            path_candidate.append(False)
            new_diagnoser.paths_to_illness_helper(illness, path_candidate, paths_lst)

        if len(path_candidate) > 0:
            path_candidate.pop()  # backtrack
        return paths_lst


def build_tree(records: list, symptoms: list):
    if len(symptoms) == 0:
        minimum_count_index = 0  # sorting the illness with the the least amount of symptoms
        if len(records) > 0:
            for i, record in enumerate(records):
                if len(record.symptoms) < len(records[minimum_count_index].symptoms):
                    minimum_count_index = i
            matching_illness = records[minimum_count_index].illness
            return Node(matching_illness)
        else:
            return Node(None)

    else:
        root = build_tree_helper(symptoms, symptoms[1:], Node(symptoms[0]))
        return root


def generate_leaf(original_symptoms, root, path_lst):
    present_symptoms = []
    absent_symptoms = []

    for i in range(len(path_lst)):
        if path_lst[i]:
            present_symptoms.append(original_symptoms[i])
        else:
            absent_symptoms.append(original_symptoms[i])

    possible_illnesses = []
    for record in records:
        if len(present_symptoms) == 0:
            return None# TODO: complete empty lists cases
        if len(absent_symptoms) == 0:
            return None

        if set(present_symptoms).issubset(record.symptoms):
            if not set(absent_symptoms) <= set(record.symptoms):
                possible_illnesses.append(record.illness)

    # sorting by number of item and returning the most popular
    return possible_illnesses.sort(key=Counter(possible_illnesses).get, reverse=True)[0]



def build_tree_helper(original_symptoms: list, symptoms: list, root: Node, path_lst=None):
    if path_lst is None:  # first iteration
        path_lst = list()

    if len(symptoms) == 0:  # base case - no symptoms left in the list
        path_lst.append(True)
        root.set_pos_child(generate_leaf(original_symptoms, root, path_lst))

        path_lst[-1] = False
        root.set_neg_child(generate_leaf(original_symptoms, root, path_lst))

        path_lst.pop()
        return root

    else:
        root.set_pos_child(Node(symptoms[0]))
        path_lst.append(True)
        build_tree_helper(original_symptoms, symptoms[1:], root.get_pos_child(), path_lst)
        path_lst.pop()

        root.set_neg_child(Node(symptoms[0]))
        path_lst.append(False)
        build_tree_helper(original_symptoms, symptoms[1:], root.get_neg_child(), path_lst)

    if len(path_lst) > 0:
        path_lst.pop()
    return root


def optimal_tree(records, symptoms, depth):
    pass


if __name__ == "__main__":
    # Manually build a simple tree.
    #                 cough
    #          Yes /         \ No
    #        fever            headache
    #   Yes /     \ No     yes/       \no
    # influenza   cold     healthy     healthy

    # flu_leaf = Node("influenza", None, None)
    # cold_leaf = Node("cold", None, None)
    # inner_vertex = Node("fever", flu_leaf, cold_leaf)
    # healthy_leaf = Node("healthy", None, None)
    # headache_vertex = Node("headache", healthy_leaf, healthy_leaf)
    # # root = Node("cough", inner_vertex, healthy_leaf)
    # root = Node("cough", inner_vertex, headache_vertex)
    #
    # diagnoser = Diagnoser(root)
    # print(diagnoser.all_illnesses())
    # print(diagnoser.paths_to_illness("cold"))
    # # Simple test
    # diagnosis = diagnoser.diagnose(["cough"])
    # if diagnosis == "cold":
    #     print("Test passed")
    # else:
    #     print("Test failed. Should have printed cold, printed: ", diagnosis)
    #
    # # Add more tests for sections 2-7 here.
    # # test build tree
    # records = parse_data("Data/tiny_data.txt")
    # symptom_lst = records[0].symptoms
    # new_tree_root = build_tree(records, symptom_lst)
    # print(new_tree_root)
    symptoms = ["fever", "irritability"]
    records = parse_data("./Data/small_data.txt")
    build_tree(records, symptoms)
