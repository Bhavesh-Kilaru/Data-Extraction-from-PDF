## CS5293 Spring 2023 Project 0

Web Scrapping Incident data
===

This project is intended to fulfil the course requirement for Text Analytics (CS5293) of The University of Oklahoma.

Author : Bhavesh Kilaru

Email  : bhavesh.kilaru@ou.edu

#About

This project intends to extract pdf data from web, extract various fields, creating a database, populating the database and printing the count of each nature.

# Required Packages
The below mentioned are the required list of packages for this project:

- argparse
- PyPDF
- re
- sqlite3
- tempfile
- urllib

# structure of the project

```
├── COLLABORATORS
├── Pipfile
├── Pipfile.lock
├── README.md
├── normanpd.db
├── project0
│   └── main.py
├── requirements.txt
├── setup.cfg
├── setup.py
└── tests
    └── test_main.py
```

# Python functions created

fetchincidents() - This function accepts an URL as an input parameter, process the pdf and returns a bytes file as an output.

		   call statement :- incident_data = fetchincidents(url)

extractincidents() - This function accepts a bytes file as an input, process the bytes file, extract the data for each of the column and returns a list of list containing five values representing each of the five columns

		   call statement :- incidents = extractincidents(incident_data)

createdb() - This function does not have an input parameter and creates a table named "incidents" in "normanpd.db". It returns the database as the output.

		   call statement :- db = createdb()

populatedb() - This function accepts two input parameters the "Database" and a list. It populates the table "incidents" and insert the records into it.

		   call statement :- populatedb(db, incidents)

status() - This function accepts the database as an input parameter and print the count of each nature.
	
		   call statement :- status(db)

# Execution of the program.

To exeute the program from the console,	execute the following command in console
<br />pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf

# Execution of test case
Execute the following command in the console
<br /> pipenv run python -m pytest



