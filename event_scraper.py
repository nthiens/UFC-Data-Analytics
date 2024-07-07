from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

url = "http://ufcstats.com/statistics/events/completed?page=all"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

event_len = len(soup.find_all("tr", class_="b-statistics__table-row")) 
processed = 0
event_id = 0


with open('events.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    field = ["event_id", "event_name", "date", "city", "region", "nation", "event_link"]
    writer.writerow(field)
    
    event_counter = 2
    all_event_info = []
    while event_counter < (event_len):
        event_id = event_id + 1
        event_info = []
        events = (soup.find_all("tr", class_="b-statistics__table-row"))[event_counter]
        event_name = (events.find("a"))
        event_link = event_name.get("href")
        event_name = event_name.text
        date = (events.find("span")).text
        location = (((events.find_all("td")))[-1]).text
        event_name = event_name.replace('\n','').strip()
    
        date = date.replace('\n','').strip().split()
        year = date[2]
        day = (date[1])[0:-1]
        month = date[0]
        if month == "January":
            month = "01"
        elif month == "February":
            month = "02"
        elif month == "March":
            month = "03"
        elif month == "April":
            month = "04"
        elif month == "May":
            month = "05"
        elif month == "June":
            month = "06"
        elif month == "July":
            month = "07"
        elif month == "August":
            month = "08"
        elif month == "September":
            month = "09"
        elif month == "October":
            month = "10"
        elif month == "November":
            month = "11"
        elif month == "December":
            month = "12"
        date = year + "-" + month + "-" + day

        location = location.replace('\n','').strip().split(", ")
        if len(location) == 2:
            city = location[0]
            region = location[0]
            nation = location[1]
        elif len(location) == 3:
            city = location[0]
            region = location[1]
            nation = location[2]

        event_info = [event_id] + [event_name] + [date] + [city] + [region] + [nation] + [event_link]
        all_event_info = all_event_info + [event_info]
        event_counter = event_counter + 1
        writer.writerow(event_info)
        processed = processed + 1
        print(str(processed) + "/" + str(event_len - 2))