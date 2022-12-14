﻿# OntCatOWL-Tester

Software used for testing OntCatOWL on OntoUML/UFO Catalog datasets.

## Description

The OntCatOWL-Tester is a software developed with two main purposes: (i) to build the infrastructure for running multiple OntCatOWL tests on the OntoUML/UFO Catalog datasets; and (ii) to be the place where these tests are implemented and executed from.

The FAIR Model Catalog for Ontology-Driven Conceptual Modeling Research, short-named [OntoUML/UFO Catalog](https://github.com/unibz-core/ontouml-models), is a structured and open-source catalog that contains OntoUML and UFO ontology models. The catalog was conceived to allow collaborative work and to be easily accessible to all its users. Its goal is to support empirical research in OntoUML and UFO, as well as for the general conceptual modeling area, by providing high-quality curated, structured, and machine-processable data on why, where, and how different modeling approaches are used. The catalog offers a diverse collection of conceptual models, created by modelers with varying modeling skills, for a range of domains, and for different purposes.

[OntCatOWL](https://github.com/unibz-core/OntCatOWL) is the abbreviated name for Identification of Ontological Categories for OWL Ontologies, a software that aims to support the semi-automatic semantic improvement of lightweight web ontologies. We aim to reach the referred semantic improvement via the association of [gUFO](https://nemo-ufes.github.io/gufo/)—a lightweight implementation of the [Unified Foundational Ontology (UFO)](https://nemo.inf.ufes.br/wp-content/uploads/ufo_unified_foundational_ontology_2021.pdf)—concepts to the OWL entities. The aim of gUFO is “*to provide a lightweight implementation of the Unified Foundational Ontology (UFO) suitable for Semantic Web OWL 2 DL applications*”.

Results of the tests performed using the OntCatOWL-Tester are available at the [OntCatOWL-Dataset](https://github.com/unibz-core/OntCatOWL-Dataset). The aim of the publication of the resulting datasets is to share with the community data that can be analyzed in different ways, even though all executed tests are totally reproducible.

This document presents the functionalities provided by the OntCatOWL-Tester, informing how it can be used for automating tests on the OntCatOWL. For a complete comprehension of the [OntCatOWL, please refer to its repository](https://github.com/unibz-core/OntCatOWL). For descriptions about the structure of the files generated by the OntCatOWL-Tester and for accessing the tests’ data, access the [OntCatOWL-Dataset repository](https://github.com/unibz-core/OntCatOWL-Dataset).

## Contents

- [Installing and Running](#installing-and-running)
- [Implemented Functionalities](#implemented-functionalities)
- [Contributors](#contributors)
- [Acknowledgements](#acknowledgements)

## Installing and Running

You need to [download and install Python](https://www.python.org/downloads/) for executing the OntCatOWL-Tester. Its code was developed and tested using Python v3.11.0.

For executing the Tester, first install OntCatOWL as a package running the following command on the terminal:

```shell

pip install git+<https://github.com/unibz-core/OntCatOWL.git>

```

For installing all other necessary dependencies, run the following command on the terminal:

```shell

pip install -r requirements.txt

```

The execution of each of the OntCatOWL-Tester functionalities are explained in their corresponding documentation sections. Please get in touch with this software’s contributors [using the provided links](https://github.com/unibz-core/OntCatOWL-Tester#contributors) or (preferably) [open an issue](https://github.com/unibz-core/OntCatOWL-Tester/issues) in case of doubts or problems found.

## Implemented Functionalities

Three functionalities are available in the OntCatOWL-Tester. The first one (*build*) is mandatory for the execution of the two last ones, which are the tests over the OntoUML/UFO Catalog. The functionalities are:

- **Build:** create directory structure and files
  - [Description and execution instructions](https://github.com/unibz-core/OntCatOWL-Tester/blob/main/documentation/OntCatOWL-Tester-Build.md)
  - [Generated file’s structures (OntCatOWL-Dataset repository)](https://github.com/unibz-core/OntCatOWL-Dataset#build-generated-files)
- **Test 1:** single class used as input
  - Description and execution instructions **(link to be created)**
  - [Generated file’s structures (OntCatOWL-Dataset repository)](https://github.com/unibz-core/OntCatOWL-Dataset/blob/main/documentation/OntCatOWL-Dataset-Test1.md)
- **Test 2:** increasing percentage of classes used as input
  - Description and execution instructions **(link to be created)**
  - [Generated file’s structures (OntCatOWL-Dataset repository)](https://github.com/unibz-core/OntCatOWL-Dataset/blob/main/documentation/OntCatOWL-Dataset-Test2.md)

## Contributors

- PhD. Pedro Paulo Favato Barcelos [[GitHub](https://github.com/pedropaulofb)] [[LinkedIn](https://www.linkedin.com/in/pedropaulofavatobarcelos/)]
- PhD. Tiago Prince Sales [[GitHub](https://github.com/tgoprince)] [[LinkedIn](https://www.linkedin.com/in/tiagosales/)]
- MSc. Elena Romanenko [[GitHub](https://github.com/mozzherina)] [[LinkedIn](https://www.linkedin.com/in/mozzherina/)]
- Prof. PhD. Giancarlo Guizzardi [[LinkedIn](https://www.linkedin.com/in/giancarloguizzardibb51aa75/)]
- Eng. MSc. Gal Engelberg [[GitHub](https://github.com/GalEngelberg)] [[LinkedIn](https://www.linkedin.com/in/galengelberg/)]
- MBA Dan Klein [[GitHub](https://github.com/danklein10)] [[LinkedIn](https://www.linkedin.com/in/~danklein/)]

## Acknowledgements

This work is a collaboration between the Free University of Bozen-Bolzano, the University of Twente, and Accenture Israel Cybersecurity Labs.
