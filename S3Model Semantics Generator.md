S3Model Semantics Generator
===========================

The semantics builder uses a configuration file to find your data, concept models and reference models. It does not check for the S3Model.owl base ontology or any XML catalog files. 

The configuration file must be located in the same directory as S3Model_Semantics.py it is named: config.ini 

Edit the config.ini file with a text editor to set the proper paths for your installation.
The default config.ini file looks like this:

    [PATHS]
    RM_PATH = RM_LIB/
    CM_PATH = CM_LIB/ 
    XML_PATH = xml_data/ 
    RDF_PATH = rdf_data/


This is what option means:

    RM_PATH - this is where your reference model schema(s) is/are located.
    CM_PATH - this is where your concept model schema(s) is/are located.
    XML_PATH - this is the location of your XML data instances.
    RDF_PATH - this is the output directory to write your RDF files into. 


    
