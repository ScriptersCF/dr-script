# :warning: These guidelines are outdated, please come back later.

______
Thank you in advance to those that choose to help us with our bot. Users that send in accepted pull requests will be rewarded with the `Open Source Dev` role in our [Discord server](https://discord.gg/N9GRpSC) if interested.

________

**Important:** When testing the bot, it is easiest to give it **Administrator** permissions. You will also need to change `general_channel` and `verified` in `data.py` to a test channel ID and test role that you need to have assigned to you, otherwise the bot will throw an error due to our invite-based verification process.

_________

We don't currently have too many rules for contributions, but we ask that you follow these to make things as easy for us as possible.
- Please provide a title and description with your pull request so we can understand exactly what your contribution does and why it should be accepted.
- All contributions should use snake_case in consistency with the rest of the project
- Please ensure that any IDs changed for testing purposes have been changed back to the original IDs so that it is easier for us to merge both projects.
- If possible, please write comments where necessary in your code so that it is easier for people to understand.
- Pull requests to fix typos/grammar mistakes are accepted, extremely minor changes that make no difference to the repository are not and will be marked as spam.
- Responses from the bot should be consistent with other commands to ensure that it is easy for the user to understand.

_______
When testing the code for yourself, you should use Python 3.8 and ensure that `discord` has been installed via PIP. You may also need to change some IDs temporarily in the data.py file when testing.

Please note that we may ask for you to make some changes to your pull request before we can accept it to ensure that it meets the general requirements we expect from a contribution.
