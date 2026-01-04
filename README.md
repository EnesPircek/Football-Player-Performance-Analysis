Football Player Performance Analysis Dashboard



This project is a data-driven dashboard designed to analyze and compare football player performances across different periods (Pre-Pandemic vs. Post-Pandemic) and league tiers. It uses SQL for data management and Streamlit for an interactive user interface.



 Features

Global Filters: Filter data by period (Pre/Post Pandemic), league tiers (Elite, Competitive, Cup/Lower), and minimum minutes played.

KPI Analysis: Interactive visualizations for Total Contributions, Efficiency, and Discipline Scores.

Top 10 Rankings:Dynamic leaderboards based on selected performance metrics.

Player Search: Detailed individual statistics and evolution over time.



Tech Stack

Python (Pandas, Matplotlib, Seaborn)

Streamlit (Web Interface)

SQLite (Database Management)



Project Structure

app.py : The main Streamlit application script.

football_data.db : SQLite database containing processed football statistics.

Python_and_SQL_Project.ipynb : Jupyter notebook showing the data cleaning and transformation process.

Requirements.txt : List of necessary Python libraries.

.gitignore : Configured to exclude large raw datasets (like `appearances.csv`).



Installation Usage

Clone the repository:

&nbsp;  ```bash

&nbsp;  git clone \[https://github.com/EnesPircek/Football-Player-Performance-Analysis.git](https://github.com/EnesPircek/Football-Player-Performance-Analysis.git)


Install dependencies:
   pip install -r Requirements.txt

Run the dashboard:
    streamlit run app.py

Data Source:

The analysis is based on a comprehensive football dataset. Due to file size limits on GitHub, the raw appearances.csv file is excluded, but all processed data is available in the provided SQLite database.
