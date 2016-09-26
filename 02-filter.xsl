<?xml version="1.0" encoding="UTF-8"?>
<!--
	Nur Münzen behalten.
	
	Sven-S. Porst <ssp-web@earthlingsoft.net>
-->
<xsl:stylesheet
	version="1.0"
	xmlns:lido="http://www.lido-schema.org"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>

	<xsl:template match="container">
		<container>
			<xsl:apply-templates select="@*|node()"/>
		</container>
	</xsl:template>

	<xsl:template match="record">
		<xsl:if test="type/text() = 'Münze'">
			<xsl:copy-of select="."/>
		</xsl:if>
	</xsl:template>
	
	<xsl:template match="@*|node()">
		<xsl:apply-templates select="@*|node()"/>
	</xsl:template>

</xsl:stylesheet>