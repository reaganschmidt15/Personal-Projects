from riotwatcher import LolWatcher
import pandas as pd

#https://developer.riotgames.com/apis#match-v5/GET_getMatch
api_key = 'RGAPI-821bf1ec-32b6-4488-8b2b-cb22342b10a7'
watcher = LolWatcher(api_key)
player_name = 'stevenssz'
player = watcher.summoner.by_name('na1', player_name)
player_matches = watcher.match.matchlist_by_puuid('americas', player['puuid'], count = 100, queue = 400)
queue_ids = [420, 400]
#https://static.developer.riotgames.com/docs/lol/queues.json

def stats():
    #Question 1
    games_more_wards_notsupp_success = 0
    games_as_supp = 0
    games_more_wards_supp_success = 0
    games_as_other_role = 0
    total_games = 0

    #Question 4
    games_more_damage = 0


    for match in player_matches:
        match_detail = watcher.match.by_id('americas', match)
        #builds dataframe for each match
        participants = []
        for row in match_detail['info']['participants']:
            participants_row = {}
            participants_row['summoner'] = row['summonerName']
            participants_row['champion'] = row['championName']
            participants_row['role'] = row['individualPosition']
            participants_row['win'] = row['win']
            participants_row['totalDamageDealtToChampions'] = row['totalDamageDealtToChampions']
            participants_row['goldEarned'] = row['goldEarned']
            participants_row['wards placed'] = row['wardsPlaced']
            participants_row['wards killed'] = row['wardsKilled']
            participants.append(participants_row)
        df = pd.DataFrame(participants)
        player_index = df[df['summoner'] == player_name].index[0]
        #gets the indices of player's role and their lane opponent
        role_indices = df[df['role'] == df.loc[player_index, 'role']].index
        opponent_index = 6996
        for i in role_indices:
            if i != player_index:
                opponent_index = i

        #if game is fucked and someone is double roleing
        if opponent_index == 6996:
            continue
        #Question 1: What % of time does Tippie ward more than his opposing support at the end of the game?
        if df.loc[player_index, 'wards placed'] > df.loc[opponent_index, 'wards placed']:
            if df.loc[player_index, 'role'] == 'UTILITY':
                games_more_wards_supp_success += 1
            else:
                games_more_wards_notsupp_success += 1

        #updating how many games as support
        if df.loc[player_index, 'role'] == 'UTILITY':
            games_as_supp += 1
        else: 
            games_as_other_role += 1

        #Questions 2: What % of time is Tippie (AND HIS TEAM) ahead by 12 minute mark and wins?
        #Success = Tipie had >= 5 wards than opponent.

       

        #Questions 3: What % of time is Tippie ahead from his lane opponent but the team is behind in gold by a sizable amount?

        #Question 4: More damage as opponent
        if df.loc[player_index, 'totalDamageDealtToChampions'] > df.loc[opponent_index, 'totalDamageDealtToChampions']:
            games_more_damage += 1

        total_games += 1
    #presenting results
    print(f"Total Ranked Games: {total_games}\n")
    print(f"Total games as support: {games_as_supp}")
    print(f"Total games more wards as support: {games_more_wards_supp_success}")
    print(f"Total games as other role: {games_as_other_role}")
    print(f"Total games more wards as other role: {games_more_wards_notsupp_success}\n")
    print(f"Total games more damage to champs as opponent: {games_more_damage}")

def main():
    stats()

if __name__ == "__main__":
    main()