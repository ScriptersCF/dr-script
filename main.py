import discord
from discord import app_commands
from modules import *
from math import ceil
from typing import Optional

SERVER = discord.Object(id=data.server_id)

class MyClient(discord.Client):
    # when initialised, set intents & generate app commands
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    # when the bot is ready, make cmds available in the server
    async def setup_hook(self):
        self.tree.copy_global_to(guild=SERVER)
        await self.tree.sync(guild=SERVER)


# declare intents, enabling members & messages
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

# start client
client = MyClient(intents=intents)

# define points command, and listen for its usage
@client.tree.command()
@app_commands.describe(user="The user to get points for")
async def points(interaction: discord.Interaction, user: Optional[discord.Member] = None):
    # get user data for reference (specified user or author)
    user = user or interaction.user
    user_id, points, _, _ = functions.get_data(user.id)

    # get level and points needed for next level
    level = 1 + int(0.3 * (int(points) ** 0.5))
    needed_points = ceil(((level)/0.3)**2)

    # create embed & put username into proper format
    response = discord.Embed(colour=0x0094FF)
    username = f"{user.name}#{user.discriminator}"

    # add extra fields to embed
    icon = user.avatar.url if user.avatar else data.default_avatar
    response.set_author(name=username, icon_url=icon)
    response.set_thumbnail(url=data.points_icon)
    response.add_field(name="Level", value=f"**{level}**", inline=True)
    response.add_field(name="Points", value=f"**{points}**/{needed_points}", inline=True)

    # respond with embed message 
    await interaction.response.send_message(embed=response)


@client.event
async def on_message(message):
    # if message is a potential donation, handle it
    if message.channel.id == data.joins_and_donations:
        await donations.handle_message(message)
    
    # if message is a moderation command, handle it
    if message.content.startswith(data.prefix):
        await moderation.handle_command(message)
    
    # if awarding points is enabled & not from bot, award points
    if data.award_points and not message.author.bot:
        await messages.award_points(message)


@client.event
async def on_message_edit(before, after):
    # if log channel doesn't exist, ignore
    if not data.messages_channel:
        return

    # if message content is the same, ignore
    if before.content == after.content:
        return
    
    # otherwise, get user data and create embed
    user = after.author
    response = discord.Embed(colour=0xFFA500)
    username = f"{user.name}#{user.discriminator}"

    # add extra fields to embed
    icon = user.avatar.url if user.avatar else data.default_avatar
    response.set_author(name=username, icon_url=icon)
    response.add_field(name="Channel", value=f"<#{before.channel.id}>", inline=False)
    response.add_field(name="Original Message", value=before.content, inline=False)
    response.add_field(name="Edited Message", value=after.content, inline=False)

    # send edited message in message log channel
    await data.messages_channel.send(embed=response)


@client.event
async def on_message_delete(message):
    # if log channel doesn't exist, ignore
    if not data.messages_channel:
        return

    # get user data and create embed
    user = message.author
    response = discord.Embed(colour=0xFF0000)
    username = f"{user.name}#{user.discriminator}"

    # add extra fields to embed
    icon = user.avatar.url if user.avatar else data.default_avatar
    response.set_author(name=username, icon_url=icon)
    response.add_field(name="Channel", value=f"<#{message.channel.id}>", inline=False)
    response.add_field(name="Deleted Message", value=message.content, inline=False)

    # send deleted message in message log channel
    await data.messages_channel.send(embed=response)


@client.event
async def on_member_update(before, after):
    # if roles haven't been changed, ignore
    if before.roles == after.roles:
        return
    
    # get lists of changed roles
    added_roles = list(set(after.roles) - set(before.roles))
    removed_roles = list(set(before.roles) - set(after.roles))

    # if roles have been added...
    if added_roles:
        # if verified role was added, send welcome message
        if data.roles[data.verified] in added_roles and data.general:
            await data.general.send(data.joined_message.format(after.id))

        # otherwise, check if relevant donation role was added
        else:
            await donations.handle_added_role(after, added_roles)
    
    # if roles have been removed, check if relevant donation role was removed
    if removed_roles:
        await donations.handle_removed_role(after, removed_roles)


@client.event
async def on_member_join(member):
    # when a member joins, create embed
    welcome_dm = discord.Embed(title=data.welcome_title,
        description=data.welcome_message,
        colour=0x0094FF)
    
    # send embed to member
    await member.send(embed=welcome_dm)


@client.event
async def on_ready():
    # when the bot is ready, assign guild variable
    # and populate channel variables based on id
    guild = client.get_guild(data.server_id)
    data.messages_channel = guild.get_channel(data.messages_channel)
    data.general = guild.get_channel(data.general)
    data.mod_logs = guild.get_channel(data.mod_logs)

    # populate roles dictionary with role objects
    for role_id in data.roles:
        role = guild.get_role(role_id)
        data.roles[role_id] = role
    
    # set bot status
    await client.change_presence(activity = discord.Game(name = data.rich_presence))


# start bot with bot's token
# use your own bot token by modifying token.py
client.run(token.value)