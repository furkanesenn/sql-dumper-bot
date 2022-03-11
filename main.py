import os
import discord 
import datetime
from discord.ext import commands

token = "" #write discord bot token here
prefix = ''

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=prefix, intents=intents)

options = {
    'dbname': '', #database name
    'password': '123456789', #database pass
    'user': 'root', #database user
    'deleteafter': True #don't delete
}

def getSQLContent() -> str:
    current_path = os.path.dirname(os.path.realpath(__file__))
    expectedFilePath = current_path + r'\{}.sql'.format(options['dbname'])

    os.system('mysqldump --no-defaults -u {} -p{} {} > {}'.format(options['user'], options['password'], options['dbname'], expectedFilePath))

    with open(expectedFilePath, 'r') as sql_file:
        content = sql_file.read()


    strfed_date = getCurrentTimeStamp()
    return content, expectedFilePath, strfed_date

def getCurrentTimeStamp() -> str:
    now = datetime.datetime.now()
    return now.strftime('%d.%m.%Y | %H.%M')


@client.event
async def on_ready():
    print(f'The bot logged in as, {client.user}')

@client.event 
async def on_message(message):
    if message.content.startswith('gimmesql') and str(message.author.id) == '916435638977437746':
        await message.channel.send('{} isimli veritabanına ait yedek çıkarılıyor...'.format(options['dbname']), reference=message)
        sqlContent, filePath, date = getSQLContent()
        await message.author.send('{} tarihli, {} isimli veritabanı yedeğiniz'.format(date, options['dbname'], content=sqlContent), file=discord.File(filePath))
        await message.channel.send('Başarıyla SQL yedeği özelden iletildi!', reference=message)
        if options['deleteafter'] == True:
            os.remove(filePath)
        pass

client.run(token)
