import discord, json
from Modules import functions, data

async def help(message):
    # send user the help message
    await functions.send_embed(message.author, "Help", data.help_message)
    
async def how(message):
    # lmgtfy
    
    args = await functions.get_arguments(message)
    if not args:
        return
    args = " ".join(args)

    # I don't want people abusing this, so let's add some guards:

    if len(args) > 100:
        await functions.send_error(message.channel, "Query too long! Max: 100 characters")
        return
  
    # Creating a google search query link lol
    new_string = args.replace(" ", "+")
    query = f"https://www.google.com/search?&q=how+{new_string}"

    # Handling embed
    embed = discord.Embed(
        title = "How " + args,
        colour=discord.Colour(0x76adf1),
        url=query,
        description=f"Don't worry, it's really easy to do that! **[Click here]({query})** to see how.\n\n_Powered by Google:tm:_"
    )
    embed.set_thumbnail(
        url="https://cdn3.iconfinder.com/data/icons/google-suits-1/32/1_google_search_logo_engine_service_suits-512.png"
    )

    # Posting to channel and adding reaction
    await message.channel.send(content=f"Here is the answer for your question:\n{query}", embed=embed)
    await message.add_reaction("<:surprisedPikachu:533297579048304660>")

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
                await msg.edit(embed=discord.Embed(title="⚠️ Error removing gamejam participant role from:", description="```{}```".format(fails), colour = 0x0094FF))
            else:
                await msg.edit(embed=discord.Embed(title="Success! 👍", description="All the gamejam participant roles have been removed.", colour = 0x0094FF))
    else:
        await msg.edit(embed=discord.Embed(title="⚠️ No one has the gamejam participant role.", colour = 0x0094FF))

# I love Josh,
# from fly.
