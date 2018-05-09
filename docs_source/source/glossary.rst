========
Glossary
========

S3Model
-------
Shareable-Structured-Semantic Model (S3Model).  An open source/open content project with the goal of solving the healthcare information, semantic interoperability problem.

It uses a multi-level information modeling approach in combination with widely available tools and language infrastructure to allow the exchange of the syntactic and semantic information along with data.

Reference Model (RM)
--------------------
The RM is a small set of structurally oriented concept definitions that allow for building arbitrarily complex models without introducing domain semantics into the structure. Domain concepts are modeled as *restrictions* on these RM concepts. Then RM, therefore, defines a standard set of concepts that allow for query and knowledge discovery across data without prior knowledge of the actual content. See DM below.

Model Component (MC)
--------------------
The name comes from the fact that it is a complete XML Schema complexType that represents a simple concept and that it can be reused in any DM. This reuse is due to the use of CUIDs for the complexType name attribute. Since complexType names must begin with an alphabetic character, all S3Model MC names begin with the prefix 'mc-' followed by the CUID. This naming convention facilitates the association with public element names in instances since they reuse the CUID but have a prefix of 'ms-' (Model Symbol) in place of the 'mc-'. The use of a CUID allows the constraint on a reference model type to be reused many times in a DM with different parameters such as enumeration constraints. The semantics for a concept modeled as an MC is represented using Semantic Web technologies. The MC name is the subject in each of the *Subject, Predicate, Object* RDF statements.

Data Model (DM)
-----------------------------------
This component is a domain concept data model that is created by expressing constraints on a generic reference model. In the S3Model reference implementation eco-system, these constraints are created through the use of the XML Schema complexTypes using the *restriction element* with its *base attribute* set to the appropriate RM complexType. DMs are immutable, once published they are never edited because once data is published in conformance with a DM, this is where the sharable semantics are located.
DMs are uniquely identified by the prefix 'dm-' followed by a `CUID <https://github.com/ericelliott/cuid>`_. They are valid against one version of the S3Model Reference Model XML Schema. **This design gives them temporal durability and prevents the requirement ever to migrate instance data.** The result of this approach is that all data, for all time in all contexts can be *maintained with complete syntactic integrity and complete semantics*. The semantics for a concept modeled as a DM is represented using Semantic Web technologies. The DM identifier is the subject in each of the *Subject, Predicate, Object* RDF statements.
