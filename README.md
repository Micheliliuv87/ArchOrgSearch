# What Is This For? 

* This is built for people who want to collect data from Archive.org
  
* This is easy to use for those who have experience in python

* This is helpful to avoid being banned and triggering robot detection

# Completeness of This Project

* Still in the development stage (adding more complete features)

# How this should work 

1. ArchiveOrgSearch.py 

   1.1 **It will first go and search for the word "Abortion" on Archive.org's TV section.**
     - This file will scrape the meta data including:
       - Name of the media, URL for video, Number of views, Number of Likes, Number of quotes, and script shown on their main page.  
     - There is a parameter setting that allows users to focus on which channel to get the data from. You can edit the following (line:34): 
    ```
    creators = ["wncn", "wkrc"] # can update this list based on preferences 
    ```
    1.2 **This data will be stored in a folder in your working directory named `"meta_data"`.**

2. Download_Processor.py

    2.1 **It will revisit the previos data saved in the `"meta-data"` folder created from ArchiveOrgSearch.py and start copying every URL to start download**

    2.2 **Since ArchiveOrg only allows 60s per video(likely for most videos) it is specialyl taken care of in the code**

# Updates on 05/26

1. Made a bat file so you can run the two things as an application by one click.
2. Make sure that you put all three files in the same folder so it can locate the correct address.
3. Please let me know what you would like to update.
