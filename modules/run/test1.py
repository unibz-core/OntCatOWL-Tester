""" Baseline dictionary definition. """
import csv
import os
import pathlib

import yaml

from modules.tester.logger_config import initialize_logger

NAMESPACE_GUFO = "http://purl.org/nemo/gufo#"
NAMESPACE_TAXONOMY = "http://taxonomy.model/"


class input_class(object):
    def __init__(self, class_name, class_stereotype):
        self.class_name = class_name
        self.class_stereotype = class_stereotype


def load_baseline_dictionary(dataset):
    list_input_classes = []

    tester_path = str(pathlib.Path().resolve())
    dataset_path = tester_path + chr(92) + "catalog" + chr(92) + dataset + chr(92)
    csv_file_full_path = dataset_path + "classes_data.csv"

    with open(csv_file_full_path, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        index = 0
        for row in csv_reader:
            if (index != 0) and (row[2] != "other"):
                new_class = input_class(row[0], row[2])
                list_input_classes.append(new_class)
            index += 1

    return list_input_classes


def convert_ontology_dataclass_list_to_dictionary_list(input_class, ontology_dataclass_list):
    """ Receives an ontology_dataclass_list and returns a dictionary to be printed in yaml format. """

    ontology_dictionary_list = []

    for ontology_dataclass in ontology_dataclass_list:

        input_class_long_name = NAMESPACE_TAXONOMY + input_class.class_name
        if input_class_long_name == ontology_dataclass.uri:
            input_situation = True
        else:
            input_situation = False

        short_class_name = ontology_dataclass.uri.removeprefix(NAMESPACE_TAXONOMY)

        ontology_dictionary = {
            short_class_name: {
                "input": input_situation,
                "is_type": ontology_dataclass.is_type,
                "can_type": ontology_dataclass.can_type,
                "not_type": ontology_dataclass.not_type,
                "is_incomplete": ontology_dataclass.incompleteness_info["is_incomplete"],
                "detected_in": ontology_dataclass.incompleteness_info["detected_in"]}
        }
        ontology_dictionary_list.append(ontology_dictionary)

    return ontology_dictionary_list


def create_classes_yaml_output(input_class, ontology_dataclass_list, test_results_folder, execution_name):
    """ Receives an ontology_dataclass_list and saves its information in yaml format. """

    logger = initialize_logger()

    yaml_folder = test_results_folder + "\\results"
    if not os.path.exists(yaml_folder):
        try:
            os.makedirs(yaml_folder)
        except OSError as error:
            logger.error(f"Directory {yaml_folder} could not be created. Program aborted.\n"
                         f"System error reported: {error}")

    classes_output_filename = f"classes_{execution_name}.yaml"
    classes_output_complete_path = yaml_folder + "\\" + classes_output_filename

    ontology_dictionary_list = convert_ontology_dataclass_list_to_dictionary_list(input_class, ontology_dataclass_list)

    with open(classes_output_complete_path, 'w', encoding='utf-8') as file:
        yaml.dump_all(ontology_dictionary_list, file, sort_keys=True)


def get_final_list(class_name_prefixed, class_gufo_stereotype, ontology_dataclass_list):
    final_list = "undeclared"
    logger = initialize_logger()

    for dataclass in ontology_dataclass_list:
        if dataclass.uri == class_name_prefixed:
            if class_gufo_stereotype in dataclass.is_type:
                final_list = "is"
            elif class_gufo_stereotype in dataclass.can_type:
                final_list = "can"
            elif class_gufo_stereotype in dataclass.not_type:
                final_list = "not"
            else:
                logger.error("Not found in any list.")
                exit(1)

    return final_list


def create_classes_results_csv_output(input_classes_list, ontology_dataclass_list, dataset_folder, test_results_folder,
                                      execution_name):
    final_row_list = []

    for input_class in input_classes_list:
        class_name_prefixed = NAMESPACE_TAXONOMY + input_class.class_name
        class_gufo_stereotype = remaps_to_gufo(input_class.class_name, input_class.class_stereotype, True)
        class_gufo_stereotype = "gufo:" + class_gufo_stereotype
        final_list = get_final_list(class_name_prefixed, class_gufo_stereotype, ontology_dataclass_list)
        final_row = [input_class.class_name, input_class.class_stereotype, final_list]
        final_row_list.append(final_row)

    yaml_folder = test_results_folder + "\\results"

    classes_output_filename = f"results_{execution_name}.csv"
    classes_output_complete_path = yaml_folder + "\\" + classes_output_filename

    csv_header = ["class_name", "class_original_stereotype", "stereotype_final_list"]

    with open(classes_output_complete_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        for final_row in final_row_list:
            writer.writerow(final_row)


def remaps_to_gufo(class_name, gufo_lower_type, no_namespace=False):
    """ Receives a gufo_lower_type and returns a valid_gufo_type """

    logger = initialize_logger()

    if gufo_lower_type == "category":
        mapped_stereotype = "Category"
    elif gufo_lower_type == "kind":
        mapped_stereotype = "Kind"
    elif gufo_lower_type == "mixin":
        mapped_stereotype = "Mixin"
    elif gufo_lower_type == "phase":
        mapped_stereotype = "Phase"
    elif gufo_lower_type == "phasemixin":
        mapped_stereotype = "PhaseMixin"
    elif gufo_lower_type == "role":
        mapped_stereotype = "Role"
    elif gufo_lower_type == "rolemixin":
        mapped_stereotype = "RoleMixin"
    elif gufo_lower_type == "subkind":
        mapped_stereotype = "SubKind"
    elif gufo_lower_type == "sortal":
        mapped_stereotype = "Sortal"
    elif gufo_lower_type == "nonsortal":
        mapped_stereotype = "NonSortal"
    elif gufo_lower_type == "rigidtype":
        mapped_stereotype = "RigidType"
    elif gufo_lower_type == "nonrigidtype":
        mapped_stereotype = "NonRigidType"
    else:
        logger.error(f"Unknown gufo_lower_type {gufo_lower_type} in class {class_name}. Program aborted.")
        exit(1)

    if no_namespace:
        valid_gufo_type = mapped_stereotype
    else:
        valid_gufo_type = NAMESPACE_GUFO + mapped_stereotype

    return valid_gufo_type


def create_times_csv_output(time_register, test_results_folder, execution_number, execution_name):
    times_output_filename = f"execution_times.csv"
    times_output_complete_path = test_results_folder + "\\" + times_output_filename

    time_register["execution"] = execution_number

    if execution_number == 1:
        with open(times_output_complete_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=time_register.keys())
            writer.writeheader()
            writer.writerow(time_register)
    else:
        with open(times_output_complete_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=time_register.keys())
            writer.writerow(time_register)


def create_csv_header():
    csv_header = []

    # GENERAL

    csv_header.append("execution")

    # CLASSES

    # Classes values before
    csv_header.append("classes_b_total_classes_number")
    csv_header.append("classes_b_tu_classes_types_v")
    csv_header.append("classes_b_pk_classes_types_v")
    csv_header.append("classes_b_tk_classes_types_v")

    # Classes percentages before
    csv_header.append("classes_b_tu_classes_types_p")
    csv_header.append("classes_b_pk_classes_types_p")
    csv_header.append("classes_b_tk_classes_types_p")

    # Classes values after
    csv_header.append("classes_a_total_classes_number")
    csv_header.append("classes_a_tu_classes_types_v")
    csv_header.append("classes_a_pk_classes_types_v")
    csv_header.append("classes_a_tk_classes_types_v")

    # Classes percentages after
    csv_header.append("classes_a_tu_classes_types_p")
    csv_header.append("classes_a_pk_classes_types_p")
    csv_header.append("classes_a_tk_classes_types_p")

    # CLASSIFICATIONS

    # Classifications values before
    csv_header.append("classif_b_total_classif_types_v")
    csv_header.append("classif_b_unknown_classif_types_v")
    csv_header.append("classif_b_known_classif_types_v")

    # Classifications values after
    csv_header.append("classif_a_total_classif_types_v")
    csv_header.append("classif_a_unknown_classif_types_v")
    csv_header.append("classif_a_known_classif_types_v")

    # Classifications percentages before
    csv_header.append("classif_b_unknown_classif_types_p")
    csv_header.append("classif_b_known_classif_types_p")

    # Classifications percentages after
    csv_header.append("classif_a_unknown_classif_types_p")
    csv_header.append("classif_a_known_classif_types_p")

    # DIFFERENCES

    # Classes difference values: after - before
    csv_header.append("diff_tu_classes_types_v")
    csv_header.append("diff_pk_classes_types_v")
    csv_header.append("diff_tk_classes_types_v")

    # Classes difference percentages: after - before
    csv_header.append("diff_tu_classes_types_p")
    csv_header.append("diff_pk_classes_types_p")
    csv_header.append("diff_tk_classes_types_p")

    # Classifications difference values: after - before
    csv_header.append("diff_unknown_classif_types_v")
    csv_header.append("diff_known_classif_types_v")

    # Classifications difference percentages: after - before
    csv_header.append("diff_unknown_classif_types_p")
    csv_header.append("diff_known_classif_types_p")

    # INCOMPLETENESS
    csv_header.append("incomplete_classes_found")

    return csv_header


def populate_csv_row(consolidated_statistics, execution_number, number_incomplete_classes):
    csv_row = []

    # GENERAL

    csv_row.append(execution_number)

    classes_b = consolidated_statistics.classes_stats_b
    classes_a = consolidated_statistics.classes_stats_a
    classif_b = consolidated_statistics.classif_stats_b
    classif_a = consolidated_statistics.classif_stats_a

    # CLASSES

    # Classes values before
    csv_row.append(classes_b.total_classes_number)
    csv_row.append(classes_b.tu_classes_types_v)
    csv_row.append(classes_b.pk_classes_types_v)
    csv_row.append(classes_b.tk_classes_types_v)

    # Classes percentages before
    csv_row.append(classes_b.tu_classes_types_p)
    csv_row.append(classes_b.pk_classes_types_p)
    csv_row.append(classes_b.tk_classes_types_p)

    # Classes values after
    csv_row.append(classes_a.total_classes_number)
    csv_row.append(classes_a.tu_classes_types_v)
    csv_row.append(classes_a.pk_classes_types_v)
    csv_row.append(classes_a.tk_classes_types_v)

    # Classes percentages after
    csv_row.append(classes_a.tu_classes_types_p)
    csv_row.append(classes_a.pk_classes_types_p)
    csv_row.append(classes_a.tk_classes_types_p)

    # CLASSIFICATIONS

    # Classifications values before
    csv_row.append(classif_b.total_classif_types_v)
    csv_row.append(classif_b.unknown_classif_types_v)
    csv_row.append(classif_b.known_classif_types_v)

    # Classifications values after
    csv_row.append(classif_a.total_classif_types_v)
    csv_row.append(classif_a.unknown_classif_types_v)
    csv_row.append(classif_a.known_classif_types_v)

    # Classifications percentages before
    csv_row.append(classif_b.unknown_classif_types_p)
    csv_row.append(classif_b.known_classif_types_p)

    # Classifications percentages after
    csv_row.append(classif_a.unknown_classif_types_p)
    csv_row.append(classif_a.known_classif_types_p)

    # DIFFERENCES

    # Classes difference values: after - before
    csv_row.append(consolidated_statistics.tu_classes_types_v_d)
    csv_row.append(consolidated_statistics.pk_classes_types_v_d)
    csv_row.append(consolidated_statistics.tk_classes_types_v_d)

    # Classes difference percentages: after - before
    csv_row.append(consolidated_statistics.tu_classes_types_p_d)
    csv_row.append(consolidated_statistics.pk_classes_types_p_d)
    csv_row.append(consolidated_statistics.tk_classes_types_p_d)

    # Classifications difference values: after - before
    csv_row.append(consolidated_statistics.unknown_classif_types_v_d)
    csv_row.append(consolidated_statistics.known_classif_types_v_d)

    # Classifications difference values: after - before
    csv_row.append(consolidated_statistics.unknown_classif_types_p_d)
    csv_row.append(consolidated_statistics.known_classif_types_p_d)

    # INCOMPLETENESS
    csv_row.append(number_incomplete_classes)

    return csv_row


def calculate_incompleteness_values(ontology_dataclass_list):
    number_incomplete_classes = 0
    for dataclass in ontology_dataclass_list:
        if dataclass.incompleteness_info["is_incomplete"]:
            number_incomplete_classes += 1

    return number_incomplete_classes


def create_statistics_csv_output(ontology_dataclass_list, consolidated_statistics, test_results_folder,
                                 execution_number):
    csv_header = create_csv_header()
    number_incomplete_classes = calculate_incompleteness_values(ontology_dataclass_list)
    csv_row = populate_csv_row(consolidated_statistics, execution_number, number_incomplete_classes)

    statistics_output_filename = f"execution_statistics.csv"
    statistics = test_results_folder + "\\" + statistics_output_filename

    if execution_number == 1:
        with open(statistics, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
            writer.writerow(csv_row)
    else:
        with open(statistics, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)


def create_summary_csv_output(test_results_folder, execution_number, input_class):
    """ Creates and updates a CSV file with a list of all executions, the respective input classes
    and their stereotypes. """

    input_class_name = input_class.class_name
    input_class_stereotype = input_class.class_stereotype

    csv_header = ["execution_number", "input_class_name", "input_class_stereotype"]
    csv_row = [execution_number, input_class_name, input_class_stereotype]

    statistics_output_filename = f"execution_summary.csv"
    statistics = test_results_folder + "\\" + statistics_output_filename

    if execution_number == 1:
        with open(statistics, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
            writer.writerow(csv_row)
    else:
        with open(statistics, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)


def create_inconsistency_csv_output(test_results_folder, execution_number, input_class):
    """ Creates and updates a CSV file with a list of all inconsistent classes and their stereotypes. """
    input_class_name = input_class.class_name
    input_class_stereotype = input_class.class_stereotype

    csv_header = ["execution_number", "inconsistent_class_name", "inconsistent_class_stereotype"]
    csv_row = [execution_number, input_class_name, input_class_stereotype]

    statistics_output_filename = f"inconsistencies_found.csv"
    statistics = test_results_folder + "\\" + statistics_output_filename

    if execution_number == 1:
        with open(statistics, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_header)
            writer.writerow(csv_row)
    else:
        with open(statistics, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)
