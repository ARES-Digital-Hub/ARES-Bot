import discord
from discord import app_commands
from discord.ext import commands
from Response_Handler import HandleMessageResponse as msg
from datetime import datetime
from Discord.BotState import State
from Discord.Slash_Commands.MatchImageCreator import ImageCreator
import time

class cmdMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="match", description="Displays match details.")
    @app_commands.describe(red_alliance="Red Alliance team numbers (space-separated).", blue_alliance="Blue Alliance team numbers (space-separated, optional).")
    async def match(self, interaction: discord.Interaction, red_alliance: str, blue_alliance: str = None):
        if self.bot.debug_mode and interaction.channel_id != self.bot.debug_channel_id:
            return

        try:
            # Defer response to allow processing time
            # await interaction.response.defer()

            red_alliance_teams = [team.strip() for team in red_alliance.split()]
            blue_alliance_teams = [team.strip() for team in blue_alliance.split()] if blue_alliance else []

            if len(red_alliance_teams) != 2 or (blue_alliance and len(blue_alliance_teams) != 2):
                embed = State.WARNING(description="Each alliance must have exactly 2 team numbers separated by a space.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            match = msg.match_message_data(red_alliance_teams, blue_alliance_teams)
            winner = match.winner if blue_alliance_teams else None

            image_name = "match_scoreboard.png"

            red_scores = match.redAlliance.scoreboard
            blue_scores = match.blueAlliance.scoreboard if blue_alliance_teams else [0, 0, 0, 0, 0]
            
            # start_time = time.time()
            if match.blueAlliance.teamNames[0] == "":
                image = ImageCreator.createAllianceImage(
                    team_1=match.redAlliance.teamNames[0],
                    team_2=match.redAlliance.teamNames[1],
                    team_1number=red_alliance_teams[0],
                    team_2number=red_alliance_teams[1],
                    team1_auto=f"{match.redAlliance.team1.stats.autoOPR:.2f}",
                    team2_auto=f"{match.redAlliance.team2.stats.autoOPR:.2f}",
                    team1_teleop=f"{match.redAlliance.team1.stats.teleOPR:.2f}",
                    team2_teleop=f"{match.redAlliance.team2.stats.teleOPR:.2f}",
                    team1_endgame=f"{match.redAlliance.team1.stats.endgameOPR:.2f}",
                    team2_endgame=f"{match.redAlliance.team2.stats.endgameOPR:.2f}",
                    team1_opr=f"{match.redAlliance.team1.stats.overallOPR:.2f}",
                    team2_opr=f"{match.redAlliance.team2.stats.overallOPR:.2f}"
                )
            else:
                image = ImageCreator.createMatchImage(
                    red_team_1=match.redAlliance.teamNames[0],
                    red_team_2=match.redAlliance.teamNames[1],
                    blue_team_1=match.blueAlliance.teamNames[0] if blue_alliance_teams else "",
                    blue_team_2=match.blueAlliance.teamNames[1] if blue_alliance_teams else "",
                    red_team_1number=red_alliance_teams[0],
                    red_team_2number=red_alliance_teams[1],
                    blue_team_1number=blue_alliance_teams[0],
                    blue_team_2number=blue_alliance_teams[1],
                    red_auto=red_scores[2],
                    blue_auto=blue_scores[2],
                    red_teleop=red_scores[3],
                    blue_teleop=blue_scores[3],
                    red_endgame=red_scores[4],
                    blue_endgame=blue_scores[4],
                    red_penalties=0,
                    blue_penalties=0,
                    red_final=red_scores[5],
                    blue_final=blue_scores[5]
                )
            # print(time.time()-start_time) # To view speed top speed 0.007 for match and 0.009 for alliance
            
            image.save(image_name, format="PNG")

            # Determine embed color
            color = State.WHITE if winner == "Tie" or not blue_alliance_teams else (
                State.CHALLENGE_RED if winner == "Red" else State.FIRST_BLUE
            )

            embed = discord.Embed(title="Match Scoreboard", color=color, timestamp=datetime.now())
            embed.set_image(url=f"attachment://{image_name}")

            file = discord.File(image_name, filename=image_name)
            await interaction.response.send_message(embed=embed, file=file)

        except Exception as e:
            if self.bot.debug_mode:
                print(f"Error: {e}")
            embed = State.ERROR(title="Error", description="An error occurred while processing the match data.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(cmdMatch(bot))

# import discord
# from discord import app_commands
# from discord.ext import commands
# from Response_Handler import HandleMessageResponse as msg
# from datetime import datetime
# from Discord.BotState import State
# import os
# from html2image import Html2Image
# from jinja2 import Template

# class cmdMatch(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
    
#     @app_commands.command(name="match", description="Displays match details.")
#     @app_commands.describe(red_alliance="Red Alliance team numbers (space-separated).", blue_alliance="Blue Alliance team numbers (space-separated, optional).")
#     async def match(self, interaction: discord.Interaction, red_alliance: str, blue_alliance: str = None):
#         if self.bot.debug_mode and interaction.channel_id != self.bot.debug_channel_id:
#             return

#         try:
#             # Defer response to allow processing time
#             await interaction.response.defer()

#             # Process alliance teams
#             red_alliance_teams = [team.strip() for team in red_alliance.split()]
#             blue_alliance_teams = [team.strip() for team in blue_alliance.split()] if blue_alliance else []

#             if len(red_alliance_teams) != 2 or (blue_alliance and len(blue_alliance_teams) != 2):
#                 embed = State.WARNING(description="Each alliance must have exactly 2 team numbers separated by a space.")
#                 await interaction.followup.send(embed=embed, ephemeral=True)
#                 return

#             # Get match data
#             match = msg.match_message_data(red_alliance_teams, blue_alliance_teams)
#             winner = match.winner if blue_alliance_teams else None

#             # Template processing for HTML to image
#             template_path = os.path.join(os.path.dirname(__file__), 'template.html')
#             if not os.path.exists(template_path):
#                 raise FileNotFoundError("The 'template.html' file was not found.")

#             with open(template_path, 'r', encoding='utf-8') as file:
#                 html_template = Template(file.read())

#             html_content = html_template.render(
#                 title="Scoreboard",
#                 description="Match Details",
#                 red_team_1=match.redAlliance.teamNames[0],
#                 red_team_2=match.redAlliance.teamNames[1],
#                 red_auto=match.redAlliance.scoreboard[2],
#                 red_teleop=match.redAlliance.scoreboard[3],
#                 red_endgame=match.redAlliance.scoreboard[4],
#                 red_final=match.redAlliance.scoreboard[5],
#                 blue_team_1=match.blueAlliance.teamNames[0],
#                 blue_team_2=match.blueAlliance.teamNames[1],
#                 blue_auto=match.blueAlliance.scoreboard[2],
#                 blue_teleop=match.blueAlliance.scoreboard[3],
#                 blue_endgame=match.blueAlliance.scoreboard[4],
#                 blue_final=match.blueAlliance.scoreboard[5]
#             )

#             image_name = "match.png"
#             hti = Html2Image(
#                 browser='chrome',
#                 custom_flags=[                    
#                     "--headless",
#                     "--disable-gpu",
#                     "--no-sandbox",
#                     "--disable-extensions",
#                     "--disable-dev-shm-usage",
#                     "--disable-software-rasterizer",
#                     "--disable-dbbackend",
#                     "--disable-broker"
#                 ]
#             )
#             img_path = hti.screenshot(html_str=html_content, size=(850, 700), save_as=image_name)[0]

#             # Send the image and match data
#             file = discord.File(img_path, filename=image_name)
#             color = State.WHITE if winner == "Tie" or not blue_alliance_teams else (State.CHALLENGE_RED if winner == "Red" else State.FIRST_BLUE)
#             embed = discord.Embed(title="Match Scoreboard", color=color, timestamp=datetime.now())
#             embed.set_image(url=f"attachment://{image_name}")

#             await interaction.followup.send(embed=embed, file=file)

#         except FileNotFoundError as e:
#             if self.bot.debug_mode:
#                 print(f"File error: {e}")
#             embed = State.ERROR(title="Error", description="Template file not found.")
#             await interaction.followup.send(embed=embed, ephemeral=True)

#         except Exception as e:
#             if self.bot.debug_mode:
#                 print(f"Error: {e}")
#             embed = State.ERROR(title="Error", description="An error occurred while processing the match data.")
#             await interaction.followup.send(embed=embed, ephemeral=True)

# async def setup(bot):
#     await bot.add_cog(cmdMatch(bot))