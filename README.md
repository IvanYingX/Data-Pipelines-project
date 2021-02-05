# Data-Pipelines-project

First project in the AI-Core course. These scripts extract data from different sources to get results and important (or not so important) features that will be used as inputs for a classification ML model
The 

## How to use the repo

There are two main scripts in this repo. The first is Main.py, which opens a GUI to ask you whether you want to create or update a database. \n
The second one is Update_Database.py which gets the data in the Data folder and looks for any update in the data. \n
The reason for having two separate scripts is for being able to:
* Create and update the database manually, so that one can add new leagues to the database
* Automatically update the database by setting a cron job on the cloud (or locally if that is available) by running periodically the Update_Database.py file

Additionally, there is a Create_Database.py file that performs the first webscraping and stores the data in the Raw_Data folder, which then will be updated, cleaned, and filled with other features.

## Content

_The packages should not be modified, since there are many dependencies between them and the main scripts_
_The only files that are recommended to be modified are the get\_leagues.py and get\_year.py, which set the possible leagues and years, but if the user wants to increase that range, he/she can broaden it by adding more leagues and/or years_

Apart from the two main files (Main.py and Update_Database.py), there are two more python scripts in the main folder of this repo:

* Create_Database.py: It is explained above
* Test.py: A playground for testing the functions

The folders in the repo contains:

### Data

* Dictionaries: This folder contains information about the matches and the teams, in both pickle files (which when unpickle are dictionaries) and csv. This folder will eventually store the weather data
* Raw Data: This folder contains the data that is extracted when creating a database for the first time.
	* Results: Each CSV contains the results of the matches from an initial year to a final year of a specific league
	* Standings: Each CSV contains the standings of the matches from an initial year to a final year of a specific league
* Updated: This folder contains the same CSVs as in Raw Data but updated, so everything is up to date (updated every day at 3:00 AM)

### Extract:

The chromedriver.exe is in this folder. Additionally we can see the following files:
* Extract_Data: This file contains the necessary functions to create a database for the first time
* Get_Match_Info: This file loads a results dataset, and extracts the information of each of the matches in that dataset
* Get_Team_Info: This file loads a standings dataset, and extracts the information of each team and its stadium
* Get_Weather_Info: This file loads the results and standings datasets, and extracts the weather for each match considering the city the match took place in.

### Initial_Gui

When executing Main.py, the GUI that pops up is determined by the files in this folder:
* confirm.py: Creates a tk object summarising the selected information by the user to know if it should procceed
* create_update: Creates a tk object that ask the user whether he/she wants to create or update the database
* get_file_update: Creates a tk object that ask the user if he/she wants to update a file or a whole directory, and also includes a class (Update_Gui) that creates a tk object that ask the user to select the files or directories to be updated
* get_leagues: Creates a tk object with checkboxes to ask the user what leagues he/she wants to include in the creation of a database
* get_years: Creates a tk object with a slider to ask the user the initial year and the final year for creating a database within those years.

#TODO
* Finish the extraction of weather
* Write some DOCSTRINGS and comments on the code