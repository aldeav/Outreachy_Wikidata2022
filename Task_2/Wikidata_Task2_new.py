#!/usr/bin/env python
# coding: utf-8
import pywikibot 
import datetime
import time


#Printing text of User:Akandoria/Outreachy 1
site = pywikibot.Site('wikidata', 'wikidata')
repo = site.data_repository()
page_outreachy = pywikibot.Page(repo, 'User:Akandoria/Outreachy 1') 
page_text = page_outreachy.text
print(page_text)


#Adding hello at the end of the page
def edit_article(page):
    text = page.get()
    text = "\n".join([page.get(), "Hello"])
    page.text = text
    try:
        page.save()
    except:
        print("Page was not saved")
        
edit_article(page_outreachy)


#Printing information
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
    
                
def print_qualifier(claim, qual_pid):
    property_label = get_property_label(qual_pid)
    try: 
        qualifier_i = claim.qualifiers
        qualifier_value = qualifier_i.get(qual_pid)[0].target
        qid, qualifier_label = get_claim_value(qualifier_value)
        print(property_label + "(" + qual_pid + ") " + ": " + qualifier_label)
    except:
        print(property_label + " not found")
        
        
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
        

def print_information(qid, qual_print):    
    #qual_print = 1 to print all the qualifiers on itempage    
    item = pywikibot.ItemPage(repo, qid)
    item_info = item.get()
    
    if ('en' in item_info['labels']): 
        #print item label
        print("Item " + "(" + qid + "): " + item_info['labels']['en']) 
    else:
        print("This item does not have an English label")
        
    for claim in item_info['claims']:
        property_label = get_property_label(claim)
        print("Property (" + claim + ") : \'"+ property_label + "\'")
        print_claim_values(item_info, claim, qual_print)
        print("\n")
        

#Printing authors 
def print_article_authors(qid):
    item = pywikibot.ItemPage(repo, qid)
    item_info = item.get()
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
            
            #gets individual qualifiers
            print_qualifier(author, 'P1545')    #Series Ordinal
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
            
            #gets individual qualifiers
            print_qualifier(author, 'P1545')    #Series Ordinal
            print_qualifier(author, 'P1932')    #Stated as
            
            #Follows author item page and prints first and last name
            print("\nFollowing the link to this author item: ")
            author_item = pywikibot.ItemPage(repo, claim_qid)
            author_info = author_item.get()
            print("Given Name: ")
            print_claim_values(author_info, 'P735', qual_print = 1)
            print("Family Name: ")
            print_claim_values(author_info, 'P734', qual_print = 1)
            
            j += 1
            print("\n")
                


#qual_print = 1 prints all the qualifiers
print("\nInformation of sandbox - ")
print_information('Q4115189', qual_print = 1)


#Loading first 4 articles and printing author information
scientific_articles = ['Q58093180', 'Q60718800', 'Q68818818', 'Q55967148']
print("Author information of articles -")
for article in scientific_articles:
    print_article_authors(article)
