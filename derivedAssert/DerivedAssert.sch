<schema xmlns="http://purl.oclc.org/dsdl/schematron" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" queryBinding="xslt2">

  <ns uri="http://www.w3.org/2001/XMLSchema" prefix="xs"/>
  <ns uri="derivedAssert" prefix="da"/>

  <xsl:include href="DerivedAssert.xsl"/>

  <pattern>
    <rule context="xs:complexType/xs:complexContent/xs:restriction[@base = $DerivedAssertList/@type]">
      <assert test="da:CheckAssertion(.)">
        <value-of select="da:Message(.)"/>
      </assert>
    </rule>
  </pattern>

</schema>
