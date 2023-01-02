### CONFIG - Feel free to change these values when testing the bot.

### REQUIRED, used to get guild object in on_ready
server_id = 1058183380254081205

### IMPORTANT, it is recommended to set to False if testing
# setting to False prevents points and ranks from being updated
award_points = True

### IMPORTANT, it is recommended to set to False if testing
# setting to False prevents helpful messages from being updated
award_help_message = True

# optional, you can leave this as is
version = "Dr. Script 1.0"
rich_presence = "scf.cx/bot"
prefix = "-" # general commands should use slash commands instead

# channel ids used in the server
# if you aren't testing this, you can leave this as is
messages_channel = 1046253977785864284
general = 306153640023031820
mod_logs = 332883332528603146

# channel that new joins and donations are sent to
# if you aren't testing this, you can leave this as is
joins_and_donations = 473852097415086090

# forum where users ask questions
help_forum = 1059300803145375834

# ids of channels with specific points earned per message (or defaults to 1)
# if you aren't testing this, you can leave this as is
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

# ids of roles in the server
# if you aren't testing this, you can leave this as is
verified = 346604542550605835
verified2 = 352799502379253772

regular = 322102125402259456
regular2 = 642852174854094868
regular3 = 642852176628285455
regular4 = 642852191606013963
regular5 = 550880780776374296

donator = 323047035840233474
donator_plus = 325937099557830656

patron = 332203969331986432
patron_plus = 642852166943637514
patron_plus_plus = 332217316693770260

nitro_booster = 585533734548406305
double_xp = 1044338857988075581
red_colour = 359352595233374208

staff_role = 1044304663073280061
shban_role = 416786636118949918
aban_role = 550114698297737216

patron_roles = [patron, patron_plus, patron_plus_plus]
donator_roles = [donator, donator_plus, double_xp]

# gets filled with actual discord.Role values at startup
# if you aren't testing this, you can leave this as is
# otherwise, you should add any new role ids to this list
roles = {
    verified: None,
    verified2: None,
    regular: None,
    regular2: None,
    regular3: None,
    regular4: None,
    regular5: None,
    donator: None,
    donator_plus: None,
    patron: None,
    patron_plus: None,
    patron_plus_plus: None,
    nitro_booster: None,
    double_xp: None,
    red_colour: None,
    staff_role: None,
    shban_role: None,
    aban_role: None
}

# xp points needed to reach each role
# if you aren't testing this, you can leave this as is
points_needed = {
    2000: regular,
    10000: regular2,
    20000: regular3,
    50000: regular4,
    100000: regular5
}

# list of donation amounts and their corresponding rewards
# if you aren't testing this, you can leave this as is
donation_awards = {
    100: {"add": [donator], "remove": [],
        "awards": ["Donator Role"]},

    1000: {"add": [donator_plus], "remove": [donator],
        "awards": ["Donator+ Role"]},

    5000: {"add": [donator_plus], "remove": [donator],
        "awards": ["Donator+ Role", "Custom Colour Access"]},

    10000: {"add": [donator_plus, double_xp], "remove": [donator],
        "awards": ["Donator+ Role", "Custom Colour Access", "2x Chat XP"]}
}

# list of available custom colour names
# if you aren't testing this, you can leave this as is
colour_list = {
    "Maroon", "Red", "Fire", "Coral", "Orange",
    "Brown", "Gold", "Yellow", "Seafoam", "Lime",
    "Green", "Teal", "Cyan", "Sky", "Blue",
    "Navy", "Purple", "Pink", "Hot Pink", "White"
}

### END OF CONFIG
# variables below this line are extraneous strings used in the bot

donation_message = """**Thank you very much** for your donation! :partying_face:

**You currently have access to the following perks:**
{0}

*If there are any issues, please contact a member of staff.*"""

welcome_message = """👋 Welcome to ScriptersCF, one of the leading scripting servers on Discord with over 7,500 members!
<:YouTube:735534954145906688> If you're looking to get into scripting, check out our [scripting tutorials](https://www.youtube.com/playlist?list=PLug2rYd8OSsV1fUEPM1C-PBg64jkZS5J0).

By joining our server, you represent that you have read and agreed to our [rules](https://github.com/ScriptersCF/server-rules/blob/master/README.md).

*Note: The invite link below will expire in 10 minutes.*"""

patron_removal_message = """Unfortunately, your Patreon perks have expired, but thank you for helping to support us for the duration of your subscription! :heart:

Your perks have been updated based on previous donations. If there are any issues, be sure to contact a member of staff so we can help.

If you would like to continue supporting us in the future, you can do so [via our Patreon page here](https://www.patreon.com/scripterscf)."""

nitro_removal_message = """Unfortunately, your Nitro Booster perks have expired, but thank you for helping to support us for the duration of your subscription! :heart:

Your perks have been updated based on previous donations. If there are any issues, be sure to contact a member of staff so we can help.

If you would like to continue supporting us in the future, feel free to boost our server again!"""

welcome_title = "Welcome to ScriptersCF :wave:"
welcome_message = """**Here's what you're about to have access to...**
:question: *Use our **scripting help** forum for free, 24/7*
:handshake: *Trade your services in our **selling & hiring** channels*
:video_game: *Join us for **game jam** events with huge prizes*

**New to scripting?** We recommend the following resources:
<:YouTube:735534954145906688> Our go-to series: [youtube.com/jotslo](https://youtube.com/jotslo)
:notebook_with_decorative_cover: Roblox Engine API: [create.roblox.com/docs](https://create.roblox.com/docs/reference/engine)
<:Studio:735548957639311380> Developer Forum: [devforum.roblox.com](https://devforum.roblox.com)

**How do I join?**
Simply head over to <#886612569601769512>, select your roles & verify :white_check_mark:
"""

joined_message = "Welcome to the community, <@{0}>! :wave:"

rankup_message = "Congratulations, <@{0}>! You have reached level **{1}**!"
roleup_message = "Congratulations, <@{0}>! You have received **{1}**!"

default_avatar = "https://cdn.discordapp.com/embed/avatars/0.png"
points_icon = "https://joshl.io/img/points.png"
