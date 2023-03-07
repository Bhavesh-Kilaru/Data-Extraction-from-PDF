import urllib.request
import tempfile
import pypdf
from pypdf import PdfReader, PdfFileReader
import re
import sqlite3
import argparse


def main(url):
    # Download data
    incident_data = fetchincidents(url)

    # Extract data
    incidents = extractincidents(incident_data)

    # Create new database
    db = createdb()

    # Insert data
    populatedb(db, incidents)

    # Print incident counts
    status(db)


def fetchincidents(url):

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    try:
        data = urllib.request.urlopen(
            urllib.request.Request(
                url, headers=headers)).read()

        return data

    except BaseException:

        print("issue in reading data")


def extractincidents(incident_data):
    temp = tempfile.TemporaryFile()
    try:
        temp.write(incident_data)
        temp.seek(0)
        reader = PdfReader(temp)
        num_pages = len(reader.pages)
        incidents = []

        for i in range(num_pages):

            page = reader.pages[i].extract_text()
            if i == 0:
                page = re.split(r'NORMAN POLICE', page)[0]
                cleaned_page = page.split("\n")[1:]
            else:
                if i == num_pages - 1:
                    page = re.split(r'1/2/2023', page)[0].rstrip()
                cleaned_page = page.split("\n")

            for line in cleaned_page:
                split = re.split('\\s+', line)

                if len(split) < 4:
                    split = incidents[-1] + split
                    incidents = incidents[:-1]

                Date_Time = split[0] + " " + split[1]
                Incident_number = split[2]
                Inc_Ori = split[-1]

                temp_holder = ''
                for i in range(3, len(split) - 1):
                    temp_holder += " " + split[i]

                Address_splitter = re.split(r'( BLVD| AVE| DR E| WAY| RD| ST| NE| LN| SE| PL| NW| CT| HWY| NR E| SW| DR| NB I| CIR| PKWY| TERR| TER| GRAY| MAIN| <UNKNOWN>| SH 9|DOUGLAS)+', temp_holder)

                nature = Address_splitter[-1].strip()
                address = ''
                for i in range(len(Address_splitter)-1):
                    address += ' ' +Address_splitter[i].strip() + ' '
                    
                if address == "":
                    address = re.split(' ', nature)[0]
                    
                    temp = ''
                    for i in re.split(' ', nature)[1:]:
                        temp += i + " "
                    nature = temp.strip()

                incidents.append(
                    [Date_Time, Incident_number, address, nature, Inc_Ori])

        return incidents
    except BaseException:
        print('issue with file reading')


def createdb():
    try:
        db = 'normanpd.db'
        conn = sqlite3.connect('normanpd.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE if not exists incidents (
                        incident_time TEXT,
                        incident_number TEXT,
                        incident_location TEXT,
                        nature TEXT,
                        incident_ori TEXT
                        ); ''')

        conn.commit()
        conn.close()
        return db

    except BaseException:
        print("Issue creating db")


def populatedb(db, incidents):
    try:
        incident_data=incidents

        con = sqlite3.connect(db)
        cur = con.cursor()

        for i in incidents:
            if i[3] == '':
                i[3] = 'Null'
            cur.execute("INSERT into incidents VALUES (?,?,?,?,?)" , (i))
        con.commit()
        con.close()
        
    except:
        print('Issue populating db')


def status(db):
    try:
        db = 'normanpd.db'
        con = sqlite3.connect(db)
        cur = con.cursor()

        records = cur.execute(
            "SELECT Nature, count(*) FROM incidents GROUP BY Nature order by Nature")

        for row in records:
            temp = row[0]
           #if temp == "":
           #     temp = 'NULL'
            print(f"{temp} | {row[1]}")

        cur.execute("DROP TABLE incidents;")
        con.commit()
        con.close()

    except BaseException:
        print("Issue printing status")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
