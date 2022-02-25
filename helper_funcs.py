from bs4 import BeautifulSoup

import pandas as pd
import requests
import os
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def add_scores(t1, t2, team1_score, team2_score):
    t1_round_wins = sum(team1_score)  # t1 round win is t2 round loss
    t2_round_wins = sum(team2_score)
    rounds_played = t1_round_wins + t2_round_wins
    maps_played = len(team1_score)
    t1_maps_won = sum(
        x > y for x, y in zip(team1_score, team2_score))  # zip through elements put 1 for each map then sum

    t1["Rounds Played"] = rounds_played
    t1["Round Wins"] = t1_round_wins
    t1["Round Losses"] = t2_round_wins
    t1["Maps played"] = maps_played
    t1["Maps Won"] = t1_maps_won
    t1["Maps Lost"] = maps_played - t1_maps_won

    t2["Rounds Played"] = rounds_played
    t2["Round Wins"] = t2_round_wins
    t2["Round Losses"] = t1_round_wins
    t2["Maps played"] = maps_played
    t2["Maps Won"] = maps_played - t1_maps_won
    t2["Maps Lost"] = t1_maps_won

    t1.sort_values(by=["Name"], inplace=True, ascending=True, ignore_index=True)
    t2.sort_values(by=["Name"], inplace=True, ascending=True, ignore_index=True)
    return t1, t2


def parse_table(_match_link):
    match = requests.get(_match_link)
    df_list = pd.read_html(match.text)  # this parses all the tables in webpages to a list
    team1_score, team2_score = get_match_status(_match_link)
    t1 = clean_table(df_list[0])
    t2 = clean_table(df_list[1])
    team1, team2 = add_scores(t1, t2, team1_score, team2_score)

    # print(team1)
    # print(team2)
    match_name = team1["Team"][0]+" vs "+team2["Team"][0]
    # print(match_name)
    path = 'CSV files'
    os.makedirs(path, exist_ok=True)
    pd.concat([team1, team2], axis=0, ignore_index=True).to_csv(path+'/'+match_name+'.csv')


def clean_table(df):
    to_drop = ['Unnamed: 1', 'ACS', 'KAST', 'ADR', 'HS%', '+/–.1', '+/–']
    df.drop(to_drop, axis=1, inplace=True)  # Unnecessary
    df['D'] = df['D'].str.extract('(\d+)').astype(int)  # Convert all to int
    df.rename(columns={'Unnamed: 0': 'Name_Team'}, inplace=True)
    df[['Name', 'Team']] = df['Name_Team'].str.split(' ', 1,
                                                     expand=True)
    cols = ['Team', 'Name', 'K', 'D', 'A', 'FK', 'FD']
    df = df[cols]
    # df.style.set_caption("Hello World")
    return df


def create_soup(URL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    page = requests.get(URL, headers=headers)
    soup_obj = BeautifulSoup(page.content, "html.parser")
    return soup_obj


class Event:
    httpstring = 'https://www.vlr.gg'

    def __init__(self, URL):
        self.soup = create_soup(URL)

    def get_team_names(self):
        team_tags = self.soup.find_all("div", {"class": "team-name text-of"})
        teams = list({team.text.strip() for team in team_tags})
        print(teams)
        return teams

    def get_matches(self):
        event_tags = self.soup.find_all("a", {
            "class": "wf-module-item match-item mod-color mod-left mod-bg-after-red mod-first"})
        event_list = []
        for tags in event_tags:
            child = tags.findChildren("div", {
                "class": "ml-status"})
            if child[0].text == 'Completed':
                event_list.append(Event.httpstring + tags["href"])  # Only append the href tags if completed
        # print(event_list)
        return event_list


def get_match_status(link):
    match = create_soup(link)
    left_team = []
    right_team = []
    scores = match.find_all("div", {
        "class": "score"})
    for score in scores:
        if score['style'] == 'margin-right: 12px;':
            left_team.append(int(score.text))  # left and right margins are switched
        else:
            right_team.append(int(score.text))
    # print(left_team)
    # print(right_team)
    return left_team, right_team


if __name__ == '__main__':
    event_link = "https://www.vlr.gg/event/matches/799/champions-tour-north-america-stage-1-challengers/?series_id=1559"
    match_link = "https://www.vlr.gg/70060/rise-vs-version1-champions-tour-north-america-stage-1-challengers-w2/?game=all&tab=overview"
    # event1 = EventCaller(event_link)
    # parse_table(event1.get_matches()[1])
    # get_match_status(event1.get_matches()[1])
    # get_match_status(match_link)
    parse_table(match_link)
