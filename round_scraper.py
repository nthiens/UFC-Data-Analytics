from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

all_fight_links = []

with open('fights_overview.csv', 'r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        all_fight_links = all_fight_links + [row[12]]
num_fights = len(all_fight_links)

with open('rounds.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    field =  ["round_id", "event_name","round","fighter_name", "kd", "ts_landed"] 
    field = field + ["ts_attempted","td_landed","td_attempted"] 
    field = field + ["sub_attempted","rev","control","ss_landed"] 
    field = field + ["ss_attempted","head_ss_attempted","head_ss_landed"] 
    field = field + ["body_ss_attempted","body_ss_landed","leg_ss_attempted"] 
    field = field + ["leg_ss_landed","distance_ss_attempted","distance_ss_landed"]
    field = field  + ["clinch_ss_attempted","clinch_ss_landed", "ground_ss_attempted","ground_ss_landed"]
    writer.writerow(field)

    all_fight_links = all_fight_links[1:]
    fights = 0
    round_id = 0

    for fight in all_fight_links:
        page = urlopen(fight)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        rounds = (soup.find_all("tr", class_="b-fight-details__table-row")) 
        all_rounds = int((len(rounds) - 6)/2)
        round_index = list(range(3, 3 + all_rounds)) + list(range(7 + all_rounds, 7 + all_rounds + all_rounds))
        first_half = round_index[:len(round_index)//2]
        second_half = round_index[len(round_index)//2:]
        round_index = list(zip(first_half,second_half))
        max_rounds = rounds
        current_round = 0


        for round in round_index:
            
            current_round = current_round + 1
            fighter_1 = []
            fighter_2 = []

            names = (soup.find_all("a", class_="b-link"))
            fight_name = names[0].text.strip()
            f_1_name = names[1].text.strip()
            f_2_name = names[2].text.strip()

            fight_stats_top = (rounds[round[0]])
            fight_stats_bottom = rounds[round[1]-1]

            fight_stats_top = fight_stats_top.find_all("p", "b-fight-details__table-text")
            fight_stats_bottom = fight_stats_bottom.find_all("p", "b-fight-details__table-text")

            f_1_kd = fight_stats_top[2].text.strip()
            f_2_kd = fight_stats_top[3].text.strip()

            f_1_ts_landed = fight_stats_top[8].text.strip().split(" ")[0]
            f_1_ts_attempted = fight_stats_top[8].text.strip().split(" ")[2]
            f_2_ts_landed = fight_stats_top[9].text.strip().split(" ")[0]
            f_2_ts_attempted = fight_stats_top[9].text.strip().split(" ")[2]

            f_1_td_landed = fight_stats_top[10].text.strip().split(" ")[0]
            f_1_td_attempted = fight_stats_top[10].text.strip().split(" ")[2]
            f_2_td_landed = fight_stats_top[11].text.strip().split(" ")[0]
            f_2_td_attempted = fight_stats_top[11].text.strip().split(" ")[2]

            f_1_sub_attempted = fight_stats_top[14].text.strip()
            f_2_sub_attempted = fight_stats_top[15].text.strip()

            f_1_rev = fight_stats_top[16].text.strip()
            f_2_rev = fight_stats_top[17].text.strip()

            f_1_control = fight_stats_top[18].text.strip().split(":")
            if f_1_control == ["--"]:
                f_1_control = ""
            else:
                f_1_control = int(f_1_control[0]) * 60 + int(f_1_control[1])
            f_2_control = fight_stats_top[19].text.strip().split(":")
            if f_2_control == ["--"]:
                f_2_control = ""
            else:
                f_2_control = int(f_2_control[0]) * 60 + int(f_2_control[1])

            f_1_ss_landed = fight_stats_bottom[2].text.strip().split(" ")[0]
            f_1_ss_attempted = fight_stats_bottom[2].text.strip().split(" ")[2]
            f_2_ss_landed = fight_stats_bottom[3].text.strip().split(" ")[0]
            f_2_ss_attempted = fight_stats_bottom[3].text.strip().split(" ")[2]

            f_1_head_ss_attempted = fight_stats_bottom[6].text.strip().split(" ")[0]
            f_1_head_ss_landed = fight_stats_bottom[6].text.strip().split(" ")[2]
            f_2_head_ss_attempted = fight_stats_bottom[7].text.strip().split(" ")[0]
            f_2_head_ss_landed = fight_stats_bottom[7].text.strip().split(" ")[2]

            f_1_body_ss_attempted = fight_stats_bottom[8].text.strip().split(" ")[0]
            f_1_body_ss_landed = fight_stats_bottom[8].text.strip().split(" ")[2]
            f_2_body_ss_attempted = fight_stats_bottom[9].text.strip().split(" ")[0]
            f_2_body_ss_landed = fight_stats_bottom[9].text.strip().split(" ")[2]

            f_1_leg_ss_attempted = fight_stats_bottom[10].text.strip().split(" ")[0]
            f_1_leg_ss_landed = fight_stats_bottom[10].text.strip().split(" ")[2]
            f_2_leg_ss_attempted = fight_stats_bottom[11].text.strip().split(" ")[0]
            f_2_leg_ss_landed = fight_stats_bottom[11].text.strip().split(" ")[2]

            f_1_distance_ss_attempted = fight_stats_bottom[12].text.strip().split(" ")[0]
            f_1_distance_ss_landed = fight_stats_bottom[12].text.strip().split(" ")[2]
            f_2_distance_ss_attempted = fight_stats_bottom[13].text.strip().split(" ")[0]
            f_2_distance_ss_landed = fight_stats_bottom[13].text.strip().split(" ")[2]

            f_1_clinch_attempted = fight_stats_bottom[14].text.strip().split(" ")[0]
            f_1_clinch_landed = fight_stats_bottom[14].text.strip().split(" ")[2]
            f_2_clinch_attempted = fight_stats_bottom[15].text.strip().split(" ")[0]
            f_2_clinch_landed = fight_stats_bottom[15].text.strip().split(" ")[2]

            f_1_ground_attempted = fight_stats_bottom[16].text.strip().split(" ")[0]
            f_1_ground_landed = fight_stats_bottom[16].text.strip().split(" ")[2]
            f_2_ground_attempted = fight_stats_bottom[17].text.strip().split(" ")[0]
            f_2_ground_landed = fight_stats_bottom[17].text.strip().split(" ")[2]
            
            round_id = round_id + 1

            fighter_1 = [round_id] + [fight_name] + [current_round] + [f_1_name] + [f_1_kd] + [f_1_ts_landed] 
            fighter_1 = fighter_1 + [f_1_ts_attempted] + [f_1_td_landed] + [f_1_td_attempted] 
            fighter_1 = fighter_1 + [f_1_sub_attempted] + [f_1_rev] + [f_1_control] + [f_1_ss_landed] 
            fighter_1 = fighter_1 + [f_1_ss_attempted] + [f_1_head_ss_attempted] + [f_1_head_ss_landed] 
            fighter_1 = fighter_1 + [f_1_body_ss_attempted] + [f_1_body_ss_landed] + [f_1_leg_ss_attempted] 
            fighter_1 = fighter_1 + [f_1_leg_ss_landed] + [f_1_distance_ss_attempted] + [f_1_distance_ss_landed]
            fighter_1 = fighter_1  + [f_1_clinch_attempted] + [f_1_clinch_landed] + [f_1_ground_attempted] + [f_1_ground_landed]

            round_id = round_id + 1
            
            fighter_2 = [round_id] + [fight_name] + [current_round] + [f_2_name] + [f_2_kd] + [f_2_ts_landed] 
            fighter_2 = fighter_2 + [f_2_ts_attempted] + [f_2_td_landed] + [f_2_td_attempted] 
            fighter_2 = fighter_2 + [f_2_sub_attempted] + [f_2_rev] + [f_2_control] + [f_2_ss_landed] 
            fighter_2 = fighter_2 + [f_2_ss_attempted] + [f_2_head_ss_attempted] + [f_2_head_ss_landed] 
            fighter_2 = fighter_2 + [f_2_body_ss_attempted] + [f_2_body_ss_landed] + [f_2_leg_ss_attempted] 
            fighter_2 = fighter_2 + [f_2_leg_ss_landed] + [f_2_distance_ss_attempted] + [f_2_distance_ss_landed]
            fighter_2 = fighter_2  + [f_2_clinch_attempted] + [f_2_clinch_landed] + [f_2_ground_attempted] + [f_2_ground_landed]

            # print(fighter_1)
            # print(fighter_2)
            writer.writerow(fighter_1)
            writer.writerow(fighter_2)
        fights = fights + 1
        print(str(fights) + "/" + str(num_fights))
