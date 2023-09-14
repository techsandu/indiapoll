#singlerun files
import pandas as pd
import os
import re
import mysql.connector as conn
import mysql.connector.errors as errorcode
from Utility.sqlQuery import SqlUtility as utility
from Utility.common_classes import Common as c
from Utility.common_classes import MyCustomException as ex
from Utility.query_handler import query_handler as query
from Utility.data_cleaner import data_clear as dc
import math
import re


def remove_whitespace_after_period(input_string):
    # Use regular expression to replace spaces after a period with no space
    output_string = re.sub(r'\.\s+', '.', input_string)
    return output_string

def remove_spaces_and_dots(input_string):
    cleaned_string = input_string.replace(" ", "").replace(".", "")
    return cleaned_string
def handle_old_candidate(data,party,legit,result_year):
    candi_Array = []
    for i, j in data.iterrows():
        result_dict = {}
        candi_name = j["Candidate Name"]
        candi_name = re.sub(r'^\d\s*', '', candi_name)
        temp_candi_name = remove_spaces_and_dots(candi_name).lower()
        tem_party = dc.party_cleaner(j[" Party Name"].lower())
        party_id = party[tem_party]
        if legit[j["Constituency Name"]] == 81:
            print("You need tp ")

        # check data is already avaliable
        candi_select_query = query.sData
        candi_data = (temp_candi_name,party_id)
        candi_id_Array = utility.select_query(candi_select_query, candi_data)
        candi_id = None
        if len(candi_id_Array) == 0:
            age = 0
            if pd.isna(j["Candidate Age"]):
                age = 0
            else:
                age = j["Candidate Age"]
            sex = "NA"
            if pd.isna(j["Candidate Sex"]):
                sex = "NA"
            else:
                sex = j["Candidate Sex"]
            insert_data = (candi_name, party_id, age, sex, "")
            insert_candi_query = "insert into candidates(candi_name,party_id,candi_age,candi_sex,candi_category) values(%s,%s,%s,%s,%s)  RETURNING candi_id;"
            insert_result = utility.insert_single(insert_candi_query, insert_data)
            candi_id = insert_result
        else:
            candi_id = candi_id_Array[0][0]
        single_result = {}
        single_result["acc_name"] = legit[j["Constituency Name"]]
        single_result["candidate"] = candi_id
        single_result["year"] = result_year
        single_result["type"] = "legit"
        if math.isnan(j[" Total Valid Votes"]):
            single_result['total'] = 0
        else:
            single_result['total'] = int(j[" Total Valid Votes"])
        candi_Array.append(single_result)
    return candi_Array

def handle_party(data):
    party_dict = {}
    for items in data:
        items_data = items.lower()
        items_data = dc.party_cleaner(items_data)

        sql_party_select_query = "SELECT party_id FROM party where party_name  = %s;"
        party_id_Array = utility.select_query(sql_party_select_query, (items_data,))
        if len(party_id_Array) == 0:
            insert_party_Query = "insert into party(party_name) values (%s)  RETURNING party_id;"
            insert_result = utility.insert_single(insert_party_Query,(items_data,))
            party_dict[items_data] = insert_result
        else:
            party_dict[items_data] = party_id_Array[0][0]
    return party_dict

def handle_legit(data,state):
    legit_dict = {}
    for items in data:
        legitData = (items,state,"legit")
        sql_leg_select_query = "SELECT legit_id FROM legit where legit_name = %s and state_id = %s and legit_type = %s;"
        legit_id_Array = utility.select_query(sql_leg_select_query,legitData)
        if len(legit_id_Array) == 0:
            insert_legit_Query = "insert into legit(legit_name,state_id,legit_type) values (%s,%s,%s)  RETURNING legit_id;"
            insert_result = utility.insert_single(insert_legit_Query,legitData)
            legit_dict[items] = insert_result
        else:
            legit_dict[items] = legit_id_Array[0][0]
    return legit_dict
def insert_data(data,type,state):

    df = pd.read_csv(data)
    file_name = os.path.basename(data)
    print(file_name)
    # extracting Year from fileName
    year_pattern = r'\d{4}'
    match = re.search(year_pattern,file_name)
    if match:
        file_year = match.group()
    else:
        raise ex("Year is not present in file name")
    state_name = state
    sql_state_select_query = "SELECT state_id FROM states where state_name = %s;"
    state_id_Array = utility.select_query(sql_state_select_query, (state_name,))
    state_id = None
    if len(state_id_Array) == 0:
        state_insert_query = "insert into states (state_name) values(%s) RETURNING state_id;"
        result = utility.insert_single(state_insert_query, (state_name,))
        state_id = result
    else:
        state_id = state_id_Array[0][0]
        # check_duplicate_data
    sql_check_data = "select c.state_id, a.res_id, a.res_legit_id, b.legit_id from result_data  as a inner join legit " \
                         "as b on a.res_legit_id = b.legit_id inner join states as c on b.state_id = c.state_id where a.res_year = %s and a.res_type = %s and c.state_id = %s"
    # sql_check_data = "SELECT res_id FROM result_data where res_legit_id = %s and res_year = %s and res_type = %s;"
    check_data = (file_year, type, state_id)
    sql_check_array = utility.select_query(sql_check_data, check_data)
    try:
        if len(sql_check_array) != 0:
            raise ex("An error occurred. Execution halted.")
        else:
            if file_year > '2030':
                # raise ex("code is not present in for file")
                df = df[df["STATE/UT NAME"] != 'TURN OUT']
                legit_data = df["AC NAME"].unique()
                legit_dict = handle_legit(legit_data, state_id)
                party_data = df["PARTY"].unique()
                party_dict = handle_party(party_data)

                candy_data = df[
                    ["AC NAME", "CANDIDATE NAME", "AGE", "SEX", 'CATEGORY',
                     'PARTY', 'TOTAL']]

                result_data = handle_old_candidate(candy_data, party_dict, legit_dict, file_year)
                print(result_data)
                values_tuple_list = [tuple(d.values()) for d in result_data]
                print(values_tuple_list)
                insert_result_query = "insert into result_data (res_legit_id,res_candi_id,res_year,res_type,res_total) values (%s,%s,%s,%s,%s)  RETURNING res_id;"
                utility.insertMany(insert_result_query, values_tuple_list)
                print(candy_data)
                print("final")

            else:
                if "STATE/UT NAME" in df :
                    df = df[df["STATE/UT NAME"] != 'TURN OUT']
                df = df.rename(columns={'AC NAME': 'Constituency Name'})
                df = df.rename(columns={'CANDIDATE NAME': 'Candidate Name'})
                df = df.rename(columns={'AGE': 'Candidate Age'})
                df = df.rename(columns={'SEX': "Candidate Sex"})
                df = df.rename(columns={'CATEGORY': 'Candidate Category'})
                df = df.rename(columns={'PARTY':  ' Party Name'})
                df = df.rename(columns={'TOTAL': ' Total Valid Votes'})
                legit_data = df['Constituency Name'].unique()
                legit_dict = handle_legit(legit_data, state_id)
                party_data = df[" Party Name"].unique()
                party_dict = handle_party(party_data)
                candy_data = df[
                    ["Constituency Name", "Candidate Name", "Candidate Age", "Candidate Sex", 'Candidate Category',
                     ' Party Name', ' Total Valid Votes']]
                result_data = handle_old_candidate(candy_data, party_dict, legit_dict, file_year)
                print(result_data)
                values_tuple_list = [tuple(d.values()) for d in result_data]
                print(values_tuple_list)
                insert_result_query = "insert into result_data (res_legit_id,res_candi_id,res_year,res_type,res_total) values (%s,%s,%s,%s,%s)  RETURNING res_id;"
                utility.insertMany(insert_result_query, values_tuple_list)

    except ex as e:
        print("Caught custom exception:", e)

if __name__ == '__main__':
    # insert_legis_data("Files/Legist/kerala_legi_2021.csv",2022,"legit")
    insert_data("Files/Legist/Karnataka_legit_2023.csv", "legit", 'karnataka')
    # insert_data("Files/Legist/kerala_legit_2016.csv",2016,"legit",'kerala')