=====================
S3Model Data Analysis
=====================

The real value in data and especially in *semantically computable data* is in how you can use it after it is recorded. Every implementation has different analysis requirements from static reports to dynamic dashboards and decision support. S3Model data is designed to accommodate all of these use cases.

In many cases `XQuery <https://en.wikibooks.org/wiki/XQuery>`_ is a natural choice for analyzing data. However, there is excellent support in all major programming languages for XML data and implementers may choose to develop in their favorite programming language.

The popular `R <https://cran.r-project.org/>`_ programming language is specifically designed for data analysis and supports XML data via an `XML package <https://cran.r-project.org/web/packages/XML/index.html>`_ using the commonly used `libxml2 library <https://xmlsoft.org/>`_ used by most of the other languages. Libxml2 includes complete XPath, Xpointer and Xinclude implementations. There is also a companion library called `libxslt <https://xmlsoft.org/XSLT/>`_ based on libxml2 that is used to provide support for `XML transformations <https://www.w3.org/TR/xslt>`_

A emerging open source project, `Semantic Analytics Stack <http://sansa-stack.net/>`_ (SANSA) is implementing *Algorithms for Distributed Data Processing for Large-scale RDF Knowledge Graphs*. 

Semantic Models vs. Semantic Markup
-----------------------------------
With the growing interest in *Big Data analytics*, various efforts are ongoing to improve the description of data and datasets. Data scientists across many domains are attempting to use commonly developed vocabularies, such as the `Dublin Core Metadata Initiative <https://dublincore.org/>`_ terms, the `Data Catalog Vocabulary <https://www.w3.org/TR/vocab-dcat/>`_, `Schema.org <https://schema.org/>`_ and others.

The conventional approach is to use the vocabularies to annotate the data directly. We call this the *direct markup approach*. While this approach does work, the extent is limited. There are several problems with this method. The glaringly obvious one is that, more often than not, high quality, accurate metadata is usually much larger than the actual data represented. Every instance of data and every copy of the dataset must carry all of its metadata. While storage size, memory size, processing speed and network bandwidth have improved immensely over the past decade. They are not infinite, and every byte still counts; affecting overall performance in an inverse relationship.

In conservative testing with S3Model, we can see that the syntactic and semantic metadata for a data instance is typically about three times the size of the data instance itself. So including metadata with the data means a small 16kb data file is now 64kb. This size increase is not too bad when you look at it on that scale. However, the growth is linear with this *direct markup approach*.

Let us say you record a time-series from some device and your data is 10MB. Now, for that one instance, if the data file is marked up individually, the size blooms to 40MB. Even with today's technology, this is a significant payload to transfer.

`Estimates are <https://www.storagenewsletter.com/rubriques/market-reportsresearch/ibm-cmo-study/>`_ that every day we create 2.5 quintillions (10 :sup:`18`) bytes of data.
The linear expansion that resulted in a growth of 48kb of the 16kb sized file is now a growth of **7.5 quintillion bytes**. That is **7.5 quintillion bytes** every day. 

Regardless of any sustainability estimates. Is it even a smart thing to do?
When the data instances are marked up with semantics, and they are being exchanged between systems (such as medical and other information should be), there is no single point of reference to ensure that the syntax or semantics of the information was not modified along the way.

The S3Model approach to the computable semantic interoperability problem does not have these issues. , and it is immutable. In other words, this is what the modeler intended for the data to mean at this time and in this context. The model can then be referred to by any required number of data instances. The multi-level modeling approach to development is what enables this level of efficiency in data management. S3Model uses the ubiquitous XML technology stack to accomplish this solution. Other multi-level modeling approaches may use a domain specific language that is not frequently used and does not have tools widely available for management and analysis of the models and data.

As stated earlier, the growth in the size of the data is only one issue with the direct markup approach. An additional concern is the specific file format used for distribution. In the direct markup approach, there may be differences in `semantics <https://goo.gl/oSTC1g>`_ or in the ability to even markup the data at all, using various syntaxes. In S3Model this is solved, as a result of the well known and proven approaches for transforming XML to and from other grammars. Because we are only processing the data and not the metadata, it cannot be corrupted, misrepresented or misinterpreted.

We have provided open source examples of this transformation process, specifically to and from JSON without any loss of semantics or the ability to validate the data against the schema (DM). See the `MXIC project <https://github.com/S3Model/mxic>`_ for further details.

One last comment on the issues with the *direct markup approach* is that is not robust enough for mission-critical data management; certainly not for your clinical healthcare data. This issue is widely recognized and is being addressed by `W3C <https://www.w3.org/2012/12/rdf-val/report>`_. However, we know from previous experience that the W3C process is a slow one.

In a few years, there may be widespread adoption and tools for validation of RDF syntaxes and the various levels of OWL. At that time it will be easy enough to migrate to a new version of S3Model using that approach. However, we need solutions today, and S3Model offers that solution now; with XML and RDF mix of technologies.

Support for Legacy Systems
---------------------------

S3Model is designed to provide semantic interoperability for future systems. Based on small, granular models that can be well defined. However, it is quite capable of supporting the transition of legacy data as well.  Several examples are available from the S3Model GitHub site.

A capability often overlooked is the ability to create models for CSV data to build Linked Data graphs. An often perplexing problem is how to support validation of data when that data may have come from a printed vocabulary or a terminology server. An example of this is in the TB demo where the Brazilian Death Certificate and Hospital Discharge data was modeled from CSV files. For Linked Data a vocabulary root is provided via S3Model:vocabRoot predicate and the resource is the URL to the WHO online repository. In cases where there is no online repository (such as a published PDF), and the number of enumerations would be too large to be practical as constraints, we suggest creating a URI prefix for the link to the PDF and use a # plus the values found in the data.
