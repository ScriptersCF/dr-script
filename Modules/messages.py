import json
from Modules import functions, data
from time import time

last_check_time = 0

# check_punishments unfinished
async def check_punishments(guild):
    # iterate through each punishment, ignore if no expiration
    for user in functions.get_data("SELECT * FROM punishments", ()):
        user_id = user[0]
        for punishment in range(1, 4):
            if not user[punishment]:
                continue
            
            # if expired, replace punishment expiration
            try:
                if int(time()) >= float(user[punishment]):
                    punish_type = data.punishment_names[punishment]
                    functions.set_data(
                        f"UPDATE punishments SET {punish_type + 'End'} = NULL WHERE userId = (?)",
                        (user_id, )
                    )

                    # find user, get associated role, remove and dm user
                    target = guild.get_member(int(user_id))
                    role = guild.get_role(data.punishment_roles[punish_type])
                    await target.remove_roles(role)
                    await functions.send_embed(
                        target,
                        "ScriptersCF",
                        f"Your **{punish_type}** has expired at ScriptersCF."
                    )
            except:
                0
                
            
        # if user has no active punishments, remove row from database
        if not any(user[1:]):
            functions.set_data(
                "DELETE FROM punishments WHERE userId = (?)",
                (user_id, )
            )


async def award_points(message):
    point_amount = 1

    # check message length and get points for channel
    if len(message.content) >= 10:
        if message.channel.id in data.channel_points:
            point_amount = data.channel_points[message.channel.id]

        # update db
        await functions.increase_count(message.author, "point", point_amount)


async def clear(message):
    # set amount of messages to delete with cap of 100, + message from mod
    arguments = await functions.get_arguments(message)
    messages_to_delete = min(100, max(0, int(arguments[0])))

    # purge and log
    await message.channel.purge(limit=messages_to_delete + 1)
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "Clear",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Amount:** {str(messages_to_delete)}
        **Channel:** <#{str(message.channel.id)}>"""
    )


async def stats(message):
    # get user's current stats to display
    user_data = functions.get_data(
        f"SELECT * FROM scores WHERE userId = (?)",
        (str(message.author.id), )
    )

    # format user's stats
    await functions.send_embed(
        message.channel,
        "Stats",
        f"""**User:** <@{message.author.id}>
        **Level:** {user_data[2]}
        **Points:** {user_data[1]}"""
    )

async def handle(message):
    global last_check_time

    await award_points(message)

    # if 15 seconds has passed since last message, call funcs + reset
    current_time = int(time())
    if current_time >= last_check_time + data.check_cooldown:
        last_check_time = current_time
        await check_punishments(message.guild)

async def check_donation(message):
    data = json.loads(message.content.split("\n")[0])
    amount = data["amount"]

    # match sent user with each member in server
    async for member in message.guild.fetch_members():
        if member.name + "#" + member.discriminator == data["user"]:
            await functions.donation(member, amount)