<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:saxon="http://saxon.sf.net/" xmlns:da="derivedAssert" exclude-result-prefixes="#all" version="2.0">


  <xsl:variable name="DerivedAssertList" as="element()*">
    <xsl:apply-templates select="/" mode="DerivedAssertList"/>
  </xsl:variable>

  <xsl:template match="element() | document-node()" mode="DerivedAssertList">
    <xsl:apply-templates select="*" mode="#current"/>
  </xsl:template>

  <xsl:template match="xs:complexType/xs:annotation/xs:appinfo/DerivedAssert" mode="DerivedAssertList">
    <xsl:copy>
      <xsl:attribute name="type" select="parent::*/parent::*/parent::*/@name"/>
      <xsl:copy-of select="@test, @message"/>
    </xsl:copy>
  </xsl:template>

  <xsl:function name="da:CheckAssertion" as="xs:boolean">
    <xsl:param name="Restriction" as="element(xs:restriction)"/>
    <xsl:variable name="DerivedAssert" as="element()?" select="$DerivedAssertList[$Restriction/@base = @type]"/>
    <xsl:choose>
      <xsl:when test="exists($DerivedAssert)">
        <xsl:for-each select="$Restriction">
          <!-- set context -->
          <xsl:sequence select="xs:boolean(saxon:evaluate($DerivedAssert/@test))"/>
        </xsl:for-each>
      </xsl:when>
      <xsl:otherwise>
        <xsl:sequence select="true()"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:function>

  <xsl:function name="da:Message" as="xs:string">
    <xsl:param name="Restriction" as="element(xs:restriction)"/>
    <xsl:variable name="DerivedAssert" as="element()?" select="$DerivedAssertList[$Restriction/@base = @type]"/>
    <xsl:sequence select="$DerivedAssert/@message"/>
  </xsl:function>

</xsl:transform>
