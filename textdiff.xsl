<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:d="http://docbook.org/ns/docbook"
    exclude-result-prefixes="xs d"
    version="2.0">
    <xsl:template match="d:article">
        <xsl:copy>
            <xsl:apply-templates/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match="@* | node()">
        <xsl:apply-templates select="@* | node()"/>
    </xsl:template>
    <xsl:template match="d:section">
        <xsl:copy>
            <xsl:attribute name="title" select="d:title"/>
            <xsl:value-of select="descendant::*[not(self::d:section or self::d:title)]"/>
        </xsl:copy>
        <xsl:apply-templates/>
    </xsl:template>
    
</xsl:stylesheet>