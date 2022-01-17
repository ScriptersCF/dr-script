prefix = "!"
bot_type = "R"
check_cooldown = 25

version = "Mr. Script 0.21" + bot_type
rich_presence = "www.scf.cx/bot"

token = "OTMyNDYxNjUwMDg1MjkwMDc0.YeTUlQ.wAppXmba6DCQlzWlVoD-K8tGgXo"
test_token = ""

regular = 932507980493103174
gold_role = 932508014706049096

muted = 932508026626265132
aban = 932508027599327332
shban = 932508027754524712

verified = 932508028345917490
verifiedlvl2 = 932508934458187786
forhire = 932508029344182392
notforhire = 932508029751021608
scripter = 932508030745059338
learner = 932508031349035008
gamejam = 932508031726526484

club10k = 932509049981911120
club20k = 932509070273945640
club50k = 932509103484469260
club100k = 932509122891505715

#donator = 323047035840233474
#donator_plus = 325937099557830656
#custom_gold = 639147821273972736

no_server = 932508223691452466
no_gamejam = 932508224102481931
no_event = 932508224723247164

general_channel = 932461442756653120
logs_channel = 932508689888342027
message_logs = 932508712889880626
#donation_channel = 473852097415086090

channel_points = {
    general_channel: 3,
    logs_channel: 0,
    message_logs: 0,
    932510713296085043: 3, # points
}

xp_roles = {
    verifiedlvl2: 30,
    regular: 2_000,
    club10k: 10_000,
    club20k: 20_000,
    club50k: 50_000,
    club100k: 100_000, # Also add 'Custom // Gold' role
}

color_list = {
    "Maroon",
    "Red",
    "Coral",
    "Brown",
    "Orange",
    "Wheat",
    "Gold",
    "Yellow",
    "Green",
    "Lime",
    "Cyan",
    "Blue",
    "Navy Blue",
    "Blurple",
    "Fuchsia",
    "Hot Pink",
    "Purple",
    "Plum",
    "Black",
    "Grey",
    "White"
}

command_aliases = {
    "help": "help",
    "cmds": "help",
    "commands": "help",
    "info": "help",

    "how": "how",

    #"changecolour": "changecolour",
    #"changecolor": "changecolour",
    #"colorlist": "colourlist",
    #"colourlist": "colourlist",

    "toggle": "toggle",

    "forhire": "forhire",
    "for_hire": "forhire",
    
    "notforhire": "notforhire",
    "not_for_hire": "norforhire",
    
    "scripter": "scripter",
    "learner": "learner",

    #"rank": "stats",
    #"statistics": "stats",
    #"ranking": "stats",

    "kick": "kick",
    "mute": "mute",
    "ban": "ban",
    "aban": "aban",
    "shban": "shban",
    "unmute": "unmute",
    "lock": "lock",
    "unlock": "unlock",
    "clear": "clear",
    "report": "report",
    "derole": "derole",
    "addpoints": "addpoints",

    "stats": "stats",
    "points": "stats",
    "level": "stats"
}

punishment_names = {
    1: "mute",
    2: "aBan",
    3: "shBan"
}

punishment_roles = {
    "mute": muted,
    "aBan": aban,
    "shBan": shban
}

welcome_message = """Welcome to ScriptersCF, one of the leading scripting servers on Discord with over 7,000 members!

By joining our server, you represent that you have read and agreed to our [rules](https://github.com/ScriptersCF/server-rules/blob/master/README.md).

Additionally, you are giving us explicit permission to store information including messages, message count, moderation history and anything else that we deem appropriate.

This allows us to moderate effectively or implement certain bot functions, contains no personally identifable information and will not be shared with or sold to any external parties.

*Note: The invite link below will expire in 10 minutes.*"""

join_message = """**[Click here](https://discord.com/invite/{0}) to rejoin the server.**"""

help_message = """`!help` - Displays general help for the Mr. Script bot.
`g:help` - Displays help for the Gamer bot used in <#715562907294761040>.

**Commands**
`!stats @user OR <num>` - Displays the user's stats.
`!leaderboard` - Displays the top 10 most active server members.
`!report @user <reason>` - Reports a user for breaking our rules.
`!roll 5d3` - Rolls 5 3-sided dice.
`!rolldie` - Rolls a standard 6-sided die.

**Roles**
`!forhire` - Gives you the `For Hire` role.
`!notforhire` - Gives you the `Not For Hire` role.
`!scripter` - Gives you the `Scripter` role.
`!learner` - Gives you the `Learner` role.

**Scripting**
🎮 Look through our [open-source games](https://discordapp.com/channels/306153640023031820/543874721603911690).
<:Lua:735536158741757969> Read the [Lua PIL guide](https://cdn.discordapp.com/attachments/306156119519264770/575829412235313172/Programming_in_Lua_5.1.pdf).
<:Studio:735548957639311380> Take a look at the [Roblox Wiki](https://developer.roblox.com).
<:YouTube:735534954145906688> Check out our [YouTube tutorials](https://youtube.com/scripterscf). *(Coming Soon)*

**Miscellaneous**
<:Script:735535206995460198> View our [rules](https://discordapp.com/channels/306153640023031820/306155109203836928).
<:Roblox:735535578191364197> Support us on [Roblox](https://www.roblox.com/games/960878638/Donate).
<:Patreon:735535762178703390> Support us on [Patreon](https://patreon.com/ScriptersCF).
<:Twitter:735526455806656595> Follow [@ScriptersCF](https://twitter.com/ScriptersCF) on Twitter.
"""

hammers = ["🔨","🛠️","⚒️","⛏️","⚔️","⛏","🛠","⚒"]
