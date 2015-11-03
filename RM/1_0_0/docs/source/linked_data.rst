====================
Linked Data Modeling
====================

Background
==========
Initial approaches to building ontologies for S3Model used the XML Schema to OWL approach that has been published several times in academic literature. However, it was learned over these attempts that this is a single level mindset and approach.  It simply does not express the richness of S3Model. The results of those approaches represent the reference implementation of S3Model and not the overall concept.

When we began S3Model in 2009, we intended to use OWL as the basis on which to build the concepts. However, the Open World Assumption is in conflict with constraint based modeling at the S3Model core.

As the Linked Data environment matures, graph based technologies are becomming mainstream for data discovery and analysis. By using both XML Schema 1.1 to model the structural and syntactic needs and RDF to model semantics we create the best of all worlds towards **computable semantic interoperability**.

In this document, when we talk about S3Model we will use the term *S3Model*. When we talk about modeling concepts in an area of interest we use the term *domain*.  Though we are thinking primarily about the domain of healthcare and the information technology to support healthcare information exchange, S3Model concepts may be applied to any domain of interest.

Syntactic Modeling
==================

The complex nature of healthcare concepts and query needs requires a rigourous yet flexible structural approach to modeling. Using a multi-level approach built on a solid data model fulfills this need. The Reference Model consists of a minimum of components required to construct robust models. Desgined around the ubiquitous XML Schema data model provides a solid, standardized, implementable infrastructure. The Reference Model reference implementation is realized in XML Schema 1.1.

Components of the Reference Model can be assembled in virtually any structure need to express any level of granularity of healthcare or other domain concepts. These components are assembled in an XML Schema that contains only constraints (restrictions) of the Reference Model components.  This constraint based approach guarantees that the structure and syntax of all domain concept models are valid against the Reference Model.

This guarantee means that it is easier to build persistence and query infrastructure that can accomodate unforseen domain concept models. This greatly reduces application complexity and maintenance.

Semantic Modeling
=================

The S3Model environment defines a few semantics to relate various components. Each Reference Model defines semantics for each component.

Each paticular domain concept model is based on one and only one Reference Model release. A domain expert determines the proper domain semantics for their domain concept model. In order to be S3Model compliant there are required semantics relating the domain concept model to its parent Reference Model.

RDF provides an elegant and simple approach to expressing semantics. In addition, the variety of syntaxes available to express the *Subject, Predicate, Object* statements provides an excellent solution.

The Reference Model and domain concept models are authored in XML Schema and therefore the canonical RDF syntax of RDF/XML is used in these instances. The syntax used to represent these in implementations is left up to the systems developers. The specifications include the RDF/XML semantics in the XML Schema in order to facilitate easy exchange and governance of the Reference Model. For convienence there is also an extract of the semantics in RDF/XML and JSON-LD.

The Python utilities used to perform this extraction are included as examples of working with S3Model models. There is also a utility for extracting semantics in RDF/XML and JSON-LD from domain concept models.


S3Model2 Semantics
================

These are the entities defined in `S3Model2.rdf <http://www.S3Model.org/ns/S3Model2/S3Model2.rdf>`_

Top-Level
=========

    * S3Model2
    * RM
    * ConceptModel

        * CoreMC
        * PluggableCM

    * Symbol

        * CoreCS
        * PluggableCS

    * CCDInstance
    * DataInstance

        * DataInstanceValid
        * DataInstanceInvalid
        * DataInstanceError

    * Exception


Other Properties
=================

  * isS3Model2objprop

    * isCoreModelIn
    * isPluggableModelIn
    * isCoreSymbolOf
    * isPluggableSymbolOf
    * isSubSymbolIn
    * refersToSymbol

Datatype Properties
===================
Some tools (e.g. Protégé) do not support the full range of XML Schema 1.1 datatypes directly. We defined these in S3Model2.rdf as well.

  * duration
  * yearMonthDuration
  * dayTimeDuration
  * gDay
  * gMonth
  * gYear
  * gYearMonth
  * gMonthDay

Annotation Properties
=====================
The most widely used (at this writing) metadata definitions come from the Dublin Core Metadata Initiative (DCMI) terms. However, the definitions for these do not meet the requirements for some reasoners. We have defined our own metadata properties and related them to other standards.

Context processing
==================
Refer to the JSON-LD-API `context processing <http://www.w3.org/TR/json-ld-api/#context-processing-algorithms>`_ specifications to understand how the S3Model2.jsonld, S3Model250.jsonld and the ccd jsonld work together.

For setting your JSON-LD processor for the correct location of context files, see this `StackExchange <https://stackoverflow.com/questions/32047434/json-ld-external-context-redirect/32105641>`_ discussion. The options for compliant processors is discussed in the `JSON-LD Specs <http://www.w3.org/TR/json-ld-api/#the-jsonldoptions-type>`_

Linked Data Tools
=================
To reduce the learning curve for working with S3Model data in your Linked Data environment we have included a few simple Python scripts to get you started. See the utils/README.md for details.
