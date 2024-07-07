from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

all_fighter_links = []
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
# alphabet = ["z"]
all_fighter_info = []
processed = 0
fighter_id = 0
fighter_len = 0

for char in alphabet:
    url = "http://ufcstats.com/statistics/fighters?char=" + char + "&page=all"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    length = len(soup.find_all("tr", class_="b-statistics__table-row")) - 2
    fighter_len = fighter_len + length
    print(str(length) + " fighters with last name starting with " + char)
print(str(fighter_len) + " fighters in the UFC database")


with open('fighters.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    field = ["fighter_id", "name", "nickname", "height", "reach", "weight", "stance", "dob"]
    field = field + ["slpm", "str_acc", "sapm", "str_def", "td_avg", "td_acc", "td_def", "sub_avg", "fighter_link"]
    writer.writerow(field)

    for letter in alphabet:
        url = "http://ufcstats.com/statistics/fighters?char=" + letter + "&page=all"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        fighter_counter = 2
        all_fighters_alpha = []
        fighters_len = len(soup.find_all("tr", class_="b-statistics__table-row"))
        while fighter_counter < (fighters_len):
            fighter_alpha = (soup.find_all("tr", class_="b-statistics__table-row"))[fighter_counter]
            fighter = fighter_alpha.find("a")
            fighter_link = fighter_link = fighter.get("href")
            all_fighters_alpha = all_fighters_alpha + [fighter_link]
            fighter_counter = fighter_counter + 1

            fighter_info = []
            page = urlopen(fighter_link)
            html = page.read().decode("utf-8")
            parse = BeautifulSoup(html, "html.parser")

            fighter_id = fighter_id + 1
            name = parse.find("span", "b-content__title-highlight").text
            name = name.replace('\n','').strip()

            nickname = parse.find("p", "b-content__Nickname").text.strip()

            height = ((parse.find_all("li", class_="b-list__box-list-item_type_block"))[0])
            height = height.i.next_sibling.text.strip().replace("'","").replace("\"","")
            height = height.split()
            if height == ["--"]:
                height = ""
            else:
                height = (int(height[0]) * 12) + int(height[1])

            information = (parse.find_all("li", class_="b-list__box-list-item_type_block"))

            reach = (information[2].i.next_sibling.text.strip().replace("'","").replace("\"",""))
            if reach[0] == "-":
                reach = ""
            else:
                reach = int(reach)

            weight = (information[1].i.next_sibling.text.strip().replace("'","").replace("\"",""))[:-5]
            if weight == "":
                weight = ""
            else:
                weight = int(weight)

            stance = (information[3].i.next_sibling.text.strip())
            # stance = stance.i.next_sibling.text.strip()
            if stance == "":
                stance = ""

            dob = (information[4].i.next_sibling.text.strip())
            # dob = dob.i.next_sibling.text.strip()
            if dob[0] == "-":
                dob = ""
            else:
                dob = dob.replace('\n','').strip().split()
                year = dob[2]
                day = (dob[1])[0:-1]
                month = dob[0]
                if month == "Jan":
                    month = "01"
                elif month == "Feb":
                    month = "02"
                elif month == "Mar":
                    month = "03"
                elif month == "Apr":
                    month = "04"
                elif month == "May":
                    month = "05"
                elif month == "Jun":
                    month = "06"
                elif month == "Jul":
                    month = "07"
                elif month == "Aug":
                    month = "08"
                elif month == "Sep":
                    month = "09"
                elif month == "Oct":
                    month = "10"
                elif month == "Nov":
                    month = "11"
                elif month == "Dec":
                    month = "12"
                dob = year + "-" + month + "-" + day

            # slpm = (information[5])
            slpm = float(information[5].i.next_sibling.text.strip())

            # str_acc = ((parse.find_all("li", class_="b-list__box-list-item_type_block"))[6])
            str_acc = int((information[6].i.next_sibling.text.strip())[:-1]) * 0.01

            # sapm = ((parse.find_all("li", class_="b-list__box-list-item_type_block"))[7])
            sapm = float(information[7].i.next_sibling.text.strip())

            # str_def = ((parse.find_all("li", class_="b-list__box-list-item_type_block"))[8])
            str_def = int((information[8].i.next_sibling.text.strip())[:-1]) * 0.01

            # td_avg = ((parse.find_all("li", class_="b-list__box-list-item_type_block"))[10])
            td_avg = float(information[10].i.next_sibling.text.strip())

            # td_acc = ((parse.find_all("li", class_="b-list__box-list-item_type_block"))[11])
            td_acc = int((information[11].i.next_sibling.text.strip())[:-1]) * 0.01

            # td_def = ((parse.find_all("li", class_="b-list__box-list-item_type_block"))[12])
            td_def = int((information[12].i.next_sibling.text.strip())[:-1]) * 0.01

            # sub_avg = ((parse.find_all("li", class_="b-list__box-list-item_type_block"))[13])
            sub_avg = float(information[13].i.next_sibling.text.strip())

            fighter_info = fighter_info + [fighter_id] + [name] + [nickname] + [height] + [reach] + [weight] + [stance] + [dob]
            fighter_info = fighter_info + [slpm] + [str_acc] + [sapm] + [str_def] + [td_avg] + [td_acc] + [td_def] + [sub_avg] + [fighter_link]
            writer.writerow(fighter_info)
            processed = processed + 1
            print(str(processed) + "/" + str(fighter_len))