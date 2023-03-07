import sys
sys.path.insert(1,'/home/bhaveshkilaru/cs5293sp23-project0/project0')
import main
import pytest
import sqlite3

url='https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf'

def test_fetchincidents():
    data = main.fetchincidents(url)

    assert type(data) == bytes


def test_extractincidents():

    incident_data = main.fetchincidents(url)

    incidents = main.extractincidents(incident_data)

    assert len(incidents[0]) == 5

def test_createdb():

    db = main.createdb()

    assert db == "normanpd.db"

def test_populatedb():
    
    incident_data = main.fetchincidents(url)

    incidents = main.extractincidents(incident_data)

    db = main.createdb()
    main.populatedb(db, incidents)
    con = sqlite3.connect('normanpd.db')
    cur = con.cursor()
    rows =  cur.execute("SELECT COUNT(*) FROM incidents;")
    
    for row in rows:
        result = row[0]

    assert result > 0

def test_status():
    
    assert True
