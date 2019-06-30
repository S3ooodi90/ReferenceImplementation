================
Additional Tools
================

The reference implementation also provides a few simple tools in Python that can be used to manipulate and analyze the refernce model implementation and support files such as the ontology and RDF output.

You will find them in the *scripts* subdirectory of the versioned RM. Ex: *RM/3_1_0/scripts*.


data_semantics_extractor.py
---------------------------

Extracts S3Model 3.1.0 (and later) data and creates RDF triples in RDF/XML
This script must be executed after the dm_semantics_extractor.py script.


demo_data_gen.py
----------------

Can be used to create multiple copies of DM based data files to use for examples or stress testing your RDF store.
Pass the number of copies per example on the commandline.



dm_semantics_extractor.py
-------------------------

Extracts the semantics from S3Model DMs in the directory passed on the commandline and creates RDF triples in RDF/XML format. It reuses the filename and replaces
'.xml' with '.rdf'



rm_semantics_extractor.py
-------------------------

Extracts the semantics from S3Model RM and creates RDF triples in RDF/XML named the same as the input file with a .rdf extension in place of the .xsd extension.





Using the tools
===============

You need to install the requirements in a virtual environment before using these tools. If you do not already have a favorite approach to Python virtual environments then the best way is to use `Anaconda <https://www.anaconda.com/>`_. Download and install a distribution for your operating system.

Then in a terminal window execute:

.. code-block:: sh

    conda env create -f s3m_environment.yml

Then follow the instructions to activate the environment.




