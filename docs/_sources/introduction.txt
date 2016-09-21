============
Introduction
============

History
-------

The Shareable, Structured, Semantic Model (S3Model) specifications are based on years of research and development in healthcare IT. 

Only the reference model is implemented in software where desired. In many implementations, the application will use XML Tools to validate against the Data Model schema and Reference Model schema. Then persist the data using any SQL, NoSQL or other persistent storage. For devices or other small apps even the file system will suffice as a storage solution. The key here is that the DM defines the structure and semantics for that data packet when exchanged with others. This is the *promise* that the initial data capture provides to secondary users.

The domain knowledge models are implemented in the XML Schema language and they represent constraints on the reference model implementation, also implemented in XML Schema.
The domain knowledge models are called Data Models and the acronyms DM and DMs are used throughout S3Model documents to mean these XML Schema files. This means that, since DMs form a model that allows the creation of data instances from and according to a specific DM, it is ensured that the data instances will be valid, in perpetuity. DMs are immutable. This insures data validity for longitudinal records and the data is never migrated to a new DM.

However, any data instance should be able to be imported into any S3Model based application since the root data model, for any application is the S3Model reference model. But, the full semantics of that data will not be known unless and until the defining DM is available to the receiving application. The DM represents the structural syntax of a concept [#f1]_ using XML Schema constraints and contains the semantics defined by the modeler in the form of RDF/XML or other XML based syntaxes within documentation and annotation segments of the DM. This enables applications to parse the DM and publish or compute using the semantics as needed on an application by application basis.

**The S3Model approach allows systems developers to build the data model they need for their application and the shared DMs tell you how and what was captured. This sharable information model allows any other data consumer to determine if the data is correct for their needs.**

The above paragraph describes the foundation of *computable semantic interoperability* in S3Model implementations. You must understand this and the implications it carries to be successful with implementing and creating systems with the full value of S3Model based applications. See the :doc:`Modeling Concepts <./modeling_concepts>` document for further discussion of Data Models (DMs).

A secret weapon of S3Model is that many times there are individual data points that appear is a number of concepts. There is often a need to analyze these together indepenedent of which larger concept it was included inside. The S3Model approach fully supports this level of granularity with the same precision as for complete documents.



.. rubric:: Footnotes

.. [#f1] In healthcare concepts include: (a) clinical concepts adopted in medicine for diagnostic and therapeutic decision making; (b) analogous concepts used for all healthcare professionals (e.g. nursing, dentistry, psychology, pharmacy); (c) public health concepts (e.g. epidemiology, social medicine, biostatistics); (d) demographic and (e) administrative concepts that concern healthcare. In other domains concepts are similar in that they embody one idea that needs to be expressed in a data exchange. 
