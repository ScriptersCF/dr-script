# Introduction
Thanks for showing an interest in improving our Discord bot! This not only helps improve the experience that we can offer to our members, but also gives you the opportunity to contribute to open-source software and show your skills as a developer!

For an introduction to the ScriptersCF organisation, feel free to take a look at our [organisation page](https://github.com/ScriptersCF). For any queries, feel free to join our [Discord community](https://discord.gg/N9GRpSC), or get in contact with the Community Lead, [@jotslo](https://github.com/jotslo).

# How do I get started?
Before starting, we first need to know what changes you wish to make to the bot. **We request that all contributors make a post in the [Issues](https://github.com/ScriptersCF/dr-script/issues) tab first**. This allows for us to reduce everyone's workload, and ensure that we keep our bot to a high standard.

When posting your Issue, please describe in detail what you would like to modify, or what feature you would like to add to the bot. You should also add the **enhancement** tag to your post, so we can identify it more easily.

Please wait for one of our maintainers to respond to your request before continuing from this point. If we like your idea and accept your request, you can then begin working on the project.

# How do I start working on my enhancement?
After your suggestion has been approved, you will need to install the bot onto your own device so that you can test it. Please follow the instructions listed below.

1) Ensure that you have the latest version of [Python 3.10](https://python.org) installed. *This is the version that we currently use.*
2) Install the latest version of [discord.py](https://pypi.org/project/discord.py/) with the following command: `pip install discord`
3) Fork the Git repository, so that you have a safe variant which you can modify and test.
4) Clone the forked Git repository to your local device.
5) **Duplicate** the `default-scores.sqlite` file, and name it `scores.sqlite`, leaving it in the same directory. *This is where your bot will store data, and will be automatically ignored in your Git commits*
6) **Duplicate** the `modules/default-token.py` file, and name it `token.py`, leaving it in the same directory. *This is where you store your test bot's token, and will be automatically ignored in your Git commits*
7) Modify your new `modules/token.py` file, entering your test bot's token. You will need to have [created a Discord bot](https://discord.com/developers/applications) for this, if you haven't already.
8) Navigate to `modules/data.py` and change the `server_id` value to your own server's ID. If you are not testing the point system, it is recommended to set `award_points` to `False`.
9) Scroll through the `data.py` file and change any values that you deem fit. *Each variable has an explanation for its use, and whether you should change it.*
10) Run the `main.py` file to test the bot is working as expected. *If you are having issues, feel free to get in touch with us and we can help!*

# Keeping your code consistent
You may now use this opportunity to implement your feature as outlined in your Issue, but please consider the following points:
- You are expected to keep the codebase consistent. Please familiarise yourself with the project's code style, including the usage of comments.
- Please ensure that lines of code are not too long, and stick to the PEP8 style guide where possible.
    - An exception to this is the use of double newlines between functions, which we use to make it easier to differentiate between functions.
- Keep code in relevant places. If you feel that it is appropriate to create a new file for a certain feature, feel free to do so.
- If you have any queries about this, make sure to ask us! We're happy to help!

# Submitting your contribution
Once you are happy with your contribution and it is ready to be submitted, please follow these instructions:
1) Revert any IDs and changes in `modules/data.py` to their original state, as this is extra work for us otherwise.
2) Ensure that your `scores.sqlite` file and `modules/token.py` file are not included in your commits.
3) Commit these final changes to your fork.

You may now submit a pull request for your fork. Please include a reference to your Issue, so that we can familiarise ourselves with the proposed features that are being implemented.

# That's it!
If you have any queries, be sure to get in touch with a project maintainer, either through an Issue, or our Discord server.

Thank you very much for your interest in contributing to our open-source project!
