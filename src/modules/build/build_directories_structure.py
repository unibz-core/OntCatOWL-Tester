""" Functions related to OS files and strings used for general purposes. """
import os
import glob

from src.modules.tester.logger_config import initialize_logger


def get_list_ttl_files(directory_path) -> list:
    """ Receives the path of a directory and returns a list of all *.ttl files in all sub-folders. """
    logger = initialize_logger()
    file_names = []

    # checking whether folder/directory exists
    if not os.path.exists(directory_path):
        logger.error(f"OntoUML/UFO Catalog directory {directory_path} does not exist. Exiting program.")
        exit(1)
    else:  # if yes, collect all ttl files we have
        for file in glob.glob(directory_path + "/*/ontology.ttl"):
            file_names.append(file)

    return file_names


def _create_folder(path, ok_message="The folder was created", existed_message=""):
    logger = initialize_logger()

    if not os.path.exists(path):
        try:
            os.makedirs(path)
            logger.info(f"{ok_message}: {path}.")
        except OSError as error:
            logger.error(f"Directory {path} could not be created. Program aborted.\n"
                         f"System error reported: {error}")
    elif existed_message:
        logger.info(f"{existed_message}: {path}.")


def create_internal_catalog_path(catalog_path):
    _create_folder(catalog_path, "Internal catalog directory created")


def create_test_results_folder(test_results_folder):
    _create_folder(test_results_folder, "Test results directory created")


def create_test_directory_folders_structure(dataset_folder, catalog_size, current):
    _create_folder(dataset_folder,
                   ok_message=f"Directory {current}/{catalog_size} created",
                   existed_message=f"Directory {current}/{catalog_size} already exists")