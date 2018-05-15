=================
Modeling Concepts
=================

Approach
========

The S3Model Reference Model provides extended datatypes and a document-like structure capability to enhance interoperability across disparate systems. This concept is the foundation of the **modern data-centric information management** world. The business case for becoming *data-centric* is detailed in other sections. 

The fundamental concepts, expressed in the reference model classes, are based on primary philosophical concepts of real-world entities. These broad concepts can then be constrained to more specific concepts using models created by domain experts. These `Data Models (DMs) <rm.html#dmtype>`_ created by domain experts provides the ability for their *tacit knowledge* to be directly encoded into a model-driven system. A subject matter/domain expert,  trained in using the tools and concepts of S3Model can create **computable models** that are not available through any other methodology.

The attempt to design a data model for a concept is restricted to the knowledge and context of a particular domain expert. In effect, there can never be one *best* or a *maximal* data model for human concepts to be communicated to machines. What this means is that from a global perspective there may be several DMs that purport to fill the same need. However, are slightly different due to the many human factors involved in their design. 

There is no conflict in the S3Model world in this case as DMs are identified using a CUID, and there is no semantics in the processing and validation model. The machine only knows what you tell it the context is for this model.

The real advantage to using the S3Model approach to information modeling is that it provides for a wide variety of applications to be developed based on the broad concepts defined in the reference model. By having domain experts within their fields, model and generate the DMs, they can then be shared across multiple applications so that the structure and semantics of the data are not locked into one specific software application, but can be exchanged among many different software applications. **This approach provides the real foundation for artificial intelligence to move forward instead of being isolated in each instance of implementation as it is today.** 

To demonstrate the differences between the S3Model approach and the typical data model design approach we use two common metaphors. Here we are assuming the reference implementation based on XML Schema.

1. The first is for the data model approach to developing software. This approach is where a set of database definitions are created based on a requirements statement representing an information model. An application is then designed to support all of the functionality required to input, manipulate and output this data as information, all built around the data model. This approach is akin to a jigsaw puzzle (the software application) where the shape of the pieces are the syntax, and the design and colors are the semantics of the information represented in the aggregation of data components described by the model. This process produces an application that, like the jigsaw puzzle, can provide for pieces (information) to be exchanged only between exact copies of the same jigsaw puzzle. If you were to try to put the puzzle pieces from one jigsaw puzzle into a different jigsaw puzzle, you might find that a puzzle piece has the same shape (syntax) but the picture on the puzzle piece (semantics) will not be the same. Even though they both belong to the same domain of jigsaw puzzles, you can see that getting a piece from one jigsaw puzzle to correctly fit into another is going to require manipulation of the underlying syntax (shape) and semantics (picture) of the puzzle piece. This approach can be extended to the relationship that the jigsaw puzzle has a defined limit of its four sides. It cannot, reasonably, be extended to incorporate new pieces (concepts) discovered after the initial design.

2. The multi-level, data-centric approach used in S3Model is akin to creating models (applications) using the popular toy blocks made by Lego® and other companies. If you compare a box of these interlocking blocks to the reference model and the instructions to creating a specific toy model (software application), where these instructions present a concept constraint (implemented as a DM in S3Model). You can see that the same blocks can be used to represent multiple toy models without any change to the physical shape, size or color of each block. Now we can see that when new concepts are created, they can be represented as instructions for building a new toy model using the same fundamental building blocks that the original software applications used.

So, the various applications are now part of a more extensive infrastructure or ecosystem of interoperability. Any software application that understands the reference model can now interpret the meaning conveyed in constraint definitions.

Constraint Definitions
----------------------
Shareable Data Models (DMs) can be created using an XML Schema editor or even a plain text editor. However, this is not a recommended approach. Realistic DMs can be several hundred and up to thousands of lines long. They also require `CUIDs <https://github.com/ericelliott/cuid>`_ to be created as complexType and element names. These CUIDs should be machine generated.

Data Insights, Inc. has a Data Model Generator as part of the `Datacentric Tools Suite <https://datainsights.tech/datacentrictools/>`_. 


DM Identification
------------------
The root element of a DM and all complexType and global elements use CUIDs as defined by https://github.com/ericelliott/cuid 
The filename of a DM may use any format specified by the DM author. The DM author must be aware that the `metadata section <rm.html#dmtype>`_ of the DM must contain the correct RDF:about URI with this filename. 

As a matter of consistency and to avoid any possible name clashes, the DMs created by the DMGen also use the DM ID (dm-<cuid>.xsd). 

To be a viable DM for validation purposes, the DM should use the W3C assigned extension of '.xsd.' Many tools may still process the artifact as an XML Schema without the standard file extension.

The S3Model community considers it a matter of best practice in artifact management practice to use the DM ID with the *.xsd* extension, as the filename.

DM Versioning
--------------
These specifications do not support versioning of DMs. Though XML Schema does have supporting concepts for versioning of schemas, this is not desirable in DMs. The reasons for this decision focuses primarily on the ability to capture the original temporal and ontological semantics for data instances and maintain them for all time. We call this future proofing your data.

A key feature of S3Model is the ability to guarantee the semantics are consistent for any given data instance, for all future time. We determined that any change in the structure or semantics of a DM constitutes a new DM. Since the complexTypes are re-usable (See the RMC description below), an approach that tools should use is to allow a modeler to copy an existing DM and assign a new DM ID to this new DM. Then, allow editing of the required RMCs to meet the new requirements, before publishing the new DM. Reusing RMCs across DMs improves the ability to perform cross-domain data analysis.

When a complexType is changed within this new DM, all of the ancestors in the document model must also be assigned a new name along with its global element name. For example, if the enumerations on an XdStringType restriction are modified, the XdStringType, the wrapper XdAdapterType, the parent ClusterType, any enclosing ClusterTypes,  and the DMType must all get new CUIDs. The DMGen is aware of these requirements and makes this an easier task than manual editing the XML Schema model.

Model Components (MCs)
-------------------------------
S3Model DMs are made up of XML Schema complexTypes composed by restriction of the Reference Model complexTypes. The *by restriction* requirement is the foundation of interoperability. No valid DM can add to the content of the RM Schema that it imports.

What is in the Reference Model is the superset of all DMs. Because a unique identifier is used for the complexType names, they are reusable components. 

For example, a domain expert might model a complexType that is a restriction of XdStringType with the enumerations for selecting one of the three measurement systems for temperature; Fahrenheit, Kelvin, and Celsius. This RMC, as well as many others, can be reused in many DMs without modification.

For this reason, the semantic links for RMCs are directly expressed in an xs:appinfo section in each MC. This approach lends itself very well to the creation of RDF triples from this information. For example::



	<xs:appinfo>
	  <rdf:Description rdf:about='&s3m;mc-3a54417d-d1d6-4294-b868-e7a9ab28f8c4'>
	    <rdfs:isDefinedBy rdf:resource='http%3A//purl.obolibrary.org/obo/RO_0002371'/>
	  </rdf:Description>
	</xs:appinfo>


In this example the subject is &s3m;mc-3a54417d-d1d6-4294-b868-e7a9ab28f8c4 the predicate is rdfs:isDefinedBy and the object is http%3A//purl.obolibrary.org/obo/RO_0002371

Every xs:appinfo section must begin with the rdf:Description element and have the rdf:about attribute to define the subject, as the containing complexType. Those elements are followed by one or more predicate/object components. The predicates can be from any vocabulary/terminology. Just be sure that the namespace prefix is correctly defined in the DM header. The Datacentric Tools Suite includes common namespaces by default, but others may be added as needed. Also be sure that any URLs are correctly encoded so that they are valid inside the DM.
RDF triples are a cornerstone of the semantic web and linked data processing. For more information see this tutorial. Of particular interest here is the section titled; Introducing RDF/XML. RDF/XML is one of the syntaxes used to describe semantic links, and it is what we use in S3Model.
