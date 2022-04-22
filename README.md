# Outreachy_Wikidata2022
This repository contains codes and outputs of Task 2 for the project: What's in a name? Automatically identifying first and last author names for Wikicite and Wikidata.

# Task_2
In this task, I implemented the following:
* Loaded the page created in Task 1 and displayed its text
* Added 'Hello' to the aforementioned page
* Loaded Wikidata Sandbox (Q4115189) and printed its information including all the qualifiers 
* Loaded articles from Task 1 and printed its author information
* Bonus: Automatically followed links to authors stored as items and printed their given name and last name

# Task_3
In this task, I implemented the following:
* Extracted author information using RegEx from citation, in BibTex format, from a url
* Processed the extracted information accordingly as LaTex encoding of accented characters needs to be processed before displaying
* Also processed non-breaking spaces and replaced them with regular spaces. Note: I could have simply achieved the same with unidecode but that resulted in changing accented characters (ü) into closest ASCII characters (u), which was undesirable
* Printed the author names and compared the ones in the Wikidata item to the ones in citation (BibTex format. This section also satisfies the first part of Task 3 - loading the article item and printing the author information from it (with the qualifiers: {{P|P1545}} for authors as strings and {{P|P1545}} and {{P|P1932}} for authors as items). 
* Added {{P|P9687}} and {{P|P9688}} to all the authors with the help of citation, as well as added {{P|P1932}} to authors stored as items if not found (did this directly as ADS had the same name in citation as the original publication)

# Bonus_Task1
* Removed duplicate entries of authors (stored as items and strings)
* Stored qualifiers from duplicate entries and added them in the only instance of that author item or author string remaining
  ## Discussion
  * This code works well for multiple cases that I have tried. It does take into account that the duplicate instance is added with the same value
  * Further extension of this bonus task can be to check if an author is stored as both item and string and removing duplicates accordingly
  * Another extension can be to add authors as items which have been added as strings. This will require cross-checking if there is an author item by the same name or    'Also known as'. The next step would be to search through their publications (maybe using ORCID) to find the title of the Wikidata article and confirm that they are indeed the author of this particular scientific article


