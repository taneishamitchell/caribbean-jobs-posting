import discord
import sys
import app
import os


posting_path = os.getcwd() + '/'

channelID = 557234203972861954

if os.environ.get('ENV') == "dev":
    channelID = 555797201465638912  # testing-channel in CCST server

app.jobpostfile()  # job posting function creates txt file that sends posts to CCST discord channel


class JobBoardClient(discord.Client):
    """
    Reads txt file with caribbeanjobs.com postings;
    Writes to CCST discord channel
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.job_board_task_bg())

    async def on_ready(self):
        print('Logged in as {0.user}'.format(client))
        print('User ID: ', self.user.id)
        print(9 * '-')

    async def job_board_task_bg(self):
        # TODO: Find a nicer way to break continuous loop
        await self.wait_until_ready()
        channel = self.get_channel(channelID)

        while not self.is_closed():
            with open(posting_path + 'posts.txt', 'r') as txtFile:
                txtreader = txtFile.readlines()

                for line in txtreader:
                    await channel.send(line)
                sys.exit()   # to avoid constant loop close connection

        self.is_closed()


client = JobBoardClient()

client.run(os.environ.get('BOT_TOKEN'))
