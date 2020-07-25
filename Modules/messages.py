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
            if int(time()) >= int(user[punishment]):
                punish_type = data.punishment_names[punishment]
                functions.set_data(
                    f"UPDATE punishments SET {punish_type + 'End'} = NULL WHERE userId = (?)",
                    (user_id, )
                )

                # find user, get associated role, remove and dm user
                target = guild.get_member(int(user_id))
                role = guild.get_role(data.punishment_roles[punish_type])
                target.remove_roles(role)
                await functions.send_embed(
                    target,
                    "ScriptersCF",
                    f"Your **{punish_type}** has expired at ScriptersCF."
                )
                
            
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


async def handle(message):
    global last_check_time

    await award_points(message)

    # if 15 seconds has passed since last message, call funcs + reset
    current_time = int(time())
    if current_time >= last_check_time + 15:
        last_check_time = current_time
        #await check_punishments(message.guild)