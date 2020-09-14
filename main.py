import discord, asyncio, aiohttp, sqlite3, json, requests, csv, time
from discord import Webhook, RequestsWebhookAdapter
client = discord.Client()

from Modules import *
private_invites = {}

command_list = {
    "help": {"run": commands.help, "requirement": ["Verified"]},

    "toggle": {"run": commands.toggle, "requirement": ["Verified"]},
    "forhire": {"run": commands.forhire, "requirement": ["Verified"]},
    "notforhire": {"run": commands.notforhire, "requirement": ["Verified"]},
    "scripter": {"run": commands.scripter, "requirement": ["Verified"]},
    "learner": {"run": commands.learner, "requirement": ["Verified"]},

    "mute": {"run": punishments.mute, "requirement": ["Moderator", "Trial Moderator"]},
    "kick": {"run": punishments.kick, "requirement": ["Moderator"]},
    "ban": {"run": punishments.ban, "requirement": ["Administrator", "Senior Moderator"]},
    "aban": {"run": punishments.aban, "requirement": ["Moderator"]},
    "shban": {"run": punishments.shban, "requirement": ["Moderator"]},
    "unmute": {"run": punishments.unmute, "requirement": ["Moderator"]},
    "clear": {"run": messages.clear, "requirement": ["Moderator"]},
    "report": {"run": punishments.report, "requirement": ["Verified"]},

    #fun commands
    "roll": {"run": commands.roll, "requirement": ["Verified"]},
    "rolldie": {"run": commands.rolldie, "requirement": ["Verified"]}
}


async def interpret_command(message):
    # check if command exists & get proper command name
    inputted_command = message.content.lower().split()[0]

    for name in data.command_aliases:
        if name == inputted_command[len(data.prefix):]:
            command = data.command_aliases[name]
            command_data = command_list[command]
            
            # iterate through user's roles and check if role requirement met
            for role in message.author.roles:
                if role.name in command_data["requirement"]:
                    await command_data["run"](message)
                    return True


async def generate_invite(member):
    global private_invites

    # otherwise, generate private invite to #general for user for verification, dm, kick and log
    try:
        general = member.guild.get_channel(data.general_channel)
        invite = await general.create_invite(
            max_age = 600,
            max_uses = 1,
            unique = True,
            reason = f"Private invite for {member.name}."
        )
        await functions.send_embed(member, "Welcome!", data.welcome_message)
        await functions.send_embed(member, "", data.join_message.format(invite.code))
        await member.kick(reason = f"Private invite code '{invite.code}' has been sent.")
        private_invites[member.id] = {"invite": invite, "timeout": time.time() + 600}

        # wait 10 minutes and reset dictionary if still found
        await asyncio.wait(600)
        if member.id in private_invites:
            del private_invites[member.id]
            
    # in case of error, kick user regardless to protect server
    except Exception as error:
        await member.kick(reason = f"Kicked due to error: {error}")


@client.event
async def on_message(message):
    # if not in server or user is bot, ignore
    if message.author.bot or not message.guild:
        return
    
    # if user is not verified, start verif process
    if message.content and not await functions.is_verified(message.author):
        await generate_invite(message.author)
        await message.delete()
        return
    
    # setup user data if it doesn't already exist
    await functions.setup_data(message.author)
    
    # interpret command if starts with prefix
    if message.content.startswith(data.prefix):
        command_exists = await interpret_command(message)
        if not command_exists:
            await functions.send_embed(
                message.channel,
                "⚠️ Unknown Command",
                "If this is a real command, please try again in a few days."
            )
    
    # check message for spam, award points and such
    await messages.handle(message)


@client.event
async def on_member_update(before, after):
    # check if user is staff member, toggle hammer accordingly
    try:
        if await functions.is_staff(after):
            if "🔨" not in after.nick:
                await after.edit(nick = after.nick + " 🔨")
        else:
            for hammer in data.hammers:
                if hammer in after.nick:
                    await after.edit(
                        nick = after.nick.replace(hammer, "")
                            or "Unnamed"
                    )
    except:
        0


@client.event
async def on_member_join(member):
    global private_invites

    # check if user has verified via dm, let in & setup data if legitimate, else kick
    if member.id in private_invites:
        invites = await member.guild.invites()
        if private_invites[member.id]["invite"] not in invites:
            del private_invites[member.id]
            role = member.guild.get_role(data.verified)
            await member.add_roles(role)
            await functions.setup_data(member)
        else:
            await member.kick(reason = "User didn't join with private invite.")
        return

    await generate_invite(member)


@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = data.rich_presence))


# determine which bot token to use & start bot
if data.bot_type == "T": # beta
    client.run(data.test_token)
elif data.bot_type == "R": # release
    client.run(data.token)