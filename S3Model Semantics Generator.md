S3Model Semantics Generator
===========================

This tool collects the semantics from your S3Models and applies those semantics to your XML data. It does so by creating a RDF/XML triples file for each file. These files are ready to be uploaded to your favorite Triple Store or imported by your visualization tool. 

The semantics generator uses a configuration file to find your data, concept models and reference models. It does not check for the S3Model.owl base ontology or any XML catalog files. 

The configuration file must be located in the same directory as S3Model_Semantics.py it is named: config.ini 

Edit the config.ini file with a text editor to set the proper paths for your installation.
The default config.ini file looks like this:

    [PATHS]
    RM_PATH = rm_lib/
    CM_PATH = cm_lib/ 
    XML_PATH = xml_data/ 
    RDF_PATH = rdf_data/


This is what each option means:

    RM_PATH - this is where your reference model schema(s) is/are located.
    CM_PATH - this is where your concept model schema(s) is/are located.
    XML_PATH - this is the location of your XML data instances.
    RDF_PATH - this is the output directory to write your RDF files into. 



The generator examines your data to determine the required concept model schema(s). Then it looks at those schemas to determine the required reference model schema(s).    

The data files are assumed to have a .xml extension and the models are assumed to have a .xsd extension. If your data is in JSON formatted files then those files should first be converted to equivalent XML files. 

If required schemas are missing the generator exits with an error message explaining what is missing. 

Once all schemas have been located the generator will create an RDF/XML file for each reference model, each concept model and each XML data file, in the RDF_PATH root directory.  

These files are now ready to be imported to your Triple Store. 


