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

        for _ in range(items_per_team):
            team_list.append(item_list.pop(0))

            if _ == items_per_team:
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
    file_name_list = []

    for _ in file_name:
        file_name_list.append(_)
        for line in open(path_list+"/"+_):
            res = re.findall(regex, line)
            if len(res):
                mat_list.append(res[0])

    final_list["schematic_files"] = file_name_list

    for mat in mat_list:
        if mat[0] not in final_list.keys():
            final_list[mat[0]] = int(mat[1])
        else:
            final_list[mat[0]] = final_list[mat[0]] + int(mat[1])

    return final_list

def rename_files():
    filename_regex = r'IMG_\d+_\d+_\d+'

    for _ in os.listdir(path_list):
        for line in open(path_list+"/"+_):
            res = re.findall(filename_regex, line)
            if len(res):
                os.rename(path_list+"/"+_,path_list+"/"+res[0]+".txt")


if __name__ == '__main__':
    # rename_files() #TODO: Activate this function on when its time to go for real
    teams_division = separate_teams()
    for team in teams_division.keys():
        complete_list = get_mats(teams_division[team])

        f = open(path_output+"/"+team+".txt", "x")
        f.close()

        f = open(path_output + "/" + team + ".txt", "w")
        f.write(f"SCHEMATICS ON THIS LIST: \n")
        for i in complete_list["schematic_files"]:
            f.write(f"{i[0:-4]}, ")

        f.write("\n\n")
        f.write("MATERIAL  |  AMOUNT\n")
        f.close()

        f = open(path_output+"/"+team+".txt", "a")
        for i in complete_list.keys():
            if i == "schematic_files":
                continue
            f.write(f"{i}  |  {complete_list[i]}\n")
        f.close()