#!/usr/bin/env python3
##########Custom################
#from utils import Get_Energy
from VAR import *
from utils import Get_D_ID , Check_Wallet ,ADD_D_ID, Get_Energy, Check_Scholar,Get_Schooler_Wallet_DB,Get_Schooler_Walle_PG, Clean_DB, Check_CSV, scholar_Unregister
#########Python3#################
import argparse
import sqlite3
import requests
import pandas as pd
###########Discord###############
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option , create_choice


# Create Arguments

parser = argparse.ArgumentParser()

#parser.add_argument('-PGX', type=float, help='Set the PGX price if bought in a dip')

parser.add_argument('-E', type=int, required=True, help='Minimum Energy' )

args = parser.parse_args()

Max_E = args.E


#####################Slash command intodcution############################

intents = discord.Intents.default()

intents.members = True

client = commands.Bot(command_prefix='!',intents=intents)

slash = SlashCommand(client , sync_commands=True)

######################Just on ready##############################
@client.event
async def on_ready():
    change_status.start()
    print('bot in active')

#####################################################

@slash.slash(name = 'Energy' , description="Check the Energy Manually" , guild_ids=[GUILD_ID])   #   >>>> Add to Var file

async def Energy(ctx:SlashContext):
################For Bot to WAit #####################
    await ctx.defer()
################Variabls for Bot ###################
    channel = client.get_channel(CHANNEL_ID)                                        #   >>>> Add to Var file
    channel_id = int(CHANNEL_ID)
    Masseg_ID = ctx.channel.id                                                      #   >>>> Add to Var file
    Empty_Response = True                                                           # for Empty Response
################Bot not the same author###################

    if ctx.author == client.user:
        return
###############Actual Command ##########################
    if  (Masseg_ID == channel_id) :                                                  # check if it's on the Mangers Channel

        await channel.send(f'''```yaml
Manual Energy Check Started```''')
        await channel.send(f'''```bash
Checking for Pegas above "{Max_E}" Energy```''')
        try:
            sqliteConnection = sqlite3.connect(f'{GUILD}.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

        except sqlite3.Error as error:

            print("Failed to read data from sqlite table", error)

        PRINT = Get_Energy(cursor,Max_E)

        for PEGA_ID in PRINT.keys():

            if PRINT[PEGA_ID] :

                Empty_Response = False
                await channel.send(f'''**Pega ID**               :{PEGA_ID}
**Name**                   :{PRINT[PEGA_ID]['name']}
**Scholar**                :{PRINT[PEGA_ID]['D_ID']}
**Wallet**                  :{PRINT[PEGA_ID]['Wallet']}
**Rent Address**   :{PRINT[PEGA_ID]['RenterAddress']}
**Energy**                  :{PRINT[PEGA_ID]['energy']}
**URL**                       :https://play.pegaxy.io/my-assets/pega/{PEGA_ID}
===================================================$''')

    if sqliteConnection:
        sqliteConnection.close()

    if Empty_Response == True :
        await channel.send(f'''```bash
All pegas are below  "{Max_E}" Energy
```''')

    await ctx.send (f'''**Bot is Running**''')

@slash.slash(
    name = 'Automatic_Scholars_unregister' ,
    description="Automatically unregister all the scholars that does not have a Pega" ,
    guild_ids=[GUILD_ID])

async def Clean(ctx:SlashContext):

################Variabls for Bot ###################
    channel             = client.get_channel(CHANNEL_ID)                                        #   >>>> Add to Var file
    channel_id          = int(CHANNEL_ID)
    Masseg_ID           = ctx.channel.id                                                                  # Scholers empty list
################Variabls for Bot ###################
    if  (Masseg_ID == channel_id) :
        await ctx.defer()

        await channel.send(f'''```yaml
Cleaning OLD Scholers Started ```''')

        Schooler_Wallet_DB = Get_Schooler_Wallet_DB()

        Schooler_Wallet_PG =  Get_Schooler_Walle_PG()

        set_difference     = set(Schooler_Wallet_DB) - set(Schooler_Wallet_PG)

        list_difference    = list(set_difference)

        Clean_DB(list_difference)

    await ctx.send (f'''**Bot is Running**''')

@slash.slash(
    name = 'Scholar_Register' ,
    description="Register Scholar Manually " ,
    guild_ids=[GUILD_ID] ,
    options=[create_option(name='option1',description='Add Scholar Account', option_type= 6 ,required = True),
  create_option(name='option2',description='Add Scholar Wallet', option_type= 3 ,required = True)])#   >>>> Add to Var file

async def Manual_Register(ctx, option1,option2):
    ################Variabls for Bot ###################
    channel             = client.get_channel(CHANNEL_ID)                                        #   >>>> Add to Var file
    channel_id          = int(CHANNEL_ID)
    Masseg_ID           = ctx.channel.id
    D_ID                = str(option1.id)
    Account             = str(option1)
    ################Variabls for Bot ###################
    if  (Masseg_ID == channel_id) :

        await ctx.defer()

        RenterAddress = str(option2)
        Wallet_True   = Check_Wallet(RenterAddress)


        if Wallet_True == True :

            try:
                print("Connected to SQLite")
                print(f'Daccount : {Account},ID : {D_ID},Wallet:{RenterAddress}')
                Schooler_INFO = ADD_D_ID(Account,D_ID,RenterAddress)
                await channel.send(f'''```bash
"{Account}" have Registered successfully with Wallet ID : "{RenterAddress}" ```''')
            except Exception as error:

                print("Failed to read data from sqlite table", error)

                await channel.send(f'''Bot Is Busy Please try Againe later ''')

        else:

            await channel.send(f'''```bash
Registration Failed ,Please Enter a Valid Wallet ID
This was not a valid entry : "{RenterAddress}"```''')

        await ctx.send (f'''**Bot is Running**''')


@slash.slash(
    name = 'scholar_Check' ,
    description="Check if the scholar is registered" ,
    guild_ids=[GUILD_ID] ,
    options=[create_option(name='option',description='Scholar Account', option_type= 6 ,required = True)])#   >>>> Add to Var file

async def Manual_Register(ctx, option):
    ################Variabls for Bot ###################
    channel             = client.get_channel(CHANNEL_ID)                                        #   >>>> Add to Var file
    channel_id          = int(CHANNEL_ID)
    Masseg_ID           = ctx.channel.id
    D_ID                = str(option.id)
    Account             = str(option)
    ################Variabls for Bot ###################
    if  (Masseg_ID == channel_id) :

        check = Check_Scholar(D_ID)

        if check[0] == True :

            await channel.send(f'''```bash
Scholar  : "{Account}" is regsitred with Wallet : "{check[1]}"
```''')

        else :

            await channel.send(f'''```bash
Scholar  : "{Account}" needs to regsiter
```''')

    await ctx.send (f'''**Bot is Running**''')

@tasks.loop(seconds=TIME)                                                                       # Time in seconds >>>> Add to Var file
async def change_status():

################Variabls for Bot ###################
    channel = client.get_channel(CHANNEL_ID)                                        #   >>>> Add to Var file
    channel_id = int(CHANNEL_ID)                                                  #   >>>> Add to Var file
    Empty_Response = True                                                           # for Empty Response
###############Actual Command ##########################                                                # check if it's on the Mangers Channel

    await channel.send(f'''```yaml
Automatic Energy Check Started```''')
    await channel.send(f'''```bash
Checking for Pegas above "{Max_E}" Energy```''')

    try:
        sqliteConnection = sqlite3.connect(f'{GUILD}.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

    except sqlite3.Error as error:

        print("Failed to read data from sqlite table", error)

    PRINT = Get_Energy(cursor,Max_E)

    for PEGA_ID in PRINT.keys():

        if PRINT[PEGA_ID] :
            Empty_Response = False
            await channel.send(f'''**Pega ID**               :{PEGA_ID}
**Name**                   :{PRINT[PEGA_ID]['name']}
**Scholar**                :{PRINT[PEGA_ID]['D_ID']}
**Wallet**                  :{PRINT[PEGA_ID]['Wallet']}
**Rent Address**   :{PRINT[PEGA_ID]['RenterAddress']}
**Energy**                  :{PRINT[PEGA_ID]['energy']}
**URL**                       :https://play.pegaxy.io/my-assets/pega/{PEGA_ID}
===================================================$''')

    if sqliteConnection:
        sqliteConnection.close()

    if Empty_Response == True :
        await channel.send(f'''```bash
All pegas are below  "{Max_E}" Energy
```''')

    await channel.send('**This is All Horses for now**')                                                   # get from VAR file

@slash.slash(
    name = 'Import_Bulk_Scholars' ,
    description="Import Bulk Scholars by uploading the CSV file" ,
    guild_ids=[GUILD_ID] )

async def Import_Bulk_Schoolars(ctx:SlashContext):
    channel             = client.get_channel(CHANNEL_ID)                                        #   >>>> Add to Var file
    channel_id          = int(CHANNEL_ID)
    guild = client.get_guild(GUILD_ID)
    Masseg_ID           = ctx.channel.id
####################################################

    if  (Masseg_ID == channel_id) :

        await ctx.defer()

        await channel.send(f'''`Please Upload your CSV file in your next Message `''')

        M = await client.wait_for('message', check=lambda message: message.author == ctx.author)

        if M.attachments:

            await channel.send(f'''`Checking the File Uploded  `''')

            await M.attachments[0].save(f'{GUILD}.csv')

            CSV_True = Check_CSV(f'{GUILD}.csv')

            if CSV_True == True :

                Failed_IMPORTS = {}

                Import_Data= pd.read_csv(f'{GUILD}.csv', encoding= 'unicode_escape')

                Total_Scholers = len(Import_Data)
                Total_Failed_IMPORTS = 0

                for index, row in Import_Data.iterrows():

                    Full_D_Account = Import_Data.discord_account[index]

                    RenterAddress = Import_Data.polygon_wallet[index]

                    Wallet_True   = Check_Wallet(RenterAddress)

                    if Wallet_True == False :
                        print('Not a valid wallet')

                        Failed_IMPORTS[Full_D_Account] = {}
                        Failed_IMPORTS[Full_D_Account]['Account'] = Full_D_Account
                        Failed_IMPORTS[Full_D_Account]['Wallet'] = RenterAddress
                        Total_Failed_IMPORTS += 1

                        continue

                    try:
                        Split_D_Account = Full_D_Account.split('#')
                        D_name = Split_D_Account[0]
                        D_discriminator = Split_D_Account[1]
                        print(f'{D_name}{D_discriminator}')

                        D_ID = (discord.utils.get(guild.members, name=D_name, discriminator=D_discriminator)).id

                    except Exception as e :

                        print(f'user could not be found{e}')

                        Failed_IMPORTS[Full_D_Account] = {}
                        Failed_IMPORTS[Full_D_Account]['Account'] = Full_D_Account
                        Failed_IMPORTS[Full_D_Account]['Wallet'] = RenterAddress
                        Total_Failed_IMPORTS += 1

                        continue

                    ADD_D_ID(Full_D_Account,D_ID,RenterAddress)

                Total_Scholers_Registered = Total_Scholers - Total_Failed_IMPORTS

                await channel.send(f'''```bash
"{Total_Scholers_Registered}" out of "{Total_Scholers}" has been successfully Registered```''')

                if Failed_IMPORTS :
                    await channel.send(f'''```bash
Below Users Has Failed to Register .
Please Make sure that they are apart of your Guild and they have a valid Polygon Wallet```''')

                    for Failed_IMPORT in Failed_IMPORTS:
                        await channel.send(f'''```bash
User:"{Failed_IMPORTS[Failed_IMPORT]['Account']}" .
Wallet:"{Failed_IMPORTS[Failed_IMPORT]['Wallet']}" ```''')

                #await ctx.send(f'''**Bot is Running**''')

            else :

                await channel.send(f'''```bash
CSV check Failed .
Kindly make sure that the file in the correct format.
Also make sure that it contains both headers "discord_account" and  "polygon_wallet" ```''')

        else :
            await channel.send(f'''`Upload CSV file failed No Attachments were Detected`''')
            await ctx.send(f'''**Bot is Running**''')
            return

    await ctx.send(f'''**Bot is Running**''')

@slash.slash(
    name = 'scholar_Unregister' ,
    description="Unregister Manully a single scholar" ,
    guild_ids=[GUILD_ID] ,
    options=[create_option(name='option',description='Scholar Account', option_type= 6 ,required = True)])#   >>>> Add to Var file

async def Unregister(ctx, option):
    ################Variabls for Bot ###################
    channel             = client.get_channel(CHANNEL_ID)                                        #   >>>> Add to Var file
    channel_id          = int(CHANNEL_ID)
    Masseg_ID           = ctx.channel.id
    D_ID                = str(option.id)
    Account             = str(option)
    ################Variabls for Bot ###################
    if  (Masseg_ID == channel_id) :

        check = Check_Scholar(D_ID)

        if check[0] == True :

            await channel.send(f'''```bash
Scholar  : "{Account}" is regsitred with Wallet : "{check[1]}"
```''')
            scholar_Unregister(Account)

            await channel.send(f'''```bash
Scholar  : "{Account}" is  Unregistered successfully"
```''')


        else :

            await channel.send(f'''```bash
Scholar  : "{Account}" Is not Registered to be able to delete
```''')

    await ctx.send (f'''**Bot is Running**''')

@slash.slash(
    name = 'Help' ,
    description="Display how to use Commands in the Bot " ,
    guild_ids=[GUILD_ID])

async def Help(ctx:SlashContext):

################Variabls for Bot ###################
    channel             = client.get_channel(CHANNEL_ID)                                        #   >>>> Add to Var file
    channel_id          = int(CHANNEL_ID)
    Masseg_ID           = ctx.channel.id                                                                  # Scholers empty list
################Variabls for Bot ###################
    if  (Masseg_ID == channel_id) :

        await channel.send(f'''```bash
Command List :-

1 - "/energy"                        : Energy Command will trigger the energy check manually
2 - "/scholar_Register"              : Register a single scholar manually
3 - "/scholar_Check"                 : Check wither or not the schooler is registered
4 - "/scholar_Unregister"            : Unregister a single scholar
5 - "/import_Bulk_Scholars"          : import scholars in a bulk by using a CSV file (CSV template can be found on our PEGATO server )
6 - "/automatic_Scholars_unregister" : Automatically delete all old scholars that are registered and dose not have a pega
```''')
    await ctx.send (f'''**Bot is Running**''')

client.run(TOKEN)
