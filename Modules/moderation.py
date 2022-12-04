from modules import data

# extended moderation commands that can be used by staff members
async def shban(user, target):
    await target.add_roles(data.roles[data.shban_role])
    await data.mod_logs.send(f"{user.mention} S&H banned {target.mention}.")

async def shunban(user, target):
    await target.remove_roles(data.roles[data.shban_role])
    await data.mod_logs.send(f"{user.mention} S&H unbanned {target.mention}.")

async def aban(user, target):
    await target.add_roles(data.roles[data.aban_role])
    await data.mod_logs.send(f"{user.mention} academic banned {target.mention}.")

async def aunban(user, target):
    await target.remove_roles(data.roles[data.aban_role])
    await data.mod_logs.send(f"{user.mention} academic unbanned {target.mention}.")


# list of commands and their functions
command_list = {
    "shban": shban,
    "shunban": shunban,
    "aban": aban,
    "aunban": aunban,
}


async def handle_command(message):
    user = message.author

    # if user is not a staff member, ignore command
    if data.roles[data.staff_role] not in user.roles:
        return
    
    # if message doesn't mention a user, ignore command
    if not message.mentions:
        return
    
    # if target is a staff member, ignore command
    target = message.mentions[0]
    if data.roles[data.staff_role] in target.roles:
        return
    
    # if command is in command list, execute it
    for command in command_list:
        if message.content.startswith(data.prefix + command):
            await command_list[command](user, target)