import re
import os

path_list = os.getcwd()+"/list"
path_output = os.getcwd()+"/output"
path_separated = os.getcwd()+"/separated"

regex = r'^\|\s([A-Za-z\s]+[A-Za-z])\s+\|\s+(\d+)'

def separate_teams(amount_teams=4):
    index_team = 0
    team_name = "team_"
    complete_list_teams = dict()

    amount_items = len(os.listdir(path_list))

    items_per_team = int(amount_items / amount_teams)
    item_list = os.listdir(path_list)

    while index_team < amount_teams:
        team_list = []

        for i in range(items_per_team):
            team_list.append(item_list.pop(0))

            if i == items_per_team:
                break

        complete_list_teams[team_name+str(index_team)] = team_list
        index_team += 1

    if len(item_list) > 0:
        missed = []
        while len(item_list) > 0:
            missed.append(item_list.pop(0))

        complete_list_teams["extra"] = missed

    return complete_list_teams


def get_mats(file_name):
    mat_list = []
    final_list = dict()

    for i in file_name:
        for line in open(path_list+"/"+i):
            res = re.findall(regex, line)
            if len(res):
                mat_list.append(res[0])

    for mat in mat_list:
        if mat[0] not in final_list.keys():
            final_list[mat[0]] = int(mat[1])
        else:
            final_list[mat[0]] = final_list[mat[0]] + int(mat[1])

    return final_list

if __name__ == '__main__':
    teams_division = separate_teams()
    for team in teams_division.keys():
        complete_list = get_mats(teams_division[team])

        f = open(path_output+"/"+team+".txt", "x")
        f.close()

        f = open(path_output + "/" + team + ".txt", "w")
        f.write("MATERIAL  |  AMOUNT\n")
        f.close()

        f = open(path_output+"/"+team+".txt", "a")
        for i in complete_list.keys():
            f.write(f"{i}  |  {complete_list[i]}\n")
        f.close()