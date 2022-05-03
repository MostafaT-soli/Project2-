#!/usr/bin/env python3
import sqlite3
from VAR import *
import requests
import time
import pandas as pd
###############################

def Get_D_ID(cursor,RenterAddress):

    sqlite_select_query = (f"SELECT Account,D_ID from scholar WHERE Wallet ='{RenterAddress}'")

    cursor.execute(sqlite_select_query)

    Result   =cursor.fetchall()[0]
    D_Account= Result[0]
    D_ID     = Result[1]

    return D_Account,D_ID

    #finally:
    #    if sqliteConnection:
    #        sqliteConnection.close()
    #        print("The SQLite connection is closed")                                          # fetch                                           # Fetch user ID for mention

def Check_Wallet(Schooler_W_ID):

    if (Schooler_W_ID[0] == '0') and (Schooler_W_ID[1] == 'x') and (len(Schooler_W_ID) == 42):

        Wallet = True

    else:

        Wallet = False

    return Wallet                                              # Check for Wallet Validty

def ADD_D_ID(Account,D_ID,RenterAddress):
    try:

        sqliteConnection = sqlite3.connect(f'{GUILD}.db')

        cursor = sqliteConnection.cursor()

        sqlite_replace_query = (f""" REPLACE INTO scholar (Account, D_ID ,Wallet)
VALUES('{Account}','{D_ID}','{RenterAddress}')""")
        cursor.execute(sqlite_replace_query)

        sqliteConnection.commit()

        cursor.close()

    except Exception as e:
        print(f'a7a le 7war {e}')

    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return Account,D_ID                                     # Register user

def Get_Schooler_Wallet_DB():

    sqliteConnection = sqlite3.connect(f'{GUILD}.db')

    cursor = sqliteConnection.cursor()

    sqlite_select_query = (f"SELECT Wallet from scholar")

    cursor.execute(sqlite_select_query)

    Result   =cursor.fetchall()

    Result_List = []

    for r in Result :

        Result_List.append(r[0])

    return Result_List                                                 # get all Wallets in DB

def Get_Schooler_Walle_PG():                                                    # get all Wallets from the Pegaxy

    Current_Schoolers   = []

    for Owner_ID in IDS:                                                          #   >>>> Add to Var file

        horse_list_request = requests.get(f'https://api-apollo.pegaxy.io/v1/pegas/owner/user/{Owner_ID}')

        horses_list = (horse_list_request.json())

        for horse_id in horses_list:

            RenterAddress = horse_id['renterAddress']

            Current_Schoolers.append(RenterAddress)

    return Current_Schoolers

def Get_Energy(cursor,Max_E):

    ######## Variabls #########

    Current_Unix_Time_H = int(time.time()/60/60)
    Pega_All ={}

    ###########################
    #########Multiple Wallets ########
    for Owner_ID in IDS:                                                          #   >>>> Add to Var file

        horse_list_request = requests.get(f'https://api-apollo.pegaxy.io/v1/pegas/owner/user/{Owner_ID}')

        horses_list = (horse_list_request.json())

        for horse_id in horses_list:

            Pega_ID = horse_id['id']
            Pega_All [Pega_ID] = {}
            #Pega_All [Pega_ID]['PRINT'] = False
            canRaceAt   =  int(horse_id['canRaceAt']/60/60)
            energy      = horse_id['energy']
            Can_Race    = canRaceAt - Current_Unix_Time_H

            if (energy >= Max_E) and ( Can_Race < 0)  :

                Pega_All [Pega_ID]['PRINT'] = True

                Pega_All[Pega_ID]['energy'] = horse_id['energy']

                Pega_All[Pega_ID]['ID']  = horse_id['id']

                Pega_All[Pega_ID]['totalRaces']  =  horse_id['totalRaces']

                Pega_All[Pega_ID]['Schooler']     =horse_id['lastRenterIsDirect']

                Pega_All[Pega_ID]['RenterAddress'] = horse_id['renterAddress']

                Pega_All[Pega_ID]['Wallet'] = Owner_ID

                Name = (horse_id['name'].encode(encoding="ascii",errors="ignore"))

                Pega_All[Pega_ID]['name'] = Name.decode("ascii")

                RenterAddress = horse_id['renterAddress']

                try:
                    Schooler_INFO = Get_D_ID(cursor,RenterAddress)
                    D_ID = Schooler_INFO[1]
                    D_Account = Schooler_INFO[0]
                    Pega_All[Pega_ID]['D_ID'] = (f'<@!{D_ID}>')
                    Pega_All[Pega_ID]['D_Account'] = D_Account
                except Exception as e:
                    print(f'{e}')
                    Pega_All[Pega_ID]['D_ID']       = 'needs to regsiter'
                    Pega_All[Pega_ID]['D_Account']  = 'needs to regsiter'

    return Pega_All

def Clean_DB(list_difference):

    sqliteConnection = sqlite3.connect(f'{GUILD}.db')

    cursor = sqliteConnection.cursor()

    try:
        for Old_Schooler in list_difference:

            sqlite_select_query = (f"DELETE FROM  scholar WHERE Wallet ='{Old_Schooler}' ")

            cursor.execute(sqlite_select_query)

            sqliteConnection.commit()

    except Exception as e:
            print(f'a7a le 7war {e}')
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def Check_Scholar(D_ID):

    sqliteConnection = sqlite3.connect(f'{GUILD}.db')

    cursor = sqliteConnection.cursor()

    try:

        sqlite_select_query = (f"SELECT Wallet from scholar WHERE D_ID ='{D_ID}'")

        cursor.execute(sqlite_select_query)

        Result   =cursor.fetchall()[0]

        Wallet = Result[0]

        Registered = True

    except Exception as e:

        print(f'a7a le 7war {e}')

        Wallet = 'NA'

        Registered = False

    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return  Registered , Wallet

def Check_CSV(CSV_File):

    Check_ALL = True

    True_List =['discord_account','polygon_wallet']

    Import_Data= pd.read_csv(CSV_File, encoding= 'unicode_escape')

    Data_List = list(Import_Data.columns)

    Check_List = all(item in Data_List for item in True_List)

    if Check_List == False:

        Check_ALL = False

    return Check_ALL

def scholar_Unregister(Account):

    sqliteConnection = sqlite3.connect(f'{GUILD}.db')

    cursor = sqliteConnection.cursor()

    try:
        sqlite_select_query = (f"DELETE FROM  scholar WHERE Account ='{Account}' ")

        cursor.execute(sqlite_select_query)

        sqliteConnection.commit()

    except Exception as e:
            print(f'a7a le 7war {e}')
    finally:
        if sqliteConnection:
            sqliteConnection.close()
