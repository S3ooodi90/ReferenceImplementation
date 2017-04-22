======================
The S3Model Eco-System
======================

It is important here to describe all of the components of the S3Model conceptual eco-system in order for the reader to appreciate the scope of S3Model and the importance of the governance policies.

The Core
--------

At the base of the S3Model eco-system is the Reference Model (RM). Though the reference implementation is in XML Schema format, in real world applications a chosen object oriented language will likely be used for implementations. Often, tools are available to automatically generate the reference model classes from the XML Schema. This is the basis for larger S3Model compliant applications. We will later cover implementation options for smaller applications such as mHealth (apps for smartphones and tablets, as well as purpose specific devices such as a home blood pressure monitor).

The next level of the S3Model hierarchy is the Data Model (DM). The DM is a set of constraints against the RM that *narrow* the valid data options to a point where they can represent a specific healthcare concept. The DM is essentially an XML Schema that uses the RM complex types as base types. This is conceptually equivalent to inheritance in object oriented applications, represented in XML Schema.

Key to Interoperability
-----------------------

Since a DM (by definition) *can only narrow the constraints* of the RM, then any data instance that is compliant with a DM is also compliant in any software application that implements the RM or is designed to validate against the RM. Even if the DM is not available, an application can know how to display and even analyze certain information. For example, if a receiving application does not have a DM for a given data instance it will be able to discern the DM ID and RM version from the element name and attributes of the root element. It may or may not be able to retrieve the DM from the xsi:schemaLocation attribute. If not, it will still be able to infer, based on the reference model version, information about the data by using the names of elements nested within an element with the prefix 'pcs-'. Because these element names are unique to certain RM complexTypes. If there is a <Xdcount-value> element then that data is from a XdCountType and *name* is in the preceding <label>.

Model Publication
-----------------

We are not implying that all DMs must be publicly available. It is possible to maintain a set of DMs within a certain political jurisdiction or within a certain professional sector or in a company. How and where these DMs are maintained are outside the scope of these specifications. Developers proficient in XML technologies will understand how this fits into their application environment and how to use XML Catalogs to reference any local copy.

Bottom Up vs. Top Down
----------------------

This is now the point where the S3Model eco-system is in contrast to the top-down approach used by other multi-level modeling specifications and the Standards Development Organization (SDO) approach.

*In the real world*; we know that there can never be complete consensus across the healthcare spectrum of domains, cultures and languages; concerning the details of a specific concept. Therefore the concept of a *maximal data model*, though idealistically valid, is realistically unattainable. Several years of participation in and observation of these attempts to build consensus has led to the development of the `Cavalini-Cook Theory <https://github.com/S3Model/specs/wiki/Cavalini-Cook-Conjecture-&-Theory>`_ - **The probability of reaching consensus among biomedical experts tends to zero with the increase of the number of concepts considered and the number of experts included in the consensus panel.**

In S3Model, participants at any level are encouraged to create domain knowledge models that *fit their needs*. The RM has very little semantic context in it to get in the way. This allows structures to be created as the modeler sees fit for purpose. The Cluster complexType allows for any data structure [#f1]_ to be built to match implementation needs. There is no inherent idea of a specific application such as an Electronic Health Record (EHR), Electronic Medical Record (EMR), etc. in the RM although the S3Model specifications can also be adopted for the development of these types of applications. This approach provides an opportunity for development of small, purpose specific apps such as mobile or portable device software as well.

How Many DMs?
--------------
In S3Model, the bottom-up approach makes room for dozens, hundreds or even thousands of DMs to describe each healthcare concept, (e.g. blood pressure, body temperature, problem list, medication list, Glasgow Coma Scale, cost of a medical procedure, or any other healthcare phenomena) vs. the top-down approach that requires a single, flat model implemented in software that must encompass all descriptions/uses/etc. This multiplicity of compatible domain knowledge models is achieved by the way DMs are uniquely identified by a Version 4 Universal Unique Identifier (UUID) prefixed with the string, 'DM-'.

DMs are assembled out of pluggable concept models (PCMs) so that modelers can use granular definitions to create any size application model or models, as needed. Modelers and developers can create systems that allow users to choose between a selection of DMs to include at specific points, at run-time. Reuse of existing PCMs in multiple DMs and reusing DMs across multiple applications makes data sharing and analysis easier. However, given that the semantics are in the DM, data consumers can decide if the data fits their needs or how to include certain components (PCM based data) from multiple DMs.

Over time, **the cream will rise to the top** and the most useful DMs will be used most often.

With S3Model DMs you can deliver your data with complete syntactic interoperability and as much semantic interoperability and information exchange as the modeler chose to include in the DM.
The governance of DMs is left to the modeler and/or publishing organization.

**There are very strict guidelines that define what constitutes a valid DM, as seen above.**

A Valid DM Must:
-----------------
* Be a valid XML Schema 1.1 schema as determined by widely available parser/validators such as `Xerces <http://xerces.apache.org/xerces2-j/faq-xs.html#faq-2>`_ or `Saxon <http://www.saxonica.com/documentation/schema-processing/>`_
* Consist of complexTypes that only use the *restriction* element of complexTypes with a *base* attribute from the associated reference model
* use Type 4 UUIDs for complexType names, with the prefix of, 'pcm-'. Example [#f2]_ ::

    <xs:complexType name='pcm-8c177dbd-c25e-4908-bffa-cdcb5c0e38e6' xml:lang='en-US'>

* publish a global element for each complexType where a substitutionGroup is required [#f3]_. The element **MUST** be defined using the same UUID as the complexType with the 'pcm-' prefix replaced with 'pcs-'.
* Include the reference model schema from www.S3Model.org using the appropriately defined namespace. Example for release 2.5.0 and later releases, S3Model uses the namespace http://www.S3Model.org/ns/S3Model/ with the standard prefix of S3Model [#f4]_ ::

  <xs:element name='pcs-8c177dbd-c25e-4908-bffa-cdcb5c0e3888' substitutionGroup='S3Model:XdAdapter-value' type='S3Model:pcm-8c177dbd-c25e-4908-bffa-cdcb5c0e3888'/>

* use the correct substitution group(s) as in the example above
* define the required namespaces used in the DM as in Figure 1.
* define the minimum `DCMI <http://dublincore.org/>`_ metadata items as shown in Figure 2.

.. image:: dm_header.png

Figure 1.

.. image:: dm_metadata.png

Figure 2.

A Valid DM Must Not:
---------------------
* Contain any other language processing instructions required for validating instance data. For example; Schematron rules. While Schematron can be very valuable in some processing environments it is considered implementation specific and not part of the S3Model interoperability framework.
* Import or include any XML Schema document other than its parent reference model schema.


DM Functionality
-----------------

---------
Structure
---------
A DM is just an XML Schema. It uses the xs:include element to reference the RM schema from the S3Model website. For performance a local copy should be used via an `XML Catalog <https://www.oasis-open.org/standards#xmlcatalogsv1.1>`_
The design of DMs allows us to separate the structure from the domain semantics of a complexType. This is key in having a small RM that represents structural components that provide a well defined data query platform which is essential for analytics and decision support.

Prior to XML Schema 1.1, other languages (such as `Schematron <http://www.schematron.com/>`_ ) were *needed* to provide for complex validation scenarios. The `xs:assert element <http://www.w3.org/TR/xmlschema11-1/#cAssertions>`_ now takes care of those issues. This in addition to gaining additional data model types and the ability to use multiple substitutionGroups is why we specify XML Schema 1.1 as a requirement for DMs.

Schematron may still be useful for defining business rules in your implementation. But these definitions are implementation specific and do not apply to the S3Model semantic interoperability goals. Experience shows that these implementation details *leaked* into the data structure definition creates a barrier to interoperability.

The use of UUIDs has been controversial and is a perceived barrier by some people. In reality though they are what allows S3Model to be such a simple, yet powerful solution. This is how we separate the structure and domain semantics. By using UUIDs for the complexType and element names we build a structure that has only *structural semantics*. As an example take a look at `HL7 <http://www.hl7.org/>`_ CDA or FHIR schemas or `NIEM <https://www.niem.gov>`_ schemas. Notice how they mix domain semantics into the names of complexTypes and elements. This creates a nasty chain of optional domain elements because you cannot know a priori what is going to be needed where.  There is an attempt to use attributes to provide some uniqueness to types of entries. But this has grow out of control to a point where those schemas are very complex. NIEM attempted to solve the problem by using a multi-level model approach.  But then *specified* that domain element names **MUST** be terms from the Oxford English Dictionary. So that limits its usefulness to 5.4% of the global population.  To be fair, NIEM is designed and named to be used in the US.  But that is a bit of a short-sighted development approach considering the global world we live in today.

In designing S3Model we had the aXdantage of being able to analyze HL7 v3.x, openEHR, ISO 13606 and other interoperability attempts and use these as lessons learned points. NIEM was started about the same time as S3Model.

We realized that this mix of structure and domain semantics was a key problem in the complexity of the models. In openEHR the focus is specifically about EHR systems but it introduced multi-level modeling as a constraint based approach. S3Model takes the constraint based, multi-level  approach along with the data package view. We say data package because you may view a data instance as a message or as a document *or* as a component of a message or a document. A *S3Model data instance* is just that. They can be very small or very large and they can be combined into documents or messages or standalone; depending upon the implementation needs. This is part of the *multi-level paradigm*.

The need for multiple substitutionGroups arises because, one PCM may be reused in multiple places in a DM. For example a XdLinkType based PCM may be reused as a link in an EntryType as well as used in a ClusterType based PCM.  In this case the since *element* of type *complexType* must be defined as substituting for the RM elements *XdLink* and *XdAdapter-value* elements from the RM.  Example::

      <xs:element name='pcs-a05e8d88-a6dc-43d5-b1b8-723cdc9bf680' substitutionGroup="S3Model:XdLink S3Model:XdAdapter-value" type='S3Model:pcm-a05e8d88-a6dc-43d5-b1b8-723cdc9bf680'/>



---------
Semantics
---------
With the reusability and structural simplicity out of the way we can now discuss the issue of **what does the data mean?**

**NOTE: This section is in active transition from RDF Semantics to OWL2 DL using the RL Profile.**

If you are not familiar with RDF you may want to read more at `LinkedDataTools <http://www.linkeddatatools.com/>`_ or directly from the `W3C Specifications <http://www.w3.org/TR/rdf11-primer/>`_.

The world of data exchange is composed of two primary players; *data providers* and *data consumers*. Whether those two parties are people or software applications they require this knowledge to turn *data* into useful *information*. We discussed approaches to transferring this information in the **Semantic Models vs. Semantic Markup** section of *Modeling Concepts*.

Adding the semantics to the model allows all of the meaning of the data to be in one known location. Each data instance has a pointer to its parent DM. Example::

    xsi:schemaLocation='http://www.S3Model.org/ns/S3Model/ http://www.DMgen.com/DMlib/DM-00605c3e-cd14-492e-9891-6ad3ad26230e.xsd'>

this example from a data instance says that the schema in the namespace *http://www.S3Model.org/ns/S3Model/* is located on the DM-Gen and is named *DM-00605c3e-cd14-492e-9891-6ad3ad26230e.xsd*. Typically DMs are located locally and an XML Catalog is used to resolve these locations.

The first part of the semantics describes the model itself. This is accomplished using the DCMI metadata elements. See the example above in Figure 2.

Taking a *simplistic* example DM (the sequence of appearance of the complexTypes is not important) we can see a PCM with a XdLinkType restriction::

    <xs:complexType name='pcm-a05e8d88-a6dc-43d5-b1b8-723cdc9bf680' xml:lang='en-US'>
    <xs:annotation>
      <xs:documentation>
        This is a test XdLink used for an example.
      </xs:documentation>
      <xs:appinfo>
        <rdf:Description rdf:about='S3Model:pcm-a05e8d88-a6dc-43d5-b1b8-723cdc9bf680'>
          <rdfs:subClassOf rdf:resource='&S3Model;XdLinkType'/>
          <rdfs:isDefinedBy rdf:resource='http://www.S3Model.org/generic_PCMs'/>
          <rdfs:label>Test XdLink</rdfs:label>
        </rdf:Description>
      </xs:appinfo>
    </xs:annotation>
    <xs:complexContent>
      <xs:restriction base='S3Model:XdLinkType'>
        <xs:sequence>
          <xs:element maxOccurs='1' minOccurs='1' name='label' type='xs:string' fixed="Test XdLink"/>

        ...
    </xs:complexType>

Notice that inside the xs:annotation there are two child elements; xs:documentation and xs:appinfo.  The xs:documentation element has a free text, human readable description of the purpose of the PCM. The xs:annotation element has a child element rdf:Description this element has an rdf:about attribute with a value of the namespace and the complexType name. This forms the *Subject* component of the RDF statements to follow.

The first child of rdf:Description is a rdfs:subClassOf element. This element name is the *Predicate* component of the first RDF statement. This element has an attribute of rdf:resource and a URI of S3Model:XdLinkType which forms the *Object* component of this RDF statement.

The second child of rdf:Description is a rdfs:isDefinedBy element. This element name is the *Predicate* component of the second RDF statement about the PCM. The rdf:resource attribute
points to a resource on the S3Model website. `Give it a try <http://www.S3Model.org/generic_PCMs>`_. It is just a simple plain text document used as a resource for these examples. Note that it is not a requirement that all URI resources be resolvable URLs. But we think it is a good idea that they are whenever possible.

The third child of rdf:Description is a rdfs:label This element defines a fixed text label to this PCM. So the *Predicate* is rdfs:label and the *Object* is the string "Test XdLink".

So now we have three statements about the unique subject called *S3Model:pcm-a05e8d88-a6dc-43d5-b1b8-723cdc9bf680*. We know it is a subtype of the S3Model XdLinkType that is defined in the S3Model Reference Model schema that is included (via xs:include) in this DM. We can also find a definition of this PCM in the resource at http://www.S3Model.org/generic_PCMs.

So now we have some machine processable semantics as well as some documentation. All available from the model. Also note that there is the *label* element. When a modeler defines a PCM they give it a fixed name as a human readable string. This is included in the data instance and even though the XML element is a UUID, this readable text is immediately below it and describes what the modeler defined for the name. The rdfs:label and the label **SHOULD** be the same string.

Example from the instance data::

    <S3Model:pcs-c05e8d88-a6dc-43d5-b1b8-723cdc9bf680>
      <label>Test XdLink</label>
      ...
    </S3Model:pcs-c05e8d88-a6dc-43d5-b1b8-723cdc9bf680>

The next section describes how all of this can be used in an operational setting.

--------------------
S3Model in Operation
--------------------
We have a Reference Model, a Data Model and some data instances; all in XML. How does all of that fit together, especially since I use JSON with my REST Services and Turtle for my RDF semantics syntax?

Glad you asked ....

Remember that the XML and RDF/XML syntaxes are used because they are robust. They are the canonical definitions for the models and the data because the tools are available for validating the syntax and the semantics.

Because S3Model XML data has a *very specific structure* it is quite easy to perform lossless conversion to and from JSON. So you can send and receive JSON data. The points in your data chain that need require validated data can be converted back to XML for validation.

So (a snippet) like this::

            <S3Model:pcs-d4079097-c68b-4c99-9a5e-b85628d55897>
          <!-- Party -->
          <party-name>A. Sample Name</party-name>
          <!-- PI external-ref -->
          <S3Model:pcs-ab51a8c0-ba5c-4053-8201-ae29c1a534bb>
            <!-- XdURI -->
            <label>External Reference for Party</label>
            <!-- Use any subtype of ExceptionalValue here when a value is missing-->
            <valid-time-begin>2006-04-15T04:18:21Z</valid-time-begin>
            <valid-time-end>1981-12-10T19:35:00Z</valid-time-end>
            <XdURI-Xd>http://www.DMgen.com</XdURI-Xd>
            <relation>Party Associated with the record</relation>
          </S3Model:pcs-ab51a8c0-ba5c-4053-8201-ae29c1a534bb>

can be converted to::

              },
          "S3Model:pcs-d4079097-c68b-4c99-9a5e-b85628d55897": {
            "party-name": "A. Sample Name",
            "S3Model:pcs-ab51a8c0-ba5c-4053-8201-ae29c1a534bb": {
              "label": "External Reference for Party",
              "valid-time-begin": "2006-04-15T04:18:21Z",
              "valid-time-end": "1981-12-10T19:35:00Z",
              "XdURI-Xd": "http://www.DMgen.com",
              "relation": "Party Associated with the record"
            },

and back again. All depending upon the needs of your information flow.


Two of the S3Model projects on GitHub demonstrate combining the model semantics with the data instances to create a Graph and storing it in a Triple Store. The connections can then be visualized using open source tools and / or queried using SPARQL.

For deeper details on using S3Model in various scenarios you should refer to the `GitHub repository <https://github.com/S3Model>`_ specifically `this project <https://github.com/S3Model/S3Model_semantics_extractor>`_ as well as the `MXIC demo <https://github.com/S3Model/mxic>`_ and the `MAPLE demo <https://github.com/S3Model/MAPLE>`_ These all use older versions of S3Model but the concepts are the same for any 2.x version.

Two projects that may be of particular interest is `adding semantics to FHIR models <https://github.com/S3Model/ichi2015_fhir_semantics>`_ and `adding semantics to HL7v2 messages <https://github.com/S3Model/hl7v2_semantics>`_



.. rubric:: Footnotes

.. [#f1] Used here to mean; trees, lists, tables, etc.
.. [#f2] The language attribute is optional.
.. [#f3] Substitution groups are required where the base type allows multiple elements and where the base type allows an abstract element.
.. [#f4] Some previous releases had a specific namespace for the RM and each DM. This was changed to a single namespace for all of S3Model 2.x versions to improve query and processing interoperability.
