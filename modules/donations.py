from modules import data, functions
from json import loads
import discord

async def award_roles(user, amount, nitro_booster=False, send_message=True):
    awards = data.donation_awards
    perk_list = ""

    # for each award boundary, check if user has donated enough
    for boundary in list(awards.keys())[::-1]:
        if amount >= boundary and not nitro_booster:

            # set list of perks based on amount donated (for user dm)
            perk_list = "\n".join(f"- {perk}"
                for perk in awards[boundary]['awards'])

            # add roles that the user needs to be awarded
            for role in awards[boundary]["add"]:
                await user.add_roles(data.roles[role])
            
            # remove excess roles that the user no longer needs
            for role in awards[boundary]["remove"]:
                await user.remove_roles(data.roles[role])
            
            # exit for loop, as user has been awarded relevant roles
            break
    
    # if user has donated 5,000+ robux, check if they have custom colour
    if amount >= 5000 or nitro_booster:
        has_role = await functions.has_custom_colour(user)

        # if no custom colour, give default red custom colour
        if not has_role:
            await user.add_roles(data.roles[data.red_colour])

        # if no perk list exists, set the perk as "custom colour"
        if not perk_list:
            perk_list = "- Custom Colour"
    
    # prepare message to send to user
    thanks_message = discord.Embed(title="Hello!",
        description=data.donation_message.format(perk_list),
        colour=0x0094FF)
    
    # send user a thank you message if specified by variable
    if send_message:
        await user.send(embed=thanks_message)


async def remove_colours(user, added_roles):
    # get first colour that user has selected
    new_colour = added_roles[0]

    # for each role that's a colour, remove if not the new colour
    for role in user.roles:
        if role.name in data.colour_list and role != new_colour:
            await user.remove_roles(role)


async def remove_patron(user):
    # get total robux donated and current custom colour role
    _, _, _, robux_donated = functions.get_data(user.id)
    colour_role = await functions.has_custom_colour(user)

    # if user has custom colour and is no longer eligible, remove it
    if colour_role and robux_donated < 5000:
        if data.roles[data.nitro_booster] not in user.roles:
            await user.remove_roles(colour_role)

    # remove each donator role for a refresh
    for role in data.donator_roles:
        await user.remove_roles(data.roles[role])
        
    # re-award roles based on total robux donated
    await award_roles(user, robux_donated, send_message=False)

    # prepare message to send to user
    goodbye_message = discord.Embed(title="Sorry to see you go!",
        description=data.patron_removal_message, colour=0x0094FF)
    
    # send user a goodbye message
    await user.send(embed=goodbye_message)


async def remove_nitro(user):
    # get total robux donated and current custom colour role
    _, _, _, robux_donated = functions.get_data(user.id)
    colour_role = await functions.has_custom_colour(user)

    # check if user has custom colour, and is no longer eligble
    ineligible = (colour_role and robux_donated < 5000
        and data.roles[data.patron_plus] not in user.roles
        and data.roles[data.patron_plus_plus] not in user.award_roles)

    # if user is ineligible for custom role, remove it
    if ineligible:
        await user.remove_roles(colour_role)
    
    # prepare message to send to user
    goodbye_message = discord.Embed(title="Sorry to see you go!",
        description=data.nitro_removal_message, colour=0x0094FF)
    
    # send user a goodbye message
    await user.send(embed=goodbye_message)


async def handle_message(message):
    # if message is json, convert to dict and find user in server
    if message.content.startswith("{"):
        donation = loads(message.content)
        user = message.guild.get_member_named(donation["user"])

        # if user exists, get their data and add the donation
        if user:
            user_data = list(functions.get_data(user.id))
            user_data[3] += donation["spent"]

            # store the new donation amount in the database
            functions.handle_data("UPDATE scores SET robux = (?) WHERE userId = (?)",
                (str(user_data[3]), str(user.id)))
            
            # give relevant roles based on donation amount
            await award_roles(user, user_data[3])


async def handle_added_role(user, added_roles):
    # if user is nitro booster, temporarily award custom colour
    if data.roles[data.nitro_booster] in added_roles:
        await award_roles(user, 0, nitro_booster=True)
    
    # if user is patron, temporarily award 1,000 robux perks
    if data.roles[data.patron] in added_roles:
        await award_roles(user, 1000)
    
    # if user is patron+, temporarily award 5,000 robux perks
    if data.roles[data.patron_plus] in added_roles:
        await award_roles(user, 5000)
    
    # if user is patron++, temporarily award 10,000 robux perks
    if data.roles[data.patron_plus_plus] in added_roles:
        await award_roles(user, 10000)
    
    # if colour role added, remove other colour roles
    if any(role.name in data.colour_list for role in added_roles):
        await remove_colours(user, added_roles)


async def handle_removed_role(user, removed_roles):
    # if user is no longer nitro booster, attempt to remove custom colour
    if data.roles[data.nitro_booster] in removed_roles:
        await remove_nitro(user)

    # determine if any patron roles were removed
    patron_removed = any(data.roles[role] in removed_roles
        for role in data.patron_roles)
    
    # if patron was removed, call remove_patron function
    if patron_removed:
        await remove_patron(user)
