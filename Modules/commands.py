import discord, json
from Modules import functions, data
import random, math


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


async def roll(message):
    Max = 100
    arguments = message.content.split() #not using the arguments function, cuz if there are no arguments, let it roll 1-100
    if len(arguments) >= 2:
        try:
            int(arguments[1])
            Max = int(arguments[1])
        except ValueError:
            Max = Max
    await message.channel.send(message.author.mention+", you rolled "+str(math.ceil(random.random()*Max))+" points!")


async def rolldie(message):
    await message.channel.send(message.author.mention + ", you rolled " + str(math.ceil(random.random() * 6)) + " points!")


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