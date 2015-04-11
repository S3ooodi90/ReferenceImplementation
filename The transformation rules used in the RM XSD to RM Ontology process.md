The transformation rules that are used in the RM XSD to RDF/OWL:

* xs:simpleType with xs:enumeration   An owl:Class is defined and instances are created for every enumerated value. 

* xs:complexType over xs:complexContent   owl:Class

* xs:element (global) with complex type   owl:Class and subclass of the class generated from the referenced complex type

* xs:element (local to a type)    owl:DatatypeProperty for XSD types and owl:ObjectProperty for RM complexTypes. OWL Restrictions are built for the occurrence.

* Substitution Groups     Subclass statements are generated for the members.


