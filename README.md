# Football Results Database

This repo extracts data of football leagues from europe over the last 30 years. The main idea is to use these data as inputs for a classification ML model or for a NN classifier. Even though the initial script is meant to extract data from some leagues, the list of leagues can be changed by going to the *get_leagues.py* script and add the desired league as well aS its corresponding name in the https://www.besoccer.com/ webpage

## Content

There are two main scripts in this repo. The first is Main.py, which opens a GUI to ask you whether you want to create or update a database. <br>
The second one is Update_Database.py which gets the data in the Data folder and looks for any update in the data. <br>
The reason for having two separate scripts is for being able to:

* Create and update the database manually, so that one can add new leagues to the database
* Automatically update the database by setting a cron job on the cloud (or locally if that is available) by running periodically the Update_Database.py file

Additionally, there is a Create_Database.py file that performs the first webscraping and stores the data in the Raw_Data folder, which then will be updated, cleaned, and filled with other features.

Apart from the two main files (Main.py and Update_Database.py), there are two more python scripts in the main folder of this repo:

* Create_Database.py: It is explained above
* Test.py: A playground for testing the functions

The folders in the repo contains:

### Data

* Dictionaries: This folder contains information about the matches and the teams, in both pickle files (which when unpickle are dictionaries) and csv. This folder will eventually store the weather data
* Results: Each folder contains the results of the matches of a specific league from an initial year to a final year
* Results_Cleaned: It has the same format as Results, but the data has been treated with the Clean_Data.py script shown below


### Extract

The chromedriver.exe is in this folder. Additionally we can see the following files:

* Clean_Data: Cleans the results of the leagues folder and store the cleaned data into Results_Cleaned
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

## How to use this repo

_The packages should not be modified, since there are many dependencies between them and the main scripts_
_The only files that are recommended to be modified are the get\_leagues.py and get\_year.py, which set the possible leagues and years, but if the user wants to increase that range, he/she can broaden it by adding more leagues and/or years_

When running Main.py, a GUI asking whether to create or update the database will pop up:

![Main_GUI](https://user-images.githubusercontent.com/58112372/114110031-db06a080-98d6-11eb-8044-6081bf201c95.png)

### Create

This option uses the Create_Database.py script to create a new database. The arguments of that function are the leagues and years to extract the data from, so three new windows will appear asking for the leagues:

![Leagues](https://user-images.githubusercontent.com/58112372/114110098-fec9e680-98d6-11eb-92b3-d52fbb64306f.png)

Then, the code will ask for an initial year:

![Initial_Year](https://user-images.githubusercontent.com/58112372/114110104-06898b00-98d7-11eb-9422-0b12525d8281.png)

And finally, the last window will ask for a final year:

![Final_Year](https://user-images.githubusercontent.com/58112372/114110122-130de380-98d7-11eb-8c82-4d201d7c9daa.png)

Before creating the new dataset, a final window will show the summary of our query to be sure of our input

![Summary](https://user-images.githubusercontent.com/58112372/114110147-1c974b80-98d7-11eb-8dbb-8fae4ef4407d.png)

_If the database of the specified years and league already exists, it will be overwritten_

### Update

When updating the database, we can choose between updating a single year of a league, a whole league, or the whole dataset:

![Year_League_Dataset](https://user-images.githubusercontent.com/58112372/114110170-2ae56780-98d7-11eb-9864-ec96a9374a4c.png)

Then, the user is asked to choose a file or a directory depending on whether he/she chose to update a year, or a league or the dataset respectively:

![Choose_File](https://user-images.githubusercontent.com/58112372/114110190-38025680-98d7-11eb-9218-51962d407ea2.png)

# Final Notes

I will try to update this repo consistently until I get as much features as I can. One example of a desired feature is a numeric score of each player, but that can take a great amount of time...<br>
If you have any question or suggestion, please, let me know by DMing me
