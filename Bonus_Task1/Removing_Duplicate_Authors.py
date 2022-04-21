#!/usr/bin/env python
# coding: utf-8
import pywikibot 
import datetime
import time


article_qid = 'Q58093180'
site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()


#Printing information
def add_qualifier(claim, pid, value):
    if pid not in claim.qualifiers:
        qualifier = pywikibot.Claim(repo, pid)
        qualifier.setTarget(value)
        pstr = " ".join([str(pid), get_property_label(pid)])
        claim.addQualifier(qualifier)
        print('Adding qualifier (', pstr, '): ', value)
        
        
def add_author_qualifier(item_info, claim, author_dict, qual_pid):
    for author in item_info['claims'][claim]:
        claim_qid, claim_label = get_claim_value(author.getTarget())
        if(claim == 'P2093'):
            claim_qid = claim_label
        if(claim_qid in author_dict):        
            add_qualifier(author, qual_pid, author_dict[claim_qid])
        
        
def get_property_label(claim):
    property_page = pywikibot.PropertyPage(repo, claim)
    property_dict = property_page.get()
    property_label = property_dict['labels']['en']
    return(property_label)
      
        
def print_all_qualifiers(claim):
    qualifier_i = claim.qualifiers    
    if(len(qualifier_i)):      
        print("Qualifier(s):")
        for qual_pid in qualifier_i:
            property_label = get_property_label(qual_pid)
            qualifier_value = qualifier_i.get(qual_pid)[0].target
            qid, qualifier_label = get_claim_value(qualifier_value)
            print(property_label + "(" + qual_pid + ")" + ": " + qualifier_label)    
    
                
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
    if (isinstance(claim_value, pywikibot.page._wikibase.ItemPage)):    #Open to addition
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


def print_claim_values(item_info, claim, qual_print):
    if (claim in item_info['claims']):
        claim_list = item_info['claims'][claim]
        j = 1
        for i in range(len(claim_list)):
            claim_value = claim_list[i].getTarget()
            claim_qid, claim_label = get_claim_value(claim_value)
            print(j, end = ". ")
            print(claim_qid + "  " + claim_label)
            
            if(qual_print == 1):
                print_all_qualifiers(claim_list[i])
            j += 1
    else:
        print("This claim does not exist for the given item")
        

#Printing authors
def print_article_authors(qid):
    item = pywikibot.ItemPage(repo, qid)
    item_info = item.get()
    author_qid_list = []
    author_series_dict = {}
    author_stated_dict = {}
    
    string_label_list = []
    string_series_dict = {}
    
    if ('en' in item_info['labels']): 
        #print item label
        print("Item " + "(" + qid + "): " + item_info['labels']['en']) 
    else:
        print("This item does not have an English label")
    
    if ('P2093' not in item_info['claims']):
        print("\nNo author is stored as string in this article.")
    else:
        print("\nThe authors stored as strings are: ")
        j = 1  
        for author in item_info['claims']['P2093']:
            print(j, end=". ")
            author_value = author.getTarget()
            claim_qid, claim_label = get_claim_value(author_value)
            print(claim_qid + "  " + claim_label)
            if(claim_label in string_label_list):
                print("Duplicate entry found ", claim_label)
                series_ordinal = get_qualifier(author, 'P1545')
                if(series_ordinal != 0):
                    string_series_dict[claim_label] = series_ordinal
                item.removeClaims(author)
            else:
                string_label_list.append(claim_label)
            
            #gets individual qualifiers
            print("Series Ordinal", f"{get_qualifier(author, 'P1545')}") #Series Ordinal
            j += 1
       
    
    if ('P50' not in item_info['claims']):
        print("\nNo author is stored as items in this article.")
    else:
        print("\nThe authors stored as items are: ")
        j = 1       
        
        for author in item_info['claims']['P50']:
            print(j, end=". ")
            author_value = author.getTarget()
            claim_qid, claim_label = get_claim_value(author_value)
            print(claim_qid + "  " + claim_label)
            if(claim_qid in author_qid_list):
                print("Duplicate entry found ", claim_qid)
                series_ordinal = get_qualifier(author, 'P1545')
                stated_as = get_qualifier(author, 'P1932')
                if(series_ordinal != 0):
                    author_series_dict[claim_qid] = series_ordinal
                if(stated_as != 0):
                    author_stated_dict[claim_qid] = stated_as
                item.removeClaims(author)
            else:
                author_qid_list.append(claim_qid)
            
            #gets individual qualifiers
            print("Series Ordinal", f"{get_qualifier(author, 'P1545')}")    #Series Ordinal
            print("Stated as", f"{get_qualifier(author, 'P1932')}")         #Stated as
            
            j += 1
            print("\n")
            

    print("Dictionaries with qualifiers found from duplicate values: ")
    print("Author item (series ordinal)", author_series_dict, sep="\n") 
    print("Author item (stated as)", author_stated_dict, sep="\n")
    print("Author string (series ordinal)", string_series_dict, sep="\n")
    print("Adding qualifiers if any need to be added: ")
    add_author_qualifier(item_info, 'P50', author_series_dict, 'P1545')
    add_author_qualifier(item_info, 'P50', author_stated_dict, 'P1932')
    add_author_qualifier(item_info, 'P2093', string_series_dict, 'P1545')
    

#Article item with duplicate authors
print_article_authors(article_qid)


#After the duplicates have been removed and qualifiers added
print("\nArticle after dulpicate deletion.................\n")
print_article_authors(article_qid)