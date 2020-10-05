from Modules import functions, data

# size of punishments.py needs to be reduced, a lot is repeated

async def mute(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return
    
    failure_count = 0
    targets = []
    reason = "No reason provided."
    length = "∞"

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])
        
        # if not target, update length if found and set reason
        else:
            if argument.isdigit():
                length = argument
            break
        
        reason = " ".join(arguments[len(targets)+1:]) or reason
    
    # iterate through targets, ignore user if moderator
    for target in targets:
        try:
            await functions.setup_data(target)
            for role in target.roles:
                if role.name == "Moderator":
                    raise Exception("user is moderator")
            
            # increase user's mute count, set length if not inf and dm user
            await functions.increase_count(target, "mute", 1)
            await functions.set_punish_time(target, "mute", length, 60)
            await functions.send_embed(
                target, "ScriptersCF",
                f"You have been **muted** in ScriptersCF for **{length} minutes** for the following reason: ```{reason}```"
            )

            # give user muted role
            role = message.guild.get_role(data.muted)
            await target.add_roles(role)
        
            # otherwise, increase failure count to warn moderator
        except:
            failure_count += 1
    
    # log kicked targets + reason in logs channel
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "Mute",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Length:** """ + str(length) + """ minutes
        **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
        **Reason:** """ + reason
    )

    # tell user whether successful or not
    if failure_count == 0:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not muted.")


async def kick(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return
    
    failure_count = 0
    targets = []
    reason = "No reason provided."

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])
        
        # if not target, update reason and stop iterating
        else:
            reason = " ".join(arguments[len(targets):])
            break
    
    # iterate through targets, ignore user if moderator
    for target in targets:
        try:
            await functions.setup_data(target)
            for role in target.roles:
                if role.name == "Moderator":
                    raise Exception("user is moderator")
            
            # increase user's kick count, dm user and kick
            await functions.increase_count(target, "kick", 1)
            await functions.send_embed(
                target,
                "ScriptersCF",
                f"You have been **kicked** from ScriptersCF for the following reason: ```{reason}```"
            )
            await target.kick(reason = reason)
        except:
            failure_count += 1
    
    # log kicked targets + reason in logs channel
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "Kick",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
        **Reason:** """ + reason
    )

    # tell user whether successful or not
    if failure_count == 0:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not kicked.")


async def ban(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return
    
    failure_count = 0
    targets = []
    reason = "No reason provided."

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])
        
        # if not target, update reason and stop iterating
        else:
            reason = " ".join(arguments[len(targets):])
            break
    
    # iterate through targets, ignore user if moderator
    for target in targets:
        try:
            await functions.setup_data(target)
            for role in target.roles:
                if role.name == "Moderator":
                    raise Exception("user is moderator")
            
            # increase user's ban count, dm user and ban
            await functions.increase_count(target, "ban", 1)
            await functions.send_embed(
                target,
                "ScriptersCF",
                f"You have been **banned** from ScriptersCF for the following reason: ```{reason}```"
                + "If you feel you have been banned by mistake, please appeal [here](https://forms.gle/Rzd4QvLJYyo3BkQg6)."
            )
            await target.ban(reason = reason)
        except:
            failure_count += 1
    
    # log banned targets + reason in logs channel
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "Ban",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
        **Reason:** """ + reason
    )

    # tell user whether successful or not
    if failure_count == 0:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not banned.")

async def shunban(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return
    
    failure_count = 0
    targets = []

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])
        
    # iterate through targets, ignore user if moderator
    for target in targets:
        try:
            await functions.setup_data(target)
            
            # increase user's aban count, set length if not inf and dm user
           # await functions.set_punish_time(target, "aban", length, 0)
            await functions.send_embed(
                target, "ScriptersCF",
                f"You have been **unbanned from Selling and Hiring** in ScriptersCF"
            )

            # remove user's aban role
            role = message.guild.get_role(data.shban)
            await target.remove_roles(role)        
        # otherwise, increase failure count to warn moderator
        except:
            failure_count += 1
    
    # log kicked targets + reason in logs channel
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "Selling and Hiring Unban",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
        """
    )

    # tell user whether successful or not
    if failure_count == 0:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not unbanned from Selling and Hiring.")

async def shban(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return
    
    failure_count = 0
    targets = []
    reason = "No reason provided."
    length = "∞"

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])
        
        # if not target, update length if found and set reason
        else:
            if argument.isdigit():
                length = argument
            break
        
        reason = " ".join(arguments[len(targets)+1:]) or reason
    
    # iterate through targets, ignore user if moderator
    for target in targets:
        try:
            await functions.setup_data(target)
            for role in target.roles:
                if role.name == "Moderator":
                    raise Exception("user is moderator")
            
            # increase user's shban count, set length if not inf and dm user
            await functions.increase_count(target, "shban", 1)
            await functions.set_punish_time(target, "shban", length, 86400)
            await functions.send_embed(
                target, "ScriptersCF",
                f"You have been **banned from selling & hiring** in ScriptersCF for **{length} days** for the following reason: ```{reason}```"
            )

            # give user shban role
            role = message.guild.get_role(data.shban)
            await target.add_roles(role)
        
        # otherwise, increase failure count to warn moderator
        except:
            failure_count += 1
    
    # log kicked targets + reason in logs channel
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "S&H Ban",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Length:** """ + str(length) + """ days
        **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
        **Reason:** """ + reason
    )

    # tell user whether successful or not
    if failure_count == 0:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not banned from selling & hiring.")

async def aunban(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return
    
    failure_count = 0
    targets = []

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])
        
    # iterate through targets, ignore user if moderator
    for target in targets:
        try:
            await functions.setup_data(target)
            
            # increase user's aban count, set length if not inf and dm user
           # await functions.set_punish_time(target, "aban", length, 1)
            await functions.send_embed(
                target, "ScriptersCF",
                f"You have been **unbanned from academics channels** in ScriptersCF"
            )

            # remove user's aban role
            role = message.guild.get_role(data.aban)
            await target.remove_roles(role)        
        # otherwise, increase failure count to warn moderator
        except:
            failure_count += 1
    
    # log kicked targets + reason in logs channel
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "Academics Unban",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
        """
    )

    # tell user whether successful or not
    if failure_count == 0:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not unbanned from Academics.")

async def aban(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return
    
    failure_count = 0
    targets = []
    reason = "No reason provided."
    length = "∞"

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])
        
        # if not target, update length if found and set reason
        else:
            if argument.isdigit():
                length = argument
            break
        
        reason = " ".join(arguments[len(targets)+1:]) or reason
    
    # iterate through targets, ignore user if moderator
    for target in targets:
        try:
            await functions.setup_data(target)
            for role in target.roles:
                if role.name == "Moderator":
                    raise Exception("user is moderator")
            
            # increase user's aban count, set length if not inf and dm user
            await functions.increase_count(target, "aban", 1)
            await functions.set_punish_time(target, "aban", length, 86400)
            await functions.send_embed(
                target, "ScriptersCF",
                f"You have been **banned from academics channels** in ScriptersCF for **{length} days** for the following reason: ```{reason}```"
            )

            # give user aban role
            role = message.guild.get_role(data.aban)
            await target.add_roles(role)
        
        # otherwise, increase failure count to warn moderator
        except:
            failure_count += 1
    
    # log kicked targets + reason in logs channel
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "Academics Ban",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Length:** """ + str(length) + """ days
        **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
        **Reason:** """ + reason
    )

    # tell user whether successful or not
    if failure_count == 0:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not banned from Academics.")


async def unmute(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return
    
    failure_count = 0
    targets = []

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])
    
    # iterate through targets, send direct messages, increase data and mute
    for target in targets:
        try:
            await functions.setup_data(target)
            await functions.send_embed(
                target,
                "ScriptersCF",
                f"You have been **unmuted** in ScriptersCF."
            )
            role = message.guild.get_role(data.muted)
            await target.remove_roles(role)
        except:
            failure_count += 1
    
    # log kicked targets + reason in logs channel
    await functions.send_embed(
        message.guild.get_channel(data.logs_channel),
        "Unmute",
        f"""**Moderator:** <@{str(message.author.id)}>
        **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets])
    )

    # tell user whether successful or not
    if failure_count == 0:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not unmuted.")


async def report(message):
    # get arguments, stop function if none are found
    arguments = await functions.get_arguments(message)
    if not arguments:
        return

    failure_count = 0
    self_report = False
    targets = []
    reason = "No reason provided."

    # check for targets and add to list
    for argument in arguments:
        if argument.startswith("<@"):
            targets.append(message.mentions[len(targets)])

        # if not target, update reason and stop iterating
        else:
            reason = " ".join(arguments[len(targets):])
            break

    # iterate through targets, ignore user if moderator
    for target in targets:
        try:
            await functions.setup_data(target)
            for role in target.roles:
                if role.name == "Moderator":
                    raise Exception("user is moderator")

            if target.id == message.author.id:
                raise Exception("self report")
            
        except:
            failure_count += 1

    # log kicked targets + reason in logs channel
    if failure_count == 0:
        await functions.send_embed(
            message.guild.get_channel(data.logs_channel),
            "Report",
            f"""**Plaintiff:** <@{str(message.author.id)}>
            **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
            **Reason:** """ + reason
        )
    else:
        await functions.send_embed(
            message.guild.get_channel(data.logs_channel),
            "Attempted Report",
            f"""**Plaintiff:** <@{str(message.author.id)}>
            **Targets:** """ + ", ".join([f"<@{target.id}>" for target in targets]) + """
            **Reason:** """ + reason
        )
        
    # tell user whether successful or not
    if failure_count == 0 and not self_report:
        await message.add_reaction("👍")
    else:
        await functions.send_error(message.channel, f"{str(failure_count)} user was not reported.")
