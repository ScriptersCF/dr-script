import discord, sqlite3, json, time
from Modules import data

async def send_embed(channel, title, description):
    try:
        embed = discord.Embed(
            title = title,
            description = description,
            colour = 0x0094FF
        )
        #embed.set_footer(text = data.version + " for ScriptersCF | !help")
        return await channel.send(embed = embed)
    except:
        return False


async def send_error(channel, error):
    await send_embed(
        channel,
        f"⚠️ {error}",
        ""
    )


def set_data(command, args):
    # open db, execute, save and close
    database = sqlite3.connect("scores.sqlite")
    cursor = database.cursor()
    cursor.execute(command, args)
    database.commit()
    database.close()


def get_data(command, args):
    # open db, execute, fetch response and close
    database = sqlite3.connect("scores.sqlite")
    cursor = database.cursor()
    cursor.execute(command, args)
    all_data = cursor.fetchall()
    database.close()

    # if data is in useless list, remove list
    if all_data:
        if len(all_data) == 1 and isinstance(all_data, list):
            return all_data[0]
    
    return all_data


def remove_from_list(main_list, remove_list):
    # iterates through all values to remove and removes if found
    for value in remove_list:
        if value in main_list:
            main_list.remove(value)
    return main_list


def remove_tags(message):
    # remove important tags from message to prevent abuse
    message = message.replace("@everyone", "everyone").replace("@here", "here")
    for word in message.split():
        if "@&" in word:
            message = message.replace(word, "@redacted-role")
    return message


async def setup_data(user):
    # if data doesn't exist, give user default amount of points
    existing_data = get_data("SELECT * FROM scores WHERE userId = (?)", (user.id,))
    if not existing_data:
        set_data(
            "INSERT INTO scores (userId, points, level) VALUES ((?), (?), (?))",
            (str(user.id), 1, 1)
        )


async def is_staff(user):
    # iterate through user's roles, if user has mod then return true
    for role in user.roles:
        if role.name == "Moderator":
            return True


async def is_verified(user):
    # iterate through user's roles, if user has verified role then return true
    for role in user.roles:
        if role.name == "Verified":
            return True


async def get_arguments(message):
    # check message arguments, return error if none given
    arguments = message.content.split()[1:]
    if not arguments:
        await send_error(message.channel, "Missing Arguments")
    return arguments


async def toggle_role(message, role_id):
    # if user has role, remove, otherwise add the role and react
    role = message.guild.get_role(role_id)
    if role in message.author.roles:
        await message.author.remove_roles(role)
    else:
        await message.author.add_roles(role)
    await message.add_reaction("👍")


async def increase_count(target, column_type, amount):
    # get amount of times that data has taken place and increase by <amount>
    #sql gross LOL who did this XD
    old_amount = get_data(
        f"SELECT {column_type}s FROM scores WHERE userId = (?)",
        (str(target.id), )
    )[0] or 0
 
    set_data(
        f"UPDATE scores SET {column_type}s = (?) WHERE userId = (?)",
        (str(old_amount + amount), str(target.id))
    )
    
    new_amount = str(old_amount + amount)
    return old_amount, new_amount


async def set_punish_time(target, punish_type, length, multiply):
    # set end_time to time that punishment should end
    end_time = int(time.time() + int(length) * multiply) if length != "∞" else 10 ** 10
    current_data = get_data("SELECT * FROM punishments WHERE userId = (?)", (str(taprget.id), ))

    # if user has no active punishments, add row to database
    if not current_data:
        set_data("INSERT INTO punishments (userId) VALUES (?)", (str(target.id), ))
    
    # set punishment expiration time accordingly
    set_data(
        f"UPDATE punishments SET {punish_type}End = (?) WHERE userId = (?)",
        (str(end_time), str(target.id))
    )
    
    
async def give_role(message, role_id): # This is different from toggle_role()
    role = message.guild.get_role(role_id)
    if role in message.author.roles:
        await message.author.add_roles(role)
        return True
    
    
async def get_level_from_points(user_points):
    return 1 + (math.floor(0.3 * math.sqrt(user_points)))


async def get_player_embed(user, xp):
    user_and_discriminator = user.name + "#" + user.discriminator
    user_avatar = user.avatar_url
    
    level = 1 + (math.floor(0.3 * math.sqrt(xp)))
    next_level = level + 1

    next_xp = ((level)/0.3)**2
    percentage_xp = xp/next_xp
    
    emojis = ""
    for i in range(10):
        if i < math.floor(percentage_xp * 10):
            emojis += :white_large_square
        else:
            emojis += :black_large_square:                   
                
    for i in range(1, math.floor(percentage*10) + 1):
        emojis += :white_large_square:

    for i in range(1, 10 - math.floor(percentage*10) + 1):
        emojis += :black_large_square:

    embed = discord.Embed(
        colour = discord.Colour(0x76adf1),
        description = emojis
    )

    embed.set_author(name = user_and_discriminator, icon_url = user_avatar)
    embed.set_thumbnail(url = user_avatar)
    embed.add_field(name = "**Level**", value = level, inline = True)
    embed.add_field(name = "**Points**", value = f"{xp}/{next_xp} XP" inline = True)
    
    return embed
