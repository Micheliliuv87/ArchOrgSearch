# What Is This For? 

* This is built for people who want to collect data from Archive.org
* This should help you extract the video URLs containing the keyword you are looking for download them and put them into folders differentiated by unique identifiers 
* This is easy to use for those who have experience in python

# Completeness of This Project

* V1 is completed, later version will be updated

# How this should work 

1. The ArchiveOrgSearch.py will first go and search for the word `Abortion` on Archive.org's TV section
        - The result will contain any content and mentioning of `Abortion` in the content (you can also edit the keyword you would like to search, and the creator filter)
   ```
           params = {
            "q": "abortion",
            "and[]": 'creator:"rt"'
        }
   ```
3. It will pick the last viewable creator (This is for reducing the amount of workload processed each time) 
4. It will start requesting the following features within that creator filter: 
    - Unique Identifier
    - URL = base URL + Unique Identifier (which I will process later)
    - Title
    - Creator
    - All-Time Views
    - Favorites
    - Number of Quotes
    - Script
5. Then it will store all the content it has scraped into an Excel file.


