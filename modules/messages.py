from modules import functions, data
from datetime import datetime, timedelta, timezone

async def process_auto_roles(message, new_points):
    member = message.author

    # if user has verified role, remove it
    if data.roles[data.verified] in member.roles:
        await member.remove_roles(data.roles[data.verified])

        # if user doesn't have verified II role, add it and congratulate
        if data.roles[data.verified2] not in member.roles:
            await member.add_roles(data.roles[data.verified2])
            await message.channel.send(data.roleup_message.format(
                member.id, data.roles[data.verified2].name))
    
    # find the highest role that the user qualifies for
    for points in list(data.points_needed.keys())[::-1]:
        if new_points >= points:
            role = data.roles[data.points_needed[points]]

            # if user doesn't have the role, award it
            if role not in member.roles:
                await member.add_roles(role)
                await message.channel.send(data.roleup_message.format(
                    member.id, role.name))
            
            # remove any lower roles that the user has
            for lower_points in data.points_needed:
                if lower_points < new_points and points != lower_points:
                    role = data.roles[data.points_needed[lower_points]]
                    if role in member.roles:
                        await member.remove_roles(role)

            
            # break out of loop, as user has been awarded highest role
            break


async def award_points(message):
    # if message isn't significant, ignore it
    if len(message.content) < 10:
        return
    
    # determine amount of points to award, based on channel
    point_increment = 1

    # if channel has a custom point increment, use that instead
    if message.channel.id in data.channel_points:
        point_increment = data.channel_points[message.channel.id]
    
    # if user has 2x xp role, double the points
    if data.roles[data.double_xp] in message.author.roles:
        point_increment *= 2
    
    # get current user data and new point count
    user_id, points, _, _ = functions.get_data(message.author.id)
    new_points = points + point_increment

    # get previous level and new level
    old_level = 1 + int(0.3 * (int(points) ** 0.5))
    new_level = 1 + int(0.3 * (int(new_points) ** 0.5))

    # if user has leveled up, send congrats message
    if new_level > old_level:
        await message.channel.send(data.rankup_message.format(user_id, new_level))
    
    # update user's points in database
    functions.handle_data("UPDATE scores SET points = (?) WHERE userId = (?)",
        (str(new_points), str(user_id)))
    
    # get user join & current time
    joined_at = message.author.joined_at
    time_now = datetime.now(timezone.utc)

    # if user has 30+ points & joined over 3 days ago, check for role upgrades
    if new_points >= 30:
        if time_now - joined_at >= timedelta(days = 3):
            await process_auto_roles(message, new_points)


async def award_help_message(message):
    # if message isn't significant, ignore it
    if len(message.content) < 10:
        return

    # if the message is sent by the author of the post, ignore it
    if message.author.id == message.channel.owner_id:
        return

    # get user's data and new help messages count
    user_id, _, _, _, help_msgs = functions.get_data(message.author.id)
    new_help_msgs = help_msgs + 1

    # update user's help messages count in database
    functions.handle_data("UPDATE scores SET helpMsgs = (?) WHERE userId = (?)",
        (str(new_help_msgs), str(user_id)))
