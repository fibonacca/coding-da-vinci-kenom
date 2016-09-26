<?xml version="1.0" encoding="UTF-8"?>
<!--
	Felder, die uns interessieren, aus Kenom-LIDO extrahieren.
	
	Sven-S. Porst <ssp-web@earthlingsoft.net>
-->
<xsl:stylesheet
	version="1.0"
	xmlns:lido="http://www.lido-schema.org"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>

	<xsl:template match="container">
		<container>
			<xsl:apply-templates select="*"/>
		</container>
	</xsl:template>

	<xsl:template match="lido:lido">
		<record>
			<xsl:apply-templates select="@*|node()"/>
		</record>
	</xsl:template>

	<xsl:template match="lido:objectPublishedID[@lido:type='URI']">
		<uri>
			<xsl:value-of select="."/>
		</uri>
	</xsl:template>

	<xsl:template match="lido:titleSet[@lido:type='generated_kenom']">
		<title>
			<xsl:value-of select="lido:appellationValue"/>
		</title>
	</xsl:template>

	<xsl:template match="lido:objectWorkType/lido:conceptID[contains(text(), 'http://d-nb.info/gnd/')]">
		<xsl:variable name="gnd-id" select="substring-after(text(), 'http://d-nb.info/gnd/')"/>
		<type>
			<xsl:choose>
				<xsl:when test="$gnd-id = '4040629-5'">Münze</xsl:when>
				<xsl:when test="$gnd-id = '4038206-0'">Medaille</xsl:when>
				<xsl:when test="$gnd-id = '4004469-5'">Banknote</xsl:when>
				<xsl:when test="$gnd-id = '4126078-8'">Münzfund</xsl:when>
				<xsl:otherwise>???</xsl:otherwise>
			</xsl:choose>
		</type>
	</xsl:template>

	<xsl:template match="lido:event[lido:eventType/lido:conceptID/text() = 'http://terminology.lido-schema.org/lido00007']">
		<earliestDate>
			<xsl:value-of select=".//lido:earliestDate"/>
		</earliestDate>
		<latestDate>
			<xsl:value-of select=".//lido:latestDate"/>
		</latestDate>
		<xsl:apply-templates select="*"/>
	</xsl:template>

	<xsl:template match="lido:termMaterialsTech[@lido:type='material']">
		<material>
			<xsl:value-of select="lido:term"/>
		</material>
	</xsl:template>

	<xsl:template match="lido:termMaterialsTech[@lido:type='technique']">
		<technique>
			<xsl:value-of select="lido:term"/>
		</technique>
	</xsl:template>

	<xsl:template match="lido:measurementsSet[lido:measurementType/text() = 'diameter']">
		<diameter>
			<xsl:attribute name="unit"><xsl:value-of select="lido:measurementUnit"/></xsl:attribute>
			<xsl:value-of select="lido:measurementValue"/>
		</diameter>
	</xsl:template>

	<xsl:template match="lido:measurementsSet[lido:measurementType/text() = 'weight']">
		<weight>
			<xsl:attribute name="unit"><xsl:value-of select="lido:measurementUnit"/></xsl:attribute>
			<xsl:value-of select="lido:measurementValue"/>
		</weight>
	</xsl:template>

	<xsl:template match="lido:measurementsSet[lido:measurementType/text() = 'orientation']">
		<orientation>
			<xsl:attribute name="unit"><xsl:value-of select="lido:measurementUnit"/></xsl:attribute>
			<xsl:value-of select="lido:measurementValue"/>
		</orientation>
	</xsl:template>
	
	<xsl:template match="lido:eventPlace/lido:place[lido:placeID[@lido:type = 'URI']]">
		<location>
			<xsl:attribute name="name">
				<xsl:value-of select="lido:namePlaceSet/lido:appellationValue"/>
			</xsl:attribute>
			<xsl:attribute name="type">
				<xsl:value-of select="@lido:politicalEntity | @lido:geographicalEntity"/>
			</xsl:attribute>
			<xsl:value-of select="lido:placeID[@lido:type = 'URI']"/>
		</location>
	</xsl:template>
	
	<xsl:template match="lido:resourceSet[lido:resourcePerspective/lido:term/text() = 'front']">
		<image-front-path>
			<xsl:attribute name="copyright">
				<xsl:value-of select="lido:rightsResource[.//lido:term/text() = 'copyright']//lido:appellationValue"/>
			</xsl:attribute>
			<xsl:value-of select=".//lido:resourceID[@lido:type = 'local']"/>
		</image-front-path>
	</xsl:template>
	
	<xsl:template match="lido:resourceSet[lido:resourcePerspective/lido:term/text() = 'back']">
		<image-back-path>
			<xsl:attribute name="copyright">
				<xsl:value-of select="lido:rightsResource[.//lido:term/text() = 'copyright']//lido:appellationValue"/>
			</xsl:attribute>
			<xsl:value-of select=".//lido:resourceID[@lido:type = 'local']"/>
		</image-back-path>
	</xsl:template>
	
	<xsl:template match="@*|node()">
		<xsl:apply-templates select="@*|node()"/>
	</xsl:template>

</xsl:stylesheet>