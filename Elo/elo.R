library(dplyr)

all_fights <- fights_overview %>% arrange(desc(fight_id))
all_fights <- inner_join(all_fights, events, by="event_name")
all_fights <- all_fights %>% 
  select(fighter_1_link, fighter_1, fighter_1_result, fighter_2_link, fighter_2, fighter_2_result, date)

fighters_elo <- fighters %>% select(fighter_link, name) %>% mutate(elo=1500)
fighters_elo <- as.data.frame(fighters_elo)


elo_single_fight <- function(row_fight, current_elo) {
  fighter_1_elo <- current_elo %>% 
    filter(fighter_link == row_fight$fighter_1_link) %>% select(elo)
  fighter_2_elo <- current_elo %>% 
    filter(fighter_link == row_fight$fighter_2_link) %>% select(elo)
  
  if (row_fight$fighter_1_result == "NC") {
    elo_in_order <- data.frame(
      fighter_id = c(row_fight$fighter_1_link, row_fight$fighter_2_link),
      name = c(row_fight$fighter_1, row_fight$fighter_2),
      elo = c(fighter_1_elo$elo[1], fighter_2_elo$elo[1]),
      date = as.Date(c(row_fight$date, row_fight$date))
    )
    final <- list(
      elo_in_order = elo_in_order,
      current_elo = current_elo
    )
    return (final)
  }
  
  winner <- NULL
  winner_old_elo <- NULL
  loser <- NULL
  loser_old_elo <- NULL
  draw <- FALSE
  
  if ((row_fight$fighter_1_result == "W") & (row_fight$fighter_2_result == "L")) {
    winner <- row_fight$fighter_1_link
    loser <- row_fight$fighter_2_link
    winner_name <- row_fight$fighter_1
    loser_name <- row_fight$fighter_2
    winner_old_elo <- current_elo %>% 
      filter(fighter_link == row_fight$fighter_1_link) %>% select(elo)
    loser_old_elo <- current_elo %>% 
      filter(fighter_link == row_fight$fighter_2_link) %>% select(elo)
  } else if ((row_fight$fighter_1_result == "L") & (row_fight$fighter_2_result == "W")) {
    winner <- row_fight$fighter_2_link
    loser <- row_fight$fighter_1_link
    winner_name <- row_fight$fighter_2
    loser_name <- row_fight$fighter_1
    winner_old_elo <- current_elo %>% 
      filter(fighter_link == row_fight$fighter_2_link) %>% select(elo)
    loser_old_elo <- current_elo %>% 
      filter(fighter_link == row_fight$fighter_1_link) %>% select(elo)
  } else {
    winner <- row_fight$fighter_1_link
    loser <- row_fight$fighter_2_link
    winner_name <- row_fight$fighter_1
    loser_name <- row_fight$fighter_2
    winner_old_elo <- current_elo %>% 
      filter(fighter_link == row_fight$fighter_1_link) %>% select(elo)
    loser_old_elo <- current_elo %>% 
      filter(fighter_link == row_fight$fighter_2_link) %>% select(elo)
    draw = TRUE
  }
  
  k <- 30
  winner_expected_score <- 1/(1+10^((loser_old_elo - winner_old_elo)/400))
  loser_expected_score <- 1/(1+10^((winner_old_elo - loser_old_elo)/400))
  
  if (draw == FALSE) {
    winner_new_elo <- winner_old_elo + k * (1 - winner_expected_score)
    winner_new_elo <- winner_new_elo$elo[1]
    loser_new_elo <- loser_old_elo + k * (0 - loser_expected_score)
    loser_new_elo <- loser_new_elo$elo[1]
  } else {
    winner_new_elo <- winner_old_elo + k * (0.5 - winner_expected_score)
    winner_new_elo <- winner_new_elo$elo[1]
    loser_new_elo <- loser_old_elo + k * (0.5 - loser_expected_score)
    loser_new_elo <- loser_new_elo$elo[1]
  }
  
  current_elo$elo[current_elo$fighter_link == winner] <- winner_new_elo
  current_elo$elo[current_elo$fighter_link == loser] <- loser_new_elo
  fighters_elo <- current_elo
  
  elo_in_order <- data.frame(
    fighter_id = c(winner, loser),
    name = c(winner_name, loser_name),
    elo = c(winner_new_elo, loser_new_elo),
    date = as.Date(c(row_fight$date, row_fight$date))
  )
  
  final <- list(
    elo_in_order = elo_in_order,
    fighters_elo = fighters_elo
  )
  
  return(final)
}

elo_all_fights <- function(all_possible_fights, starting_elo) {
  
  elo_in_order <- data.frame(
    fighter_id = character(),
    name = character(),
    elo = double(),
    date = as.Date(character())
  )
  
  for (fight in 1:nrow(all_possible_fights)) {
    row <- all_possible_fights[fight,]
    row <- as.data.frame(row)
    row <- elo_single_fight(row, starting_elo)
    starting_elo <- row[[2]]
    elo_in_order <- rbind(elo_in_order, row[[1]])
    print(row[[1]])
  }
  
  return (elo_in_order)
}

## Run once########################################
all_elo <- elo_all_fights(all_fights, fighters_elo)
###################################################

names(all_elo)[names(all_elo) == "fighter_id"] <- "fighter_link"
all_elo <- inner_join(all_elo, fighters, by = "fighter_link")
all_elo <- all_elo %>% select(fighter_link, name.y, weight, elo, date)
names(all_elo)[names(all_elo) == "name.y"] <- "name"
all_elo

get_elo_specific <- function(start_date, end_date, min_weight, max_weight, elo_data, criteria, max_rank) {
  date_range <- elo_data[elo_data$date >= start_date,]
  date_range <- date_range[date_range$date <= end_date,]
  
  if (criteria == "latest") {
    ranking <- date_range %>% group_by(name) %>% slice_max(date, n = 1) %>% 
      arrange(desc(elo))
  } else if (criteria == "peak") {
    ranking <- date_range %>% group_by(name) %>% slice_max(elo, n = 1) %>% 
      arrange(desc(elo))
  }
  ranking <- ranking %>% filter(weight >= min_weight) %>% filter(weight <= max_weight)
  ranking <- head(ranking, n = max_rank)
  return (ranking)
}

earliest_date <- as.Date("1994-03-11")
latest_date <- as.Date("2024-08-24")
one_year_before_latest_date <- latest_date - 365

p4p_current <- get_elo_specific(one_year_before_latest_date, latest_date, 100, 400, all_elo, "latest", 15)
p4p_current <- p4p_current %>% select(name, weight, elo, date)
p4p_current

p4p_alltime <- get_elo_specific(earliest_date, latest_date, 100, 400, all_elo, "peak", 15)
p4p_alltime <- p4p_alltime %>% select(name, weight, elo, date)
p4p_alltime

top_15_lightweight <- get_elo_specific(one_year_before_latest_date, latest_date, 155, 155, all_elo, "latest", 15)
top_15_lightweight <- top_15_lightweight %>% select(name, weight, elo, date)
top_15_lightweight

top_15_welterweight <- get_elo_specific(one_year_before_latest_date, latest_date, 170, 170, all_elo, "latest", 15)
top_15_welterweight <- top_15_welterweight %>% select(name, weight, elo, date)
top_15_welterweight

top_15_middleweight <- get_elo_specific(one_year_before_latest_date, latest_date, 185, 185, all_elo, "latest", 15)
top_15_middleweight <- top_15_middleweight %>% select(name, weight, elo, date)
top_15_middleweight

top_15_lightheavyweight <- get_elo_specific(one_year_before_latest_date, latest_date, 205, 205, all_elo, "latest", 15)
top_15_lightheavyweight <- top_15_lightheavyweight %>% select(name, weight, elo, date)
top_15_lightheavyweight

top_15_heavyweight <- get_elo_specific(one_year_before_latest_date, latest_date, 206, 266, all_elo, "latest", 15)
top_15_heavyweight <- top_15_heavyweight %>% select(name, weight, elo, date)
top_15_heavyweight
