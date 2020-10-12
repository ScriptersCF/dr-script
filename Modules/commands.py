import discord, json, requests, io, datetime
from Modules import functions, data
from PIL import Image

def execute(Type, Command):
    Database = sqlite3.connect("scores.sqlite")
    Cursor = Database.cursor()
    Cursor.execute(Command)
    if Type == "Get":
        AllData = Cursor.fetchall()
        Database.close()
        return AllData
    elif Type == "Set":
        Database.commit()
        Database.close()

async def stats(Message, Args):
    User = Message.author
    try:
        if Args[0][:2] == "<@":
            User = Message.mentions[0]
        elif Args[0].isdigit():
            if int(Args[0]) < 1000000:
                User = await GetUserFromRank(int(Args[0]))
            else:
                User = server.get_member(Args[0])
    except Exception as e:
        print("5",e)
    Data = Execute(
        "Get",
        "SELECT * FROM scores WHERE userId = \"" + User.id + "\""
    )
    JoinDate = "30 May 2017" if User.id == "356836476777922562" else User.joined_at.strftime('%d %b %Y')
    await SendLevelMsg(
        User,
        Message.channel,
        "Stats",
        "**User**: <@" + User.id + """>
**Level**: """ + str(Data[0][2]) + """
**Points**: """ + str(Data[0][1]) + """
**Rank**: """ + str(await GetRank(User)) + """
**Joined**: """ + JoinDate + "\n**Staff Member** ✔️\n" * (await GetLevel(User) >= 4)
    )


async def help(message):
    # send user the help message
    await functions.send_embed(message.author, "Help", data.help_message)


async def forhire(message):
    # remove "not for hire" role if the user has it
    opposite_role = message.guild.get_role(data.notforhire)
    if opposite_role in message.author.roles:
        await message.author.remove_roles(opposite_role)
    
    # give the user the "for hire" role and give thumbs up reaction
    role = message.guild.get_role(data.forhire)
    await message.author.add_roles(role)
    await message.add_reaction("👍")


async def notforhire(message):
    # remove "for hire" role if the user has it
    opposite_role = message.guild.get_role(data.forhire)
    if opposite_role in message.author.roles:
        await message.author.remove_roles(opposite_role)
    
    # give the user the "not for hire" role and give thumbs up reaction
    role = message.guild.get_role(data.notforhire)
    await message.author.add_roles(role)
    await message.add_reaction("👍")


async def scripter(message):
    # remove "learner" role if the user has it
    opposite_role = message.guild.get_role(data.learner)
    if opposite_role in message.author.roles:
        await message.author.remove_roles(opposite_role)
    
    # give the user the "scripter" role and give thumbs up reaction
    role = message.guild.get_role(data.scripter)
    await message.author.add_roles(role)
    await message.add_reaction("👍")


async def learner(message):
    # remove "scripter" role if the user has it
    opposite_role = message.guild.get_role(data.scripter)
    if opposite_role in message.author.roles:
        await message.author.remove_roles(opposite_role)
    
    # give the user the "learner" role and give thumbs up reaction
    role = message.guild.get_role(data.learner)
    await message.author.add_roles(role)
    await message.add_reaction("👍")


async def toggle(message):
    role = (await functions.get_arguments(message))[0]

    # toggle associated role if found
    if "server" in role: await functions.toggle_role(message, data.no_server)
    elif "event" in role: await functions.toggle_role(message, data.no_event)
    elif "game" in role or "gj" in role: await functions.toggle_role(message, data.no_gamejam)
    
    # otherwise, show error
    else:
        await functions.send_error(message.channel, "Role not found")


async def lock(message):
    channel = message.channel
    role = message.guild.get_role(data.verified)
    await channel.set_permissions(role, send_messages=False)


async def unlock(message):
    channel = message.channel
    role = message.guild.get_role(data.verified)
    await channel.set_permissions(role, send_messages=True)


async def colourlist(message):
    await functions.send_embed(
        message.author,
        "Colour List",
        "",
        "https://cdn.discordapp.com/attachments/306153640023031820/740004654368424066/unknown.png"
    )

# taken from https://note.nkmk.me/en/python-pillow-add-margin-expand-canvas/
def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

async def generate_latex(message):
    # predefine URL, including the default DPI for the image and the background color to be white
    url = 'https://latex.codecogs.com/gif.latex?\\dpi{{500}}\\bg_white\\{}'

    # parses the message, removes the initial command
    equation = message.content.replace('!latex ', '')

    await message.channel.send('Processing your request: {}'.format(equation))

    # requests the LaTeX to be generated, in stream mode
    r = requests.get(url.format(equation), stream=True)
    
    # check if status_code of request was not 200, if it is not, an error occurred
    if r.status_code != 200:
        if r.status_code == 400:
            await message.channel.send('Error while requesting LaTeX file. Status code: {} \nPlease check formatting of equation and try again.'.format(r.status_code)) 
        else:
            await message.channel.send('Error while requesting LaTeX file. Status code {}'.format(r.status_code)) 
        return

    # take the binary content of the request and put it into a bytes object   
    bytes = io.BytesIO(r.content)

    # open the bytes as a PIL Image object to add margins
    img = Image.open(bytes)
    new_img = add_margin(img, 10, 30, 10, 30, (255,255,255))

    # turn updated PIL Image object back to bytes
    new_bytes = io.BytesIO()
    new_img.save(new_bytes, 'PNG')
    new_bytes.seek(0)

    # create discord.File object in .png format
    file = discord.File(new_bytes, (str(datetime.datetime.now()) + '.png' ))

    # send image in channel
    await message.channel.send(file=file)
    

async def changecolor(message):
    arguments = await functions.get_arguments(message)
    if not arguments:
        await colourlist(message)
        return

    color = arguments[0].lower()
    if not color in data.color_list:
        await functions.send_error(message.channel, "That is not a valid colour.")
        return

    roles = message.author.roles

    for role in roles:
        if "Custom //" in role.name:
            for newrole in message.guild.roles:
                if newrole.name.lower() == "custom // " + color:
                    try:
                        await role.delete(reason="Changing Colour")
                        await message.author.add_roles(newrole)
                        await functions.send_embed(message.channel, "Success! 👍", "Your custom colour has successfully been changed.")
                    except:
                        await functions.send_error(message.channel, "An error occurred, try again later.")
                        return False
