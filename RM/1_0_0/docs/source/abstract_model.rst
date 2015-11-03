====================
S3Model Abstract Model
====================

S3Model is by name as well as by definition and design a multi-level modeling approach.  This means that there are multiple models with increasing specificity to get to the instance data point. S3Model is constraint based which provides a complete syntactic validation path back to the reference model for the instance data. The semantic model is designed around the concepts of this multi-level model approach.

When answering the high-level question: *How do we elaborate the components required for a generic, implementation independent interoperability platform?* These few components were the answer.

------
S3Model2
------
Multi-Level Healthcare Information Modeling

The root concept. The abstract idea of S3Model 2.x. All of the S3Model2 classes are subclasses of this class.

--
RM
--
Reference Model

A set of components (CCMs) to provide structural integrity for a domain concept. Some CCMs are mandatory in CCDs and some are optional. Optionality is defined in each RM implementation.

------
CoreMC
------
Core Concept Model

A composable model contained in a reference model. A CoreMC represents a specific core type of component that further contains elements with base datatypes and/or other CoreMCs to define its structure.

------
CoreCS
------
Core Concept Symbol

A CoreCS represents a CoreMC in instance data. In practice, it is usually substituted for by a PluggableCS.
This substitution is due to the fact that constraints are expressed in a PluggableCM which is then represented by a PluggableCS. However the overall constraint model (CCDInstance) must match with components of the RM.

-----------
CCDInstance
-----------
Concept Constraint Definition Instance

A set of selected PluggableCMs that are constraints on the RM components (CoreMCs) in order to represent a domain concept.
In the implementation language there may be additional syntactic conventions required.

-----------
PluggableCM
-----------
Pluggable Concept Model

The name given to a CoreMC that has been constrained for use in a CCDInstance. Through the constraints, a PluggableCM defines a single concept based on syntactic data constraints as well as specified semantics. It is *pluggable* because it can be reused in multiple CCDInstances.

-----------
PluggableCS
-----------
Pluggable Concept Symbol
Represents a PluggableCM in instance data. Can be considered as a data container for the components of a PluggableCM.

------------
DataInstance
------------
A set of data items that reports via *isInstanceOf* property that it conforms to a CCDInstance. In this state it has not been tested for validation.

-----------------
DataInstanceValid
-----------------
Subclass of DataInstance.
A set of data items that conforms to a CCDInstance to represent an instance of that concept **AND** the data values are valid according to the CCD Instance constraints.

-------------------
DataInstanceInvalid
-------------------
Subclass of DataInstance.
A set of data items that conforms to a CCD Instance to represent an instance of that concept **AND** the data values are **NOT** valid according to the CCD Instance constraints. An Invalid Data Instance must contain one or more children of an Exception.

-----------------
DataInstanceError
-----------------
Subclass of DataInstance.
A set of data items that **DOES NOT** conform to the CCD Instance it represents **OR** it contains invalid data and does not contain one or more children of an Exception.

---------
Exception
---------
Indicates that some data is outside of the parameters defined by the CCD Instance.
