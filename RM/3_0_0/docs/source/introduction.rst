============
Introduction
============

History
-------

The Multi-Level Health Information Modeling (S3Model) specifications are partially derived from various `ISO <http://www.iso.org/iso/home.html>`_ Healthcare Information Standards (See the 'Compliance Section') and the `openEHR <http://www.openehr.org/>`_ 1.0.2 specifications and the intent is that S3Model 1.x be technologically inter-operable with openEHR.

See the :doc:`Governance<./governance>` document for more information on the history of S3Model.

The 1.x *attempts* are available on `Launchpad <http://launchpad.net/S3Model-specs>`_ if anyone is interested in reviving the effort.

Current Versions
----------------

S3Model 2.x (this document and related artifacts) introduces **further innovation and a departure from previous approaches** that haven't worked, through the use of XML technologies and reducing complexity without sacrificing interoperability as well as improved modeling tools and as application development platforms. These specifications can be implemented in any structured language.
While a certain level of knowledge is assumed, the primary goal of these specifications is to make them 'implementable' by the widest possible number of people. The primary motivator for these specifications is the complexity involved in the recording of the temporal-spatial-ontological relationships in healthcare information while maintaining the original semantics across all applications; for all time.

We :doc:`invite <./support>` you to join us in this effort to maintain the specifications and build great, translatable healthcare tools and applications for global use.
International input is encouraged in order for the S3Model specifications to allow for true interoperability, available to everyone in all languages.

Actual implementation in languages other than XML Schema and related XML technologies, the packages/classes should be implemented per the standard language naming format. A Language Implementation Specification (LIS) should be created for each language. For example S3Model-Python-LIS.rst for the Python language or S3Model-Java-LIS.rst for the Java language. Add the LIS to the docs directory of the current development version and submit a pull request.

S3Model intentionally does not specify full behavior within a class. Only the data and constraints are specified. Behavior may differ between various applications and should not be specified at the information model level. The goal is to provide a system that can capture and share the semantics and structure of information in the context in which it is captured, not define specific application behaviors.

The generic class names in the specification documents are in CamelCase type. since this is most typical of implementation usage.

Only the reference model is implemented in software where needed. In many implementations, the application can use XML Tools to validate against the CCD and reference model using any SQL, NoSQL or other persistent storage. For devices or other small apps even the file system will suffice as a storage solution.

The domain knowledge models are implemented in the XML Schema language and they represent constraints on the reference model implementation that is also implemented in XML Schema.
The domain knowledge models are called Concept Constraint Definitions and the acronyms CCD and CCDs are used throughout S3Model documents to mean these XML Schema files. This means that, since CCDs form a model that allows the creation of data instances from and according to a specific CCD, it is ensured that the data instances will be valid, in perpetuity. CCDs are immutable. This insures data validity for longitudinal records.

However, any data instance should be able to be imported into any S3Model based application since the root data model, for any application is the S3Model reference model. But, the full semantics of that data will not be known unless and until the defining CCD is available to the receiving application. The CCD represents the structural syntax of a healthcare [#f1]_ concept using XML Schema constraints and contains the semantics defined by the modeler in the form of RDF/XML or other XML based syntaxes within documentation and annotation segments of the CCD. This enables applications to parse the CCD and publish or compute using the semantics as needed on an application by application basis.

**The S3Model approach allows systems developers to build the data model they need for their application and the shared CCDs tell you how and what was captured, not what to capture.
This sharable information model allows any other data consumer to determine if the data is correct for their needs.**

The above paragraph describes the foundation of *computable semantic interoperability* in S3Model implementations. You must understand this and the implications it carries to be successful with implementing and creating the full value of S3Model based applications. See the :doc:`Modeling Concepts <./modeling_concepts>` document for further discussion of Concept Constraint Definitions (CCDs).

.. rubric:: Footnotes

.. [#f1] Healthcare concepts include: (a) clinical concepts adopted in medicine for diagnostic and therapeutic decision making; (b) analogous concepts used for all healthcare professionals (e.g. nursing, dentistry, psychology, pharmacy); (c) public health concepts (e.g. epidemiology, social medicine, biostatistics); (d) demographic and (e) administrative concepts that concern healthcare
