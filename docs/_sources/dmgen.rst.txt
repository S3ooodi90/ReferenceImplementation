=================================================
Data Model Generator (DM-Gen)
=================================================
The `DM-Gen <https://www.DMgen.com>`_ is not part of the specifications. However, since it is a primary tool for authoring DMs we include this chapter.

Registration & Access
---------------------
The DM-Gen does require free registration to gain access to be able to view and download current DMs. Note that DMs are also available on `GitHub <https://github.com/S3Model/DMlib>`_.

Access to authoring your own PCMs & DMs requires posting a request in the S3Model Google+ Community. See the Support page for links.


Creating and Managing DMs
--------------------------
The DM-Gen is an online tool used to create DMs via a web driven, declarative environment. The DM-Gen allows the building of complete DMs by selecting the desired Pluggable complexType (PCM) definitions from existing PCMs or ones that you design yourself. You assemble the pieces into the concept definition you need. By re-using PCMs you improve the data exchange and analysis capability.

Many of the PCMs have been designed based on existing data models. Resources such as the `Common Data Element <https://cdebrowser.nci.nih.gov/CDEBrowser/>`_ definitions from the US National Cancer Institute, the United States Health Information Knowledgebase (USHIK), from the Agency for Healthcare Research and Quality (AHRQ) and many others. Some `HL7 FHIR® <https://www.hl7.org/fhir/>`_ models have been translated to PCMs. More are planned and you can contribute to the open content effort. The `Siscolo <https://goo.gl/mSHk47>`_ application has been modeled and `example <https://github.com/S3Model/TB-Data-in-eXist-db>`_ of translating a controlled vocabulary using ICD-10 in an XML-DB is on GitHub.

The DM is an XML Schema that is compliant with the W3C XML Schema 1.1 standards. It is valid against one S3Model Reference Model release. However, many of the PCMs maybe used in DMs across various reference model releases. A DM provides an approach to improve the process of allowing semantic interoperability between various applications. This process is enabled due the ability to *exchange the syntax and semantics for data models designed by domain experts.*

The DM-Gen has a library of some of the DMs created using this tool. Because of the governance approach to DMs there is no need for a centralized repository. It is helpful though to have some place for potential users to review published examples. The DM-Gen Library page displays the DMs in a table and an included XSLT renders the details directly from the DM (click on the Title link) in a familiar data dictionary format. This is an example of how applications can extract this information from the DM for user help pages and tooltips and even decision support.

DMs created by the DM-Gen are also commited to a `GitHub repository <https://github.com/S3Model/DMlib>`_ Each reference model version has a separate branch in the repository. See the `README <https://github.com/S3Model/DMlib/blob/master/README.md>`_ for instructions on searching the DM Library on GitHub.

XML Data Instances
------------------
The DM-Gen creates one sample XML instance along with every DM. These samples are valid instances of the DM schema. The one exception is when an xs:assert is used in a PCM definition. The instance generator cannot *always* create guaranteed valid data content for any arbitrary assert statement. If your sample is not valid, this is likely the case and it can be edited using any XML editor. For regular expressions (regexes) used to describe a string pattern in a Xdstring-value element, the DM-Gen can handle most patterns. Strings like postal codes, phone numbers, etc. should be randomly created okay. Other PCMs have no facility for xs:assert matching.

JSON Data Instances
-------------------
The DM-Gen executes an XML to JSON conversion to create the example JSON data instance. The namespace entries are treated as data so that they are maintained for conversion back to XML.

HTML Forms
----------
There are hundreds of possibilities for uses of data when defining a model. Any given application component may write to multiple DM instances at any one time. There is no a priori solution for this.

The DM-Gen takes the most generic approach and creates a HTML form that depicts the nested nature of data defined by this DM. This automatically generated form is more appropriately useful as a communications tool between the knowledge modeler (domain expert) and the software developer. It allows the developer to visually see the structure of the data.
This form also includes helpful information for the developer to relate the visual content to the DM and data instance.

There is a tooltip on every structure name (Cluster, XdString, etc.) that provides the UUID for that structure. A HTTP link is also provided here that connects the developer to the specific documentation on the S3Model website concerning the parent complexType of the Reference Model.

The textual semantics for each component is also presented. A tooltip on these names/titles provided by the modeler displays the documentation as well as all links/semantic references that the modeler included in the PCM. This provides the developer with the same context that the modeler used when defining the PCM.

R Code
------
In conjunction with each DM, the DM-Gen creates source code for use with the R statistical programming environment [#f1]_. Specifically the code is created in a project suitable for use in R Studio[#f2]_, a package development and management tool for R.

The R code is package complete and compliant for distribution via the The Comprehensive R Archive Network[#f3]_ . You can use R Studio or the R tools for package creation to generate the desired package format, either source or compiled binary for a specific platform (Linux, Mac, Windows, etc.). The code written by the DM-Gen also contains package documentation (R help files) that can be created using the tools mentioned above.

The R code is created on a PCM level and will return a dataframe from all matching instances of a PCM. For example you may search across a complete repository of XML instances and receive a dataframe containing all occurrences of a specific PCM in all DMs. Users should note however that the generated R code will only return the first instance in a given file.

For more practical use, the code modules can be edited and combined into an application specific library and used to build any desired data structure based on the content of your repository. For example you may want to provide an additional loop or apply function to gather cases where multiple instances appear within a given XdAdapter node.
**Customizing these basic routines allows the analyst to apply any of the thousands of algorithms available as R packages to their S3Model based data repository.**

Users and developers should note that the metadata.R file is not included in the NAMESPACES that are exported. However, it is required for every other R file since there are functions for XML namespace resolution located there. This file must be specifically 'sourced'. You may optionally include it in your NAMESPACE file.


.. rubric:: Footnotes

.. [#f1] https://www.r-project.org/
.. [#f2] https://www.rstudio.com/
.. [#f3] https://cran.r-project.org/
