=================
Executive Summary
=================

*Keep everything as simple as possible; but no simpler.* (attributed to Albert Einstein)

**S3Model** is a foundation to build a **modern data-centric** information infrastructure across all domains. This essential capability is required to advance to the modern era of performing decision support services (DSS) and Big Data analysis across information coming from multiple points. These points of data creation are increasing every day as a result of more institutions bringing new digital capabilities to more functions, in addition to the plethora of new devices arriving in the Internet of Things (IoT) marketplace.

The core purpose of S3Model is to provide a way to share context across applications either internal or external to organizations. For example, when people communicate with one another, the conversation takes place in a shared environment called "the context of the conversation." This context allows the individuals to use familiar terms, like the name of a local business or the nickname of a friend to communicate more quickly but without losing accuracy. An S3Model data model provides that context as well as constraints on data instances so that applications can automatically understand the data. 

Managing information across domains is too broad for one top-down, one-size-fits-all, slow-moving standards defined solution for information modeling and interoperability. S3Model *is built on* multiple, widely used standards.

Data is produced by people that need to record that data in a specific time and place. Often that data is useful to others at a later time and often in other domains. However, to merely transfer the raw *data* is not enough for the receiver to determine if the data meets their needs. Secondary users need to know much more about the contexts (ontological, spatial, temporal) that were applicable when the data was initially captured.

For example, if I have a leaky faucet in my home and need a washer to repair it. I go to the local hardware store to purchase a new one. The attendant there doesn't know what I need because they do not know what type of faucet I have. However, I can look at the package information and determine based on thickness, inside and outside diameters and shape (flat, conical, or round) if a particular washer fits my needs.  In this sense, S3Model is the packaging for data.  It allows the data consumer to determine if the data is useful to them as is or maybe it can even be adjusted because the consumer knows the context in which the data was captured. Of course, there are certain base standards in the plumbing industry. Just like we have datatypes (string, integer, dateTime, etc. ) and XML constructs (element, complexType, etc.). However, the overall concept is similar.

The **legacy application-centric** approach does not allow for this packaging information to be transmitted with the data. That information is locked up in, at best the source code and database table layouts and at worst in a PDF somewhere that describes cryptic SQL table column names. This non-computability prevents real decision support or artificial intelligence operations across the data from multiple sources. The human effort required to perform these reconciliation tasks are both expensive and error-prone. The data-centric approach allows you to solve these problems up front.

S3Model can be used as the original information model for new applications ranging from mobile apps to enterprise suites. S3Model is also used to enhance semantic interoperability of existing systems. We have developed tooling to strengthen existing CSV data files and for augmenting entire SQL-DB based systems. *This provides model-driven, data-centric transition capability without replacing all of your systems*.

S3Model specifically addresses the need to communicate *syntactically* sound data with the intended initial *semantics*. The more significant, point to point issues of information exchange are already handled by other formal and de-facto standards such as SOAP, REST, and others. S3Model is fully capable of utilizing systems built on those standards.

S3Model is the foundation for retrofitting your current applications to inter-operate with your future applications using the modern data-centric (as opposed to legacy application-centric) approach, without requiring wholesale replacement.

Information management *value propositions* are varied based on the needs of the industry and individual institutions. We have assembled some examples by use case :doc:`Value Propositions <./value_prop>` document.

The research and development process of S3Model is based on more than a decade of iteration and implementation. There have been multiple graduate and undergraduate degrees awarded based on the underlying R&D as well as the publication of many peer-reviewed papers. Academic project archives are at 

.. raw:: html

  <p><a href='https://www.mlhim.org/documents.html' target='_blank'>MLHIM Documentation archive.</a></p>
