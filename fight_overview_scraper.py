from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

fight_id = 0
all_events_link = []
all_events_name = []
num_events = 0

with open('events.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        all_events_link = all_events_link + [(row[6])]
        all_events_name = all_events_name + [(row[1])]
event_name_and_link = [[all_events_link[i], all_events_name[i]] for i in range(len(all_events_name))]
event_name_and_link = event_name_and_link[1:]

# for event in event_name_and_link:
#     page = urlopen(event[0])
#     html = page.read().decode("utf-8")
#     soup = BeautifulSoup(html, "html.parser")
#     length = len(soup.find_all("tr", class_="b-fight-details__table-row__hover"))
#     num_events = num_events + length
#     print(event[1] + " has " + str(length) + " fights")
# print(num_events)

fight_id = 0
processed = 0

with open('fights_overview.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    field = ["fight_id", "event_name", "fighter_1", "fighter_1_result", "fighter_2", "fighter_2_result"]
    field = field + ["bout_type", "method", "end_round", "end_time_round", "max_round", "referee", "fight_link"]
    
    writer.writerow(field)

    all_events_link = all_events_link[1:]
    for event in all_events_link:
        page = urlopen(event)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        fight = (soup.find_all(class_='b-fight-details__table-row'))
        fight = (fight[1:])
        for i in fight:
            fight_id = fight_id + 1
            processed = processed + 1
            i = (i["data-link"])
            fight_page = urlopen(i)
            fight_html = fight_page.read().decode("utf-8")
            fight_soup = BeautifulSoup(fight_html, "html.parser")
            event_name = (fight_soup.find_all(class_='b-link')[0]).text
            event_name = event_name.replace('\n','').strip()
            fighters = (fight_soup.find_all(class_='b-fight-details__person-link'))
            fighter_1 = (fighters[0]).text.strip()
            fighter_2 = (fighters[1]).text.strip()

            fighter_1_result = (fight_soup.find_all(class_="b-fight-details__person-status")[0]).text
            fighter_1_result = fighter_1_result.replace('\n','').strip()

            fighter_2_result = (fight_soup.find_all(class_="b-fight-details__person-status")[1]).text
            fighter_2_result = fighter_2_result.replace('\n','').strip()

            weight_class = (fight_soup.find_all(class_='b-fight-details__fight-title')[0]).text
            weight_class = weight_class.replace('\n','').strip()

            method = (fight_soup.find_all(class_='b-fight-details__label')[0]).find_next_sibling().text.strip()

            info =  (fight_soup.find_all(class_='b-fight-details__text-item'))
            end_round = (info[0])
            end_round = (end_round.text.strip())[-1]

            end_time_round =  (info[1])
            end_time_round = (end_time_round.text.strip())[-4:]
            end_time_round = int((end_time_round.split(":"))[0]) * 60 + int((end_time_round.split(":"))[1])

            max_round = (info[2]).text.strip()
            max_round = ((max_round[12:]).strip())[0]
            if max_round == "N":
                max_round = ""

            referee = (info[3]).text.strip()
            referee = (referee[20:]).strip()

            overview = [str(fight_id)] + [event_name] + [fighter_1] + [fighter_1_result] + [fighter_2] + [fighter_2_result]
            overview = overview + [weight_class] + [method] + [end_round] + [end_time_round] + [max_round] + [referee] + [i]
            writer.writerow(overview)
            print(processed)



# fight = "http://ufcstats.com/fight-details/636fd144716a3084"
# page = urlopen(fight)
# html = page.read().decode("utf-8")
# soup = BeautifulSoup(html, "html.parser")


# event_name = (soup.find_all(class_='b-link')[0]).text
# event_name = event_name.replace('\n','').strip()

# fighters = (soup.find_all(class_='b-fight-details__person-link'))
# fighter_1 = (fighters[0]).text.strip()
# fighter_2 = (fighters[1]).text.strip()

# fighter_1_result = (soup.find_all(class_="b-fight-details__person-status")[0]).text
# fighter_1_result = fighter_1_result.replace('\n','').strip()

# fighter_2_result = (soup.find_all(class_="b-fight-details__person-status")[1]).text
# fighter_2_result = fighter_2_result.replace('\n','').strip()

# weight_class = (soup.find_all(class_='b-fight-details__fight-title')[0]).text
# weight_class = weight_class.replace('\n','').strip()

# method = (soup.find_all(class_='b-fight-details__label')[0]).find_next_sibling().text.strip()

# info =  (soup.find_all(class_='b-fight-details__text-item'))
# end_round = (info[0])
# end_round = (end_round.text.strip())[-1]

# end_time_round =  (info[1])
# end_time_round = (end_time_round.text.strip())[-4:]
# end_time_round = int((end_time_round.split(":"))[0]) * 60 + int((end_time_round.split(":"))[1])

# max_round = (info[2]).text.strip()
# max_round = ((max_round[12:]).strip())[0]
# if max_round == "N":
#     max_round = ""

# referee = (info[3]).text.strip()
# referee = (referee[20:]).strip()

# overview = [str(fight_id)] + [event_name] + [fighter_1] + [fighter_1_result] + [fighter_2] + [fighter_2_result]
# overview = overview + [weight_class] + [method] + [end_round] + [end_time_round] + [max_round] + [referee]
# print(overview)
