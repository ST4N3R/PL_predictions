# EPL predictor

The project aims to predict the outcomes of all matches in a given season of the English Premier League, ultimately determining the likely season winner. The collected data comes from https://fbref.com/en/ and was gathered using Python's Requests and BeautifulSoup. The data was then cleaned with Spark, and all data is stored on Azure Blob Storage. The project's results are WIP (work in progress).







## Table of contents

- [Web scrapping](#Web-scrapping)
- [Data cleaning](#Data-cleaning)
- [EDA](#EDA)
- [Model building](#Model-building)
- [Productionization](#Productionization)



## Web scrapping

Using Python, the project retrieves the final league table, match results, and future match schedule from the 1995-1996 season up to the current one. It is divided into two scripts—one for retrieving match results and schedule, and another for the league table. The first script gathers the following data:

- Wk - the match week
- Day - day of the week
- Date - exact date
- Time - time the match was played
- Home - name of the home team
- xG_Home - xG value for the home team
- Score - final match score
- xG_Away - xG value for the away team
- Away - name of the away team
- Attendance - number of spectators attending live
- Venue - stadium where the match was played
- Referee - name of the referee
- Match Report - link to detailed match data
- Notes - comments from the website authors

This data splits into two files, one with results for past matches and second with the fixtures for current season. The second script collects league table data. It's splitting data into two files, one with final league table for previous seasons and second with current league table. Those table contains the following columns:

- Rk - position in the league table
- Squad - club name
- MP - number of matches played
- W - number of wins
- D - number of draws
- L - number of losses
- GF - goals scored
- GA - goals conceded
- GD - goal difference
- Pts - points earned
- Pts/MP - points per match
- xG - total xG from each match played
- xGA - total xG of opponents from each match played
- xGD - difference between xG and xGA
- xGD/90 - difference between xG and xGA per 90 minutes
- Last 5 - results of the last five matches
- Attendance - average attendance
- Top Team Scorer - player with the most goals
- Goalkeeper - team’s goalkeeper
- Notes - comments from the website authors

The retrieved data is saved in the folder [epl_predictions/data/raw](https://github.com/ST4N3R/PL_predictions/tree/main/epl_predictions%2Fdata%2Fraw)


## Data cleaning

During data cleaning, only one column was removed, namely Notes (applies to both tables). Additionally, the following columns were created:

- Match_result - information about result of the match. W - home team win, D - draw, L - away team win. This column is going to be predicted by the model.
- Home_points_last_5_matches - the sum of points earned by home team in last five matches
- Away_points_last_5_matches - the sum of points earned by away team in last five matches


I’m still working on this part. I would like to add the following columns and functionalities:

- New column with result of the previous match between two clubs
- Stworzyć nowe dane, które będą ligową tabelą po każdej rezegranej kolejce. Dzięki temu będę mógł uwzględnić te dane podczas trenowania modelu
- Currently column "Home_points_last_5_matches" contains sum of points, but I want to check if this format "WWWWW" (for five wins) will be better
- I still need to arrange data in table that will be easy to use by the model
- Connect, to Azure, so I can import data there
## EDA

I want to predict result of each match, so this will focus on creating insights about "Match_result" column. I want to see how each column impact result of the match.

Work in progress
## Model building

The model's task is to predict each match in a given week. Then, the script will update the league table with the new results. These data will be used to make further predictions, which will update the table again. This process will repeat until the results of all matches have been predicted.

Work in progress
## Productionization

Work in progress