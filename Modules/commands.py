import discord, json, re
from Modules import functions, data


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


async def derole(message):
    role = message.guild.get_role(data.gamejam)
    msg = await functions.send_embed(message.channel, "✋ Okay hang on!", "Attempting to remove gamejam participant role.")

    if role.members:
        fails = []

        for member in role.members:
            try:
                await member.remove_roles(role)
            except:
                fails.append("%s#%s" % (member.name, member.discriminator))
        else:
            if fails:
                await msg.edit(embed=discord.Embed(title="⚠️ Error removing gamejam particpant role from:", description="```{}```".format(fails), colour = 0x0094FF))
            else:
                await msg.edit(embed=discord.Embed(title="Success! 👍", description="All the gamejam participant roles have been removed.", colour = 0x0094FF))
    else:
        await msg.edit(embed=discord.Embed(title="⚠️ No one has the gamejam particpant role.", colour = 0x0094FF))


async def addpoints(message):
    args = await functions.get_arguments(message)
    
    if args:
        member = message.guild.get_member(int(re.findall(r"\d+", args[0])[0]))

        if member:
            if len(args) > 1 and args[1].isdigit():
                await functions.increase_count(member, "point", int(args[1]))
                await functions.send_embed(message.channel, "Success! 👍", "**{}** points have been added to **{}**".format(args[1], member))
            else:
                await functions.send_error(message.channel, "Please provide a valid amount.")
        else:
            await functions.send_error(message.channel, "Please provide a valid user.")