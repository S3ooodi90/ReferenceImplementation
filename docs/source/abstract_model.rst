======================
S3Model Abstract Model
======================

S3Model is by name as well as by definition and design a constraint based multi-level modeling approach.  This means that there are multiple models with increasing specificity to get to the instance data point. S3Model is constraint based which provides a complete syntactic validation path back to the reference model for the instance data. The semantic model is designed around the concepts of this multi-level model approach. Extensions to the reference model concepts are not allowed.

When answering the high-level question: *How do we elaborate the components required for a generic, implementation independent interoperability platform?* These few components were the answer.

-------
S3Model
-------
Shareable, Structured, Semantic Model (S3Model)

The root concept. The abstract idea of S3Model. All of the S3Model classes are subclasses of this class.

--
RM
--
Reference Model

A set of components called *Core Concept Models* (CCMs) that provide structural integrity for a domain concept. Some CCMs are mandatory in DMs and some are optional. Optionality is defined in each RM implementation.

---
CCM
---
Core Concept Model

A composable model contained in a reference model. A CCM represents a specific core type of component that further contains elements with base datatypes and/or other CCMs to define its structure.

---
CCS
---
Core Concept Symbol

A CCS represents a CCM in instance data. In practice, it is usually substituted for by a Pluggable Concept Symbol (PCS).
This substitution is due to the fact that constraints are expressed in a Pluggable Concept Model (PCM) which is then represented by a PCS. 

---
DMI
---
Data Model Instance

A set of selected PCMs that are constraints on the RM components (CCMs) in order to represent a domain concept.
In the implementation language there may be additional syntactic conventions required. *Caution:* Not to be confused with Data Instance.

---
PCM
---
Pluggable Concept Model

The name given to a CCM that has been constrained for use in a DMI. Through the constraints, a PCM defines a single concept based on syntactic data constraints as well as specified semantics. It is *pluggable* because it can be reused in multiple DMIs.

---
PCS
---
Pluggable Concept Symbol
Represents a PCM in instance data. Can be considered as a data container for the components of a PCM.

------------
DataInstance
------------
A set of data items that reports via *isInstanceOf* property that it conforms to a DMI. In this state it has not been tested for validation.

-----------------
DataInstanceValid
-----------------
Subclass of DataInstance.
A set of data items that conforms to a DMI to represent an instance of that concept **AND** the all of the data values are valid according to the DMI constraints.

-------------------
DataInstanceInvalid
-------------------
Subclass of DataInstance.
A set of data items that conforms to a DMI to represent an instance of that concept **AND** at least some of the data values are **NOT** valid according to the DMI constraints. An Invalid Data Instance must contain one or more children of an Exception. 

-----------------
DataInstanceError
-----------------
Subclass of DataInstance.
A set of data items that **DOES NOT** conform to the DMI it represents **OR** it contains invalid data and does not contain one or more children of an Exception. If there are no noted Exceptions in the Data Instance then it should be considered suspect and discarded.

---------
Exception
---------
Indicates that some data is outside of the parameters defined by the DMI and provides some context as to the cause of the anomaly. 
