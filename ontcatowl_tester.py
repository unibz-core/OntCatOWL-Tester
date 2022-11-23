""" Main module for the OntoCatOWL-Catalog Tester. """
import pathlib
from copy import deepcopy

from rdflib import URIRef, RDF

from modules.build.build_classes_stereotypes_information import collect_stereotypes_classes_information
from modules.build.build_directories_structure import get_list_unhidden_directories, \
    create_test_directory_folders_structure, create_test_results_folder
from modules.build.build_information_classes import saves_dataset_csv_classes_data
from modules.build.build_taxonomy_classes_information import collect_taxonomy_information
from modules.build.build_taxonomy_files import create_taxonomy_files
from modules.ontcatowl.ontcatowl import run_ontcatowl
from modules.run.run_data_structures import load_baseline_dictionary, create_yaml_classes_output, remaps_to_gufo, \
    generate_times_csv_output
from modules.tester.input_arguments import treat_arguments
from modules.tester.logger_config import initialize_logger
from modules.tester.utils_rdf import load_graph_safely

SOFTWARE_ACRONYM = "OntCatOWL Tester"
SOFTWARE_NAME = "Tester for the Identification of Ontological Categories for OWL Ontologies"
SOFTWARE_VERSION = "0.22.11.22"
SOFTWARE_URL = "https://github.com/unibz-core/OntCatOWL-Tester"

NAMESPACE_GUFO = "http://purl.org/nemo/gufo#"
NAMESPACE_TAXONOMY = "http://taxonomy.model/"


def build_ontcatowl_tester(catalog_path):
    """ Build function for the OntoCatOWL-Catalog Tester. """

    # DATA GENERATION FOR TESTS

    # Building directories structure
    list_datasets = get_list_unhidden_directories(catalog_path)
    list_datasets.sort()
    catalog_size = len(list_datasets)
    logger.info(f"The catalog contains {catalog_size} datasets.\n")

    current = 1

    for dataset in list_datasets[5:10]:
        logger.info(f"### Starting dataset {current}/{catalog_size}: {dataset} ###\n")

        create_test_directory_folders_structure(dataset, catalog_size, current)

        # Building taxonomies files and collecting information from classes
        create_taxonomy_files(catalog_path, dataset, catalog_size, current)

        # Builds dataset_classes_information and collects attributes name, prefixed_name, and all taxonomic information
        dataset_classes_information = collect_taxonomy_information(dataset, catalog_size, current)

        # Collects stereotype_original and stereotype_gufo for dataset_classes_information
        collect_stereotypes_classes_information(catalog_path, dataset_classes_information,
                                                dataset, catalog_size, current)

        saves_dataset_csv_classes_data(dataset_classes_information, dataset, catalog_size, current)

        current += 1


def run_ontcatowl_tester(catalog_path):
    list_datasets = get_list_unhidden_directories(catalog_path)
    list_datasets.sort()
    list_datasets_paths = []
    list_datasets_taxonomies = []

    global_configurations = {"is_automatic": True,
                             "is_complete": False}

    # Creating list of dataset paths and taxonomies
    for dataset in list_datasets:

        logger.info(f"Starting OntCatOWL for {dataset}")

        tester_catalog_folder = str(pathlib.Path().resolve()) + r"\catalog"
        dataset_folder = tester_catalog_folder + "\\" + dataset
        list_datasets_paths.append(dataset_folder)
        dataset_taxonomy = dataset_folder + "\\" + "taxonomy.ttl"
        list_datasets_taxonomies.append(dataset_taxonomy)

        input_classes_list = load_baseline_dictionary(dataset)
        input_graph = load_graph_safely(dataset_taxonomy)

        test_name = "test1_an"
        test_results_folder = dataset_folder + "\\" + test_name
        create_test_results_folder(test_results_folder)

        # Executions of the test
        execution_number = 1
        tests_total = len(input_classes_list)

        for input_class in input_classes_list:
            execution_name = test_name + "_exec" + str(execution_number)

            working_graph = deepcopy(input_graph)
            triple_subject = URIRef(NAMESPACE_TAXONOMY + input_class.class_name)
            triple_predicate = RDF.type
            class_gufo_type = remaps_to_gufo(input_class.class_stereotype)
            triple_object = URIRef(class_gufo_type)
            working_graph.add((triple_subject, triple_predicate, triple_object))
            working_graph.bind("gufo", "http://purl.org/nemo/gufo#")

            ontology_dataclass_list, time_register, consolidated_statistics = run_ontcatowl(global_configurations,
                                                                                            working_graph)

            # Creating resulting files
            create_yaml_classes_output(input_class, ontology_dataclass_list, test_results_folder, execution_name)
            # generate_times_csv_output(time_register)
            # generate_statistics_csv_output(consolidated_statistics)

            logger.info(f"Test {execution_number}/{tests_total} for input class {input_class.class_name} executed.")
            execution_number += 1
        exit(2)


if __name__ == '__main__':

    logger = initialize_logger()

    arguments = treat_arguments(SOFTWARE_ACRONYM, SOFTWARE_NAME, SOFTWARE_VERSION, SOFTWARE_URL)

    # Execute in BUILD mode.
    if arguments["build"]:
        build_ontcatowl_tester(arguments["catalog_path"])

    # Execute in RUN mode.
    if arguments["run"]:
        run_ontcatowl_tester(arguments["catalog_path"])

# TODO (@pedropaulofb): VERIFY
# Are there any classes with more than one stereotype?
# Try to clean garbage classes for creating better statistics
# The following datasets don't have any taxonomy and were removed by hand:
# - chartered-service, experiment2013, gailly2016value, pereira2020ontotrans, zhou2017hazard-ontology-robotic-strolling, zhou2017hazard-ontology-train-control
# van-ee2021modular - RecursionError: maximum recursion depth exceeded while calling a Python object
