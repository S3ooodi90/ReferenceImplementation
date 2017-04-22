# S3Model
Shareable-Structured-Semantic Model (S3Model)
See the Documentation 'https://github.com/DataInsightsInc/S3Model/docs/index.html'


The S3Model Data Model (DM) XML Schema file is named using the UUID of the complexType restriction of ConceptType from the RM. The UUID is prepended with 'dm-' and has the file extension '.xsd'.


The rdf:about attribute of the rdf:Description defining the RDF/XML Subject prepends the file name with 'http://www.s3model.com/ns/s3m/'.  This rdf:Description then contains each Predicate/Object pair.


All Reference Models are named with their version number and are dereferenceable in the '/ns/s3m/' folder on the site. I.e. http://www.s3model.com/ns/s3m/s3model_1_0_0.xsd

The complexTypes in the RM named Xd* all descend from XdAnyType where Xd denotes eXtended Datatype. 
