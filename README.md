# What Is This For? 

* This is built for people who want to collect data from Archive.org
* 
* This is easy to use for those who have experience in python

# Completeness of This Project

* Still in the development stage (Will likely finish in one or two weeks) 

# How this should work 

1. The ArchiveOrgSearch.py will first go and search for the word "Abortion" on Archive.org's TV section
        - The result will contain any content and mentioning of "Abortion" in the content 
2. Then it will first pick the last viewable creator (This is for reducing the amount of workload processed each time) 
3. Then it will start requesting the following features : 
    - Unique Identifier
    - URL = base URL + Unique Identifier (which I will process later)
    - Title
    - Creator
    - All-Time Views
    - Favorites
    - Number of Quotes
    - Script
4. Then it will store all the content it has scraped into an Excel file.

# Result 

Saved 6339 entries
ok

----------------------------------------------------------------------
Ran 1 test in 1423.164s

# Updates on 01/23 

