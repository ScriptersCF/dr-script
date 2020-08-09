prefix = "!"
bot_type = "T"

version = "Mr. Script 0.1" + bot_type
rich_presence = "www.scf.cx/bot"

token = ""
test_token = ""

muted = 335171382428303360
aban = 550114698297737216
shban = 416786636118949918

verified = 346604542550605835
forhire = 374610760032321537
notforhire = 374610878940708864
scripter = 308611398672318475
learner = 391938933841199104

no_server = 676921838181548083
no_gamejam = 678974586951565312
no_event = 676921944880185365

general_channel = 306153640023031820
logs_channel = 332883332528603146

channel_points = {
    349255881977757696: 0,
    639942887152549899: 0,
    692166689403437090: 0,
    692166854914867230: 0,
    692165904947216414: 0,
    692166816830586920: 0,
    306156119519264770: 2,
    462394160629153812: 2,
    699995169629667370: 2,
    379023623245004810: 2,
    306885827189800960: 3,
    351182527316099072: 3,
    372506961171841025: 3,
    639153031619018752: 3
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
    
    "changecolour": "changecolour",
    "changecolor": "changecolour",
    "colorlist": "colourlist",
    "colourlist": "colourlist",

    "toggle": "toggle",

    "forhire": "forhire",
    "for_hire": "forhire",
    
    "notforhire": "notforhire",
    "not_for_hire": "norforhire",
    
    "scripter": "scripter",
    "learner": "learner",

    "kick": "kick",
    "mute": "mute",
    "ban": "ban",
    "aban": "aban",
    "shban": "shban",
    "unmute": "unmute",
    "lock": "lock",
    "unlock": "unlock",
    "clear": "clear",
    "report": "report"
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
