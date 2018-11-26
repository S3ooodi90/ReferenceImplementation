====================
Linked Data Modeling
====================

Background
----------

Initial approaches to building ontologies for S3Model used the XML Schema to OWL approach that has been published several times in the academic literature. However, it was learned over these attempts that this is a single level mindset and approach.  It simply does not express the richness of S3Model. The results of those approaches represent the reference implementation of S3Model and not the overall concept.

When we began S3Model in 2009, we intended to use the OWL language as the basis on which to build the concepts. This is the same approach attempted or currently being attempted by other interoperability projects. However, the Open World Assumption conflicts with constraint-based modeling at the S3Model core. 

As the Linked Data environment matures, graph-based technologies are becoming mainstream for data discovery and analysis. By using a combination of XML Schema (to model the structural and syntactic needs) and RDF (to model semantics) we create the best of all worlds towards **computable semantic interoperability**. 

In this document, when we talk about S3Model, we use the term *S3Model* or *S3M*. When we talk about modeling concepts in an area of interest, we use the term *domain*. 

Syntactic Modeling
------------------

The complex nature of interacting with cross-domain concepts and query needs requires a rigorous yet flexible structural approach to modeling. Using a multi-level approach built on a robust data model fulfills this need. The `Reference Model <rm.html>`_ consists of a minimum of components required to construct robust models. Designed around the ubiquitous XML Schema data model provides a reliable, standardized, implementable infrastructure. The Reference Model reference implementation is expressed in XML Schema.

Components of the Reference Model can be assembled in virtually any structure need to express any level of granularity of healthcare or other domain concepts. These components are assembled in an XML Schema that contains only constraints (restrictions) of the Reference Model components.  This constraint-based approach guarantees that the structure and syntax of all domain concept models are valid against the Reference Model.

This guarantee means that it is easier to build persistence and query infrastructure that can accommodate unforeseen domain concept models. This capability reduces application complexity and maintenance.

Semantic Modeling
-----------------

The S3Model environment defines a few semantics to relate various components. Each Reference Model defines semantics for each component.

Each particular domain concept model is based on one and only one Reference Model release. A domain expert determines the proper domain semantics for their domain concept model.

RDF provides an elegant and straightforward approach to expressing semantics. Besides, the variety of syntaxes available to express the *Subject, Predicate, Object* statements provides an excellent solution.

The Reference Model and domain concept models are authored in XML Schema, and therefore the canonical RDF syntax of RDF/XML is used in these instances. The syntax used to represent these in implementations is left up to the systems developers. The specifications include the RDF/XML semantics in the XML Schema to facilitate exchange and governance of the Reference Model. For convenience, there is also an extract of the semantics in RDF/XML and JSON-LD.

The Python utilities used to perform this extraction are included as examples of working with S3Model models. There is also a utility for extracting semantics in RDF/XML and JSON-LD from domain concept models. These utilities use XPath and XSLT for extraction and conversion. These simple scripts can be implemented in any chosen programming language.


S3Model Semantics
-----------------

These are the entities defined in the core ontology `s3model.owl <http://datainsights.tech/S3Model/owl/>`_

Classes
=======

    * S3Model
    * RM
    * ConceptModel

        * CoreMC
        * PluggableCM

    * Symbol

        * CoreCS
        * PluggableCS

    * DMInstance
    * DataInstance

        * DataInstanceValid
        * DataInstanceInvalid
        * DataInstanceError

    * Exception


Object Properties
-----------------

  * isS3Modelobjprop

    * isCoreModelIn
    * isPluggableModelIn
    * isCoreSymbolOf
    * isPluggableSymbolOf
    * isSubSymbolIn
    * refersToSymbol

Datatype Properties
-------------------
Some tools do not support the full range of XML Schema datatypes directly. We defined these in the ontotlogy as well.

  * duration
  * gDay
  * gMonth
  * gYear
  * gYearMonth
  * gMonthDay

Annotation Properties
---------------------

The most widely used (at this writing) metadata definitions come from the Dublin Core Metadata Initiative (DCMI) terms. However, the definitions for these do not meet the requirements for some reasoners. We have defined our metadata properties and related them to other standards.

Linked Data Tools
=================
To reduce the learning curve for working with S3Model data in your Linked Data environment, we have included a few simple Python scripts to get you started. See the utils/README.md for details.

The open source tool `Kunteksto <https://datainsights.tech/Kunteksto/index.html>`_ is used to transform flat CSV data in semantically enriched linked data.

The Python implementation is the foundation of the `training materials <https://datainsights.tech/training>`_ and also available as an `open source library <https://pypi.org/project/S3MPython/>`_.
