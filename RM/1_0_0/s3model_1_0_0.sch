<schema xmlns="http://purl.oclc.org/dsdl/schematron" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" queryBinding="xslt2">

  <ns uri="http://www.w3.org/2001/XMLSchema" prefix="xs"/>
  <ns uri="http://www.s3model.com/rm" prefix="s3m"/>

  <xsl:include href="./s3model_1_0_0.xsl"/>

  <pattern>
    <rule context="xs:complexType/xs:complexContent/xs:restriction[@base = $DerivedAssertList/@type]">
      <assert test="s3m:CheckAssertion(.)">
        <value-of select="s3m:Message(.)"/>
      </assert>
    </rule>
  </pattern>

</schema>
