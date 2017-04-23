=================
Modeling Concepts
=================

Approach
========
The S3Model Reference Model reference implementation is implemented in a single XML Schema. The fundamental concepts, expressed in the reference model classes, are based on basic philosophical concepts of real world entities. These broad concepts can then be constrained to more specific concepts using models created by domain experts, in this case healthcare experts. These are called Data Models (DMs).

The attempt to design a data model for a concept is restricted to the knowledge and context of a particular domain expert. In effect, there can never be one *best* or a *maximal* data model for healthcare concepts. This means that from a global perspective there may be several DMs that purport to fill the same need.

There is no conflict in the S3Model world in this case as DMs are identified using a Type 4 UUID and there are no semantics in the processing and validation model.

The DM may be further constrained at the implementation level through the use of implementation templates in the selected framework. Examples are additional XML Schemas that provide further restrictions or HTML pages used for display and data form entry. These templates are constructed in the implementation and may or may not be sharable across applications depending upon the needs of the implementation.

The S3Model specifications do not play any role in defining what these templates look like or how they perform. They are only mentioned here as a way of making note that applications will require a user interface template layer to be functional. Th application UI as well as any transport layers between applications is outside the scope of the S3Model ecosystem.

**The interoperability layer remains at the DM instance level.**

The real advantage to using the S3Model approach to healthcare information modeling is that it provides for a wide variety of healthcare applications to be developed based on the broad concepts defined in the reference model. By having domain experts within the healthcare field to define and create the DMs, they can then be shared across multiple applications so that the structure and semantics of the data is not locked into one specific application, but can be exchanged among many different applications. This properly implements the separation of roles between IT and domain experts.

To demonstrate the differences between the S3Model approach and the typical data model design approach we will use two common metaphors. This is assuming the reference implementation based on XML Schema.

1. The first is for the data model approach to developing software. This is where a set of database definitions are created based on a requirements statement representing an information model. An application is then developed to support all of the functionality required to input, manipulate and output this data as information, all built around the data model. This approach is akin to a jigsaw puzzle (the software application) where the shape of the pieces are the syntax and the design and colors are the semantics of the information represented in an aggregation of data components described by the model. This produces an application that, like the jigsaw puzzle, can provide for pieces (information) to be exchanged only between exact copies of the same puzzle. If you were to try to put pieces from one puzzle into a different puzzle, you might find that a piece has the same shape (syntax) but the picture on the piece (semantics) will not be the same. Even though they both belong to the same domain of jigsaw puzzles. You can see that getting a piece from one puzzle to correctly fit into another is going to require manipulation of the basic syntax (shape) and / or semantics (picture) of the piece. This can also be extended to the relationship that the puzzle has a defined limit of its four sides. It cannot, reasonably, be extended to incorporate new pieces (concepts) discovered after the initial design.

2. The multi-level approach used in S3Model is akin to creating models (applications) using the popular toy blocks made by Lego® and other companies. If you compare a box of these interlocking blocks to the reference model and the instructions to creating a specific toy model (software application), where these instructions present a concept constraint (implemented as a DM in S3Model). You can see that the same blocks can be used to represent multiple toy models without any change to the physical shape, size or color of each block. Now we can see that when new concepts are created within healthcare, they can be represented as instructions for building a new toy model using the same fundamental building blocks that the original software applications were created upon.
So, the various applications are now part of a larger infrastructure or ecosystem of interoperability. Any application that understands the reference model can now interpret the meaning conveyed in constraint definitions.

Constraint Definitions
----------------------
Data Models (DMs) can be created using any XML Schema editor or even a plain text editor. However, this is not a recommended approach. Realistic DMs can be several hundred and up to thousands of lines long. They also require Type 4 UUIDs to be created as complexType and element names. These UUIDs should be machine generated.

Data Insights, Inc. has a Data Model Generator (DMGen) for license. 


DM Identification
------------------
The root element of a DM and all complexType and global elements will use 4 Type UUIDs as defined by the IETF RFC 4122 See: https://www.ietf.org/rfc/rfc4122.txt
The filename of a DM may use any format defined by the DM author. The DM author must recognize that the metadata section of the DM must contain the correct RDF:about URI with this filename. 

As a matter of consistency and to avoid any possible name clashes, the DMs created by the DMGen also use the DM ID (DM-<uuid>.xsd). To be a viable DM for validation purposes the DM should use the W3C assigned extension of '.xsd'. Though many tools may still process the artifact as an XML Schema without it.
The S3Model community considers it a matter of good artifact management practice to use the DM ID with the .xsd extension, as the filename.

DM Versioning
--------------
Versioning of DMs is not supported by these specifications. Though XML Schema 1.1 does have supporting concepts for versioning of schemas, this is not desirable in DMs. The reasons for this decision focuses primarily around the ability to capture temporal and ontological semantics for data instances and maintain them for all time (future proof data).
A key feature of S3Model is the ability to guarantee the semantics for all future time, as intended by the original modeler. We determined that any change in the structure or semantics of a DM, constitutes a new DM. Since the complexTypes are re-usable (See the PCM description below), an approach that tools should use is to allow for copying a DM and assigning a new DM ID. The editing the required PCMs before publishing the new DM. Reusing PCMs across DMs improves the ability to perform data analysis across time.

When a complexType is changed within this new DM, all ancestors (enclosing complexTypes) also must be assigned a new name along with its global element name. For example if the enumerations on a XdStringType restriction are changed, the XdStringType, the XdAdapterType, the parent ClusterType and any enclosing ClusterTypes, the EntryType and the DMType must all get new UUIDs. The DMGen is aware of these processes and makes this an easier task than manual editing.

Pluggable Concept Models (PCMs)
-------------------------------
S3Model DMs are made up of XML schema complexTypes composed by restriction of the Reference Model complexTypes. This is the foundation of interoperability.
What is in the Reference Model is the superset of all DMs. The Pluggable part of the name is given to the fact that due to their unique identification the complexTypes can be seen as re-usable components. For example, a domain expert might model a complexType that is a restriction of XdStringType with the enumerations for selecting one of the three measurement systems for temperature; Fahrenheit, Kelvin and Celsius. This PCM as well as many others can be reused in many DMs without modification.
For this reason, the semantic links for PCMs are directly expressed in an xs:appinfo section in each PCM. This approach lends itself very well to the creation of RDF triples from this information. For example::

  <xs:appinfo>
   <rdf:Description rdf:about='&S3Model;mc-3a54417d-d1d6-4294-b868-e7a9ab28f8c4'>
    <rdfs:isDefinedBy rdf:resource='http%3A//purl.obolibrary.org/obo/RO_0002371'/>
   </rdf:Description>
  </xs:appinfo>

In this example the subject is &S3Model;mc-3a54417d-d1d6-4294-b868-e7a9ab28f8c4 the predicate is rdfs:isDefinedBy and the object is http%3A//purl.obolibrary.org/obo/RO_0002371

Every xs:appinfo section must begin with the rdf:Description element and have the rdf:about attribute to define the subject, as the containing complexType. This is then followed by one or more predicate/object components. The predicates can be from any vocabulary/terminology. Just be certain that the namespace prefix is correctly defined in the DM header. The DM-Gen defines common namespaces by default but others may be added as needed. Also be certain that any URLs are properly encoded so that they will be valid inside the DM.
RDF triples are a cornerstone of the semantic web. For more information see this tutorial. Of particular interest here is the section titled; Introducing RDF/XML. RDF/XML is one of the syntaxes used to describe semantic links and it is what we use in S3Model. Another popular syntax you may see is called Turtle.
