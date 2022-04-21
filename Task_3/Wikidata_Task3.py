#!/usr/bin/env python
# coding: utf-8
import pywikibot
import urllib.request
import re
from bs4 import BeautifulSoup
from pylatexenc.latex2text import LatexNodes2Text


article_qid = 'Q55967148'
site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()


#Getting citation
with urllib.request.urlopen('https://ui.adsabs.harvard.edu/abs/2014MNRAS.439.3225L/exportcitation') as response:
    html = response.read()

soup = BeautifulSoup(html, from_encoding = "utf-8")


#Extracting authors using RegEx
authors = re.search(r'author = {(.*?)\.},', str(soup))


#Extracting author first name
#LatexNodes2Text() to get the accented characters
#Not using unidecode as it changes ö to o
#replacing nbsp with a regular space
author_f = [a+b for a,b in re.findall(r'}, (.*?) and|}, (.*?)},', authors.group())]
author_first = [LatexNodes2Text().latex_to_text(x).replace('\xa0', ' ') for x in author_f]


#Extracting author last name
author_l = re.findall(r'{(.*?)},', authors.group(1))
author_last = [LatexNodes2Text().latex_to_text(x).replace('\xa0', ' ') for x in author_l]


def get_property_label(claim):
    property_page = pywikibot.PropertyPage(repo, claim)
    property_dict = property_page.get()
    property_label = property_dict['labels']['en']
    return(property_label)
      

def get_qualifier(claim, qual_pid):
    property_label = get_property_label(qual_pid)
    try:  
        qualifier_i = claim.qualifiers
        qualifier_value = qualifier_i.get(qual_pid)[0].target
        qid, qualifier_label = get_claim_value(qualifier_value)
        return(qualifier_label)
    except:
        return(0)
        
        
def get_claim_value(claim_value):
    claim_qid = ""
    if(isinstance(claim_value, pywikibot.page._wikibase.ItemPage)):
        #Changed it from try to if since just working with ItemPage
        claim_dict = claim_value.get()
        claim_qid = claim_value.title()
        claim_label = claim_dict['labels']['en']
    else:
        #Added conditions for few datatypes
        #Open to adding more conditions
        if (isinstance(claim_value, pywikibot.WbQuantity)):
            claim_qid = "Value:"
            claim_label = str(claim_value.amount);
        elif (isinstance(claim_value, pywikibot.WbTime)):
            if(claim_value.month and claim_value.day != 0):
                claim_label = str(datetime.date
                (claim_value.year, claim_value.month, claim_value.day))
            else:
                claim_label = str(claim_value.year)
        else:
            claim_label = str(claim_value)

    return(claim_qid, claim_label)


def add_qualifier(claim, pid, value):
    if pid not in claim.qualifiers:
        qualifier = pywikibot.Claim(repo, pid)
        qualifier.setTarget(value)
        pstr = " ".join([str(pid), get_property_label(pid)])
        claim.addQualifier(qualifier, summary='Adding qualifier: ' + pstr)
        print('Adding qualifier (', pstr, '): ', value)
            

def print_article_authors(qid):
    i = 0
    item = pywikibot.ItemPage(repo, qid)
    item_info = item.get()
    if 'en' in item_info['labels']:
        print("Article: ", "(", qid, ")", item_info['labels']['en'])
    else:
        print("This article does not have an English label")        
    
    authors_wiki = []    
    if ('P2093' not in item_info['claims']):
        pass
    else:
        authors_wiki += item_info['claims']['P2093']
        
    if ('P50' not in item_info['claims']):
        pass
    else:
        authors_wiki += item_info['claims']['P50']
        
    for author in authors_wiki:
            
        author_value = author.getTarget()
        claim_qid, claim_label = get_claim_value(author_value)
        qualifier_label1 = get_qualifier(author, 'P1545')    #Series Ordinal
        qualifier_label2 = get_qualifier(author, 'P1932')    #Stated as
            
        bibtex_first = author_first[int(qualifier_label1) - 1]
        bibtex_last = author_last[int(qualifier_label1) - 1]
        bibtex_author = bibtex_first + " " + bibtex_last
        
        print("Series Ordinal: ", qualifier_label1)
        print("Name in Citation: ", bibtex_author)
        if (claim_qid == ""):
            print("Name in Wikidata (Author String): ", claim_label)
        else:
            print("Name in Wikidata (Author item):", claim_qid, claim_label, sep=" ")
            print("Wikidata Stated as (P1932): ", qualifier_label2)        
        
        add_qualifier(author, 'P9687', bibtex_first)
        add_qualifier(author, 'P9688', bibtex_last)
        if(claim_qid != ""):
            add_qualifier(author, 'P1932', bibtex_author)
        print("\n")


#Printing author names from Citation (BibTex) and Wikidata
print_article_authors(article_qid)

