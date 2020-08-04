import discord, sqlite3, json, time
from Modules import data

async def send_embed(channel, title, description, *args):
    try:
        embed = discord.Embed(
            title = title,
            description = description,
            colour = 0x0094FF
        )
        if args:
            embed.set_image(url=args[0])
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
    # get amount of times that punishment has taken place and increase by 1
    current_amount = get_data(
        f"SELECT {column_type}s FROM scores WHERE userId = (?)",
        (str(target.id), )
    )[0] or 0

    set_data(
        f"UPDATE scores SET {column_type}s = (?) WHERE userId = (?)",
        (str(current_amount + amount), str(target.id))
    )

async def set_punish_time(target, punish_type, length, multiply):
    # set end_time to time that punishment should end
    end_time = int(time.time() + int(length) * multiply) if length != "∞" else 10 ^ 10
    current_data = get_data("SELECT * FROM Punishments WHERE userId = (?)", (str(target.id), ))

    # if user has no active punishments, add row to database
    if not current_data:
        set_data("INSERT INTO punishments (userId) VALUES (?)", (str(target.id), ))