"""
Defines the S3Model ontology in Python 3.7
"""

from dataclasses import dataclass

@dataclass
class CMC:
    """
    Core Model Component - A component model contained in a reference model. 
    A CMC represents a specific core type of component that further contains elements with base datatypes and other CMCs to define its structure.</s3m:description>
    """

@dataclass
class CMS:
    """
    Core Model Symbol - A CMS represents a CMC in instance data. 
    In practice, it is usually substituted for by a Replaceable Model Symbol (RMS). 
    This substitution is because constraints are expressed in a Replaceable Model Component (RMC) which is then represented by an RMS.</s3m:description>
    """
    
    