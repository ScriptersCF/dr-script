import math, datetime
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


async def process_auto_roles(new_points):
    if new_points < data.xp_roles[352799502379253772]: # No point in processing this if xp < 30
        return None
    
    #  Give highest role that satisfies: user xp >= xp_role
    role_id = list(filter(lambda x: (new_points >= data.xp_roles[x]), data.xp_roles))[-1] 

    # Handle special cases:
    if role_id == 352799502379253772: # Verified Lvl. 2
        joined_at = message.author.joined_at
        time_now = datetime.datetime.now()      

        if not time_now - joined_at >= datetime.timedelta(days = 3): # Award only if joined more than 3 days ago.
            return None
        
    elif role_id == 550880780776374296: # 100k+ Points
        await give_role(message, 639147821273972736) # Additionally give custom Gold role
        
    elif not role_id:
        return None
        
    # Handle all cases  
    return await give_role(message, role_id)


async def award_points(message):
    # Handle point awarding process.
    if not len(message.content) >= 10: # Check message length!
        return
    
    point_amount = 1 # Default at 1
    if message.channel.id in data.channel_points:
        point_amount = data.channel_points[message.channel.id] # Get points awarded by channel!

    # Increment points by <point_amount>
    old_points, new_points = await functions.increase_count(message.author, "point", point_amount)
    
    # Get user level based on points
    old_level = await functions.get_level_from_points(old_points)
    new_level = await functions.get_level_from_points(new_points)
    
    # Process auto-role
    new_role = None
    new_role = await process_auto_roles(new_points)
    
    # Process auto-level   
    if new_level > old_level or new_role:
        embed = await functions.get_user_embed(message.author, new_points, new_level > old_level, new_role)
        await message.channel.send(embed = embed)

        
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
