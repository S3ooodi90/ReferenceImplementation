# S3Model
Shareable-Structured-Semantic Model (S3Model)
See the Documentation 'https://github.com/DataInsightsInc/S3Model/docs/index.html'


A S3Model Data Model (DM) XML Schema file is named using the UUID of the complexType restriction of ConceptType from the RM. The UUID is prepended with 'dm-' and has the file extension '.xsd'.


The rdf:about attribute of the rdf:Description defining the RDF/XML Subject prepends the file name with 'http://www.s3model.com/ns/s3m/'.  This rdf:Description then contains each Predicate/Object pair.


All Reference Models are named with their version number and are dereferenceable in the '/ns/s3m/' folder on the site. I.e. http://www.s3model.com/ns/s3m/s3model_1_0_0.xsd

The complexTypes in the RM named Xd* all descend from XdAnyType where Xd denotes eXtended Datatype. 

Python Implementation
=====================
The Python 3.7+ implementation is in located in the RM/<version>/pylib directory. 
There are tutorials included in the Jupyter notebooks. These are companions to the book
*Infotropic* Section 2. 

See the Getting Started notebook. 

You will need to install Anaconda for your platform. 
https://www.anaconda.com/download/


Then create the S3Model environement with:
::code bash
    $conda env create -f s3m_environment.yml 

