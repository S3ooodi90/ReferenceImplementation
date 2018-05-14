==============
Abstract Model
==============

S3Model is by name as well as by definition and design a constraint-based multi-level modeling approach.  This approach means that there are multiple models with increasing specificity to get to the instance data point. S3Model is constraint-based which provides a complete syntactic validation path back to the reference model for the instance data. The semantic model is designed using the concepts of this multi-level model approach. Extensions to the reference model concepts are not allowed.

When answering the high-level question: *How do we elaborate the components required for a generic, implementation independent interoperability platform?* These few components were the answer.

-------
S3Model
-------
(Shareable, Structured, Semantic Model)
---------------------------------------

The root concept. The is the source of the abstract concept of S3Model. All of the S3Model classes are related to this class through partOf.

--
RM
--
(Reference Model)
-----------------

A set of components called Core Concept Models (CMCs) that provide structural integrity for a domain concept. Some CMCs are mandatory in DMs, and some are optional. Optionality is defined in each versioned, RM implementation.

---
CMC
---
(Core Model Component)
----------------------

Core Model Component 
A component model contained in a reference model. A CMC represents a specific core type of component that further contains elements with base datatypes and other CMCs to define its structure.

---
CMS
---
(Core Model Symbol)
-------------------

A CMS represents a CMC in instance data. In practice, it is usually substituted for by a Replaceable Model Symbol (RMS). This substitution is because constraints are expressed in a Replaceable Model Component (RMC) which is then represented by an RMS.

--
DM
--
(Data Model)
------------

A set of selected RMCs that are constraints on the RM components (CMCs) to represent a domain concept. In the implementation language, there may be additional syntactic conventions required. Caution: Not to be confused with Data Instance.

---
RMC
---
(Reusable Model Component)
--------------------------

The name RMC is given to a CMC that has been constrained for use in a DM. Through the constraints, an RMC defines a single concept based on syntactic data constraints as well as specified semantics. It is reusable because it can be reused in multiple DMs.

---
RMS
---
(Reusable Model Symbol)
-----------------------

The RMS represents an RMC in instance data. Can be considered as a data container for the components of an RMC. All of the RMSs are contained in a DataInstance when in transit.

------------
DataInstance
------------
A set of data items that report via the isInstanceOf property that it conforms to a DM. In this state, it has not been tested for validation.

-----------------
DataInstanceValid
-----------------
Subclass of DataInstance. A set of data items that conforms to a DM to represent an instance of that concept AND the all of the data values are valid according to the DM constraints.

-------------------
DataInstanceInvalid
-------------------
Subclass of DataInstance. A set of data items that conforms to a DM to represent an instance of that concept AND at least some of the data values are NOT valid according to the DM constraints. An Invalid Data Instance must contain one or more children of an Exception.

-----------------
DataInstanceError
-----------------
Subclass of DataInstance. A set of data items that DOES NOT conform to the DM it represents, OR it contains invalid data and does not contain one or more children of an Exception. If there are no noted Exceptions in the Data Instance, then it should be considered suspect and discarded.

---------
Exception
---------
Exceptions indicate that a data instance may be invalid when validated against its model. However, the exceptional value may be explainable and provide valuable contextual information. A specific Exception subclass instance included in the data instance will provide that additional information. `here <owl/index.html>`_ 

