#!/usr/bin env python
"""
As the script name implies, generate the Media Format Ontology (mfo)
from the MusicBrainz NGS tables.

Note to get mfo URIs we replace space " " with "_" and urlencode

@author kurtjx
@date Thu Oct  7 17:38:07 CDT 2010
"""

# settings hard coded
DBNAME = 'musicbrainz_db'
USER = 'kurtjx'
PASS = 'kurtjx'

import psycopg2
from urllib import quote

prefixes = '''@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix mo: <http://purl.org/ontology/mo/> .
@prefix mfo: <http://purl.org/ontology/mfo/> .

<http://purl.org/ontology/mfo/> a owl:Ontology ;
    dct:title "The Media Format Ontology";
    owl:versionInfo "Revision 0.01";
    dct:description """
        The Media Format Ontology is a small extension to the Music Ontology
        that provides a series of concepts relate to media formats derived
        from the MusicBrainz database.
    """ ;
    foaf:maker <http://kurtisrandom.com/foaf.rdf#kurtjx> ;
    owl:imports <http://purl.org/ontology/mo/> .

mo:Medium
    a owl:Class;
    rdfs:label "Medium";
    rdfs:comment "A means or instrumentality for storing or communicating musical manifestation.";
    rdfs:isDefinedBy <http://purl.org/ontology/mo/> .

'''
ttl_template = '''
mfo:%s a owl:Class;
    rdfs:label "%s" ;
    rdfs:subClassOf mo:Medium .
    '''
ttl_template_year = '''
mfo:%s a owl:Class;
    rdfs:label "%s" ;
    rdfs:subClassOf mo:Medium ;
    dct:created "%s"^^xsd:gYear .
    '''

def main():
    c = psycopg2.connect(database=DBNAME, user=USER,password=PASS).cursor()
    c.execute('select name, year from musicbrainz.medium_format')

    turtle = prefixes
    for row in c.fetchall():
        name, year = row
        uri = quote(name.replace(' ','_'))
        if year != None:
            turtle += ttl_template_year % (uri, name, year)
        else:
            turtle += ttl_template % (uri, name)
            
    f = open('mfo.ttl', 'w')
    f.write(turtle)
    f.close()
    c.close()
    

if __name__ == '__main__':
    main()
