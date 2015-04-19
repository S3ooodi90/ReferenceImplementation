Example queries for S3Model data
==================================

Find the DvBooleanType(d) elements in a data set. 

    PREFIX s3m: <http://www.s3model.com/>
    PREFIX sem: <http://marklogic.com/semantics>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT *

    WHERE { ?el a ?ct .
           ?ct rdfs:subClassOf <s3m:DvBooleanType> .
          } 

Find the one with a specific label:

    PREFIX s3m: <http://www.s3model.com/>
    PREFIX sem: <http://marklogic.com/semantics>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT *

    WHERE { ?el a ?ct .
           ?ct rdfs:subClassOf <s3m:DvBooleanType> .
           ?ct rdfs:label 'Test DvBoolean'.
          } 

Find with with a specific source document definition:

    PREFIX s3m: <http://www.s3model.com/>
    PREFIX sem: <http://marklogic.com/semantics>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT *

    WHERE { ?el a ?ct .
           ?ct rdfs:subClassOf <s3m:DvBooleanType> .
           ?ct rdfs:isDefinedBy <http://bvsms.saude.gov.br/bvs/periodicos/boletim_eletronico_epi_ano04_n04.pdf>.
          } 


Use DESCRIBE to return more information about the complexType:

    PREFIX s3m: <http://www.s3model.com/>
    PREFIX sem: <http://marklogic.com/semantics>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    DESCRIBE ?ct

    WHERE { ?el a ?ct .
           ?ct rdfs:subClassOf <s3m:DvBooleanType> .
          } 

Find all of the triples where the subject is a data-name:

    PREFIX s3m: <http://www.s3model.com/>
    PREFIX sem: <http://marklogic.com/semantics>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX cts: <http://marklogic.com/cts#>

    SELECT *

    WHERE { ?s ?p ?o .
           FILTER(cts:contains(?s, "data-name") )
          } 

Find all of the triples where the subject is a data-name and the text contains 'test':

    PREFIX s3m: <http://www.s3model.com/>
    PREFIX sem: <http://marklogic.com/semantics>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX cts: <http://marklogic.com/cts#>

    SELECT *

    WHERE { ?s ?p ?o .
           FILTER(cts:contains(?s, "data-name") )
           FILTER(cts:contains(?o, "test") )
          } 




