import discord
from discord import app_commands
from Response_Handler.HandleMessageResponse import HandleMessageResponse as msg
import requests
import re

class cmdTeam:
    def __init__(self, bot, visual):
        self.bot = bot
        self.visual = visual

    def setup(self):
        @self.bot.tree.command(name="team", description="Displays team information.")
        @app_commands.describe(team_number="Details about the team.")
        async def team(interaction: discord.Interaction, team_number: str):
            if self.bot.debug_mode and interaction.channel_id != self.bot.debug_channel_id:
                return
            
            if not team_number or not team_number.isdigit():
                embed = self.visual.WARNING
                embed.add_field(name="Reason:", value="Team number must be numerical.")
                await interaction.response.send_message(embed=self.visual.WARNING, ephemeral=True)
                return

            try:
                message = msg.team_message_data(team_number).__str__()
            except Exception as e:
                print(e) if self.bot.debug_mode else None
                embed = self.visual.ERROR
                embed.add_field(name="Reason:", value="Team number must be valid.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            lines = message.strip().split('\n')
            embed = discord.Embed(
                title=f"Information for Team {team_number}",
                description="\n".join(lines[:-1]),
                color=discord.Color.lighter_grey()
            )
            
            # try:
                # url = None  # Initialize the url variable
                # css_content = requests.get('https://ftc-scoring.firstinspires.org/avatars/composed/2025.css').text
                # match = re.search(rf'\.team-{team_number} \{{\s*background-image: url\("(?P<url>data:image/png;base64,[^"]+)"\);', css_content)
                # if match:
                #     url = match.group("url")
                
                # if url and url.startswith("data:image/png;base64,"):
                #     embed.set_thumbnail(url=url)
                # else:
                    # embed.set_thumbnail(url="data:image/svg+xml;PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMzEiIGhlaWdodD0iMTczIj48ZGVmcz48Y2xpcFBhdGggaWQ9ImEiPjxwYXRoIGQ9Ik0yNiAuMjA3aDI4VjEwMkgyNlptMCAwIi8+PC9jbGlwUGF0aD48Y2xpcFBhdGggaWQ9ImIiPjxwYXRoIGQ9Ik0zNCAuMjA3aDgxVjEwMkgzNFptMCAwIi8+PC9jbGlwUGF0aD48Y2xpcFBhdGggaWQ9ImMiPjxwYXRoIGQ9Ik0xMDUgLjIwN2g5OVY5OWgtOTlabTAgMCIvPjwvY2xpcFBhdGg+PGNsaXBQYXRoIGlkPSJkIj48cGF0aCBkPSJNMTc1IDExNGg1NS4xNHY1OEgxNzVabTAgMCIvPjwvY2xpcFBhdGg+PC9kZWZzPjxwYXRoIGZpbGw9IiM5NTk1OTYiIGQ9Ik0xMTEuNyAzMy45MzRjMy4xMiAwIDYuMTUyLjI4NSA5LjA0Mi44MTJsNi44ODctNy4xNzJjLTQuODE3LTEuNjY0LTEwLjIxOS0yLjYwMS0xNS45My0yLjYwMS05LjcxIDAtMTguNTI3IDIuNzEtMjUuMDY2IDcuMTE3bDYgNS42ODNjNS41NDctMi40MyAxMi4wNzQtMy44NCAxOS4wNjYtMy44NCIvPjxwYXRoIGZpbGw9IiNGRkYiIGQ9Ik0xMTEuNyAyNC45NzNjNS43MSAwIDExLjExMi45MzcgMTUuOTI5IDIuNjAxbDcuNDgtNy43OTNjLTYuOTgtMi43NS0xNC45NDUtNC4zMTItMjMuNDEtNC4zMTItMTIuNjE3IDAtMjQuMTI5IDMuNDY5LTMyLjkxNCA5LjE4M2w3Ljg0OCA3LjQzOGM2LjUzOS00LjQwNiAxNS4zNTUtNy4xMTcgMjUuMDY2LTcuMTE3Ii8+PHBhdGggZmlsbD0iIzk1OTU5NiIgZD0iTTc1Ljc2MiA1NS40NTdjLjYyOS0yLjU3IDEuNzkzLTUuMDEyIDMuMzk4LTcuMjY2bC0zLjAxNS0zLjA0NmExOSAxOSAwIDAgMC0uOTMgNS44MzVjMCAxLjUyOC4xOTEgMy4wMjQuNTQ3IDQuNDc3TTUzLjQ4OCA3Mi4zMTZsLTEuMjY1IDYuNTYzIDEyLjU5My01LjQyMmMtLjc5Ni0xLjY3Mi0uOTUzLTMuODUyLTEuNDE0LTUuNjI1eiIvPjxnIGNsaXAtcGF0aD0idXJsKCNhKSI+PHBhdGggZmlsbD0iIzk1OTU5NiIgZD0iTTQ0LjYyNS45NTcgMjYuMzk4IDEwMC43N2w4LjYyMi43MDNMNTMuMDY2LjIwN3oiLz48L2c+PGcgY2xpcC1wYXRoPSJ1cmwoI2IpIj48cGF0aCBmaWxsPSIjRUQxQzI0IiBkPSJNMTA1LjkxNCA1OC4zOTVWNTAuMzJMOTIuNjggMzcuNzczbC02LTUuNjgzLTcuODQ4LTcuNDM4TDUzLjAzNS4yMDcgMzQuOTggMTAxLjQ3M2wzOC4yMDQtMTYuNzk3Yy0zLjgwNS0zLjM2LTYuNS02Ljk0Mi04LjUtMTEuMTZsLTEyLjQzOCA1LjMzMiAxLjI0Ni02LjUyOCA4LjA1OS00MiAuNjc2LTMuNTIzIDYuNjUyIDYuNyA4LjU1OCA4LjYyIDMuNjc2IDMuNzA3TDk2LjIyNyA1OC44NGwtMTQuNjcyIDYuNzE5YzMuODEyIDMuODA4IDguMzIgNy4xNiAxNC40MDYgOS4wNTRsMTguMy04LjIxOHoiLz48L2c+PHBhdGggZmlsbD0iIzk1OTU5NiIgZD0iTTE0Ny42MzMgNTUuNDU3Yy4zNTUtMS40NTMuNTUtMi45NS41NS00LjQ3NyAwLTQuNTExLTEuNjQ4LTguNzY1LTQuNDg0LTEyLjQ2bC00LjM0NCA0LjVjNC4xNjggMy40NzIgNy4xMzcgNy43NSA4LjI3OCAxMi40MzdNMTU1LjggOTguMThsLTEwLjI5Ni05Ljg5NWE1MSA1MSAwIDAgMS01LjI1IDMuMTI1bDE1LjU0NyAxNC45MyA0Ny45NDEtNDkuOTM4LS4wNS04LjA4NnptLTM0LjkzNy0zMy41NC04LjQ3Ni04LjE0NC02LjQ5Mi02LjE5NS0uMDI0IDguMDk0IDkuMTI1IDguNzYxIDguNzIzIDguMzc1YTQ1IDQ1IDAgMCAwIDYuMzI4LTIuMDc0eiIvPjxwYXRoIGZpbGw9IiM5NTk1OTYiIGQ9Im0xNTQuMiAxOS40OC02LjgyNSA3LjEwNi03LjUzMSA3Ljg0OC01LjEzIDUuMzQtOS43MjYgMTAuMTI4IDQuMDc1IDMuOTFMMTM5LjQxIDQzLjA0bDQuMzI4LTQuNTA4IDcuOTI2LTguMjUgMi41MzUtMi42NDQgMjYuMzY3IDI1LjI3MyA0LjA3OS00LjIzNHoiLz48cGF0aCBmaWxsPSIjRkZGIiBkPSJtMTUxLjY2NCAzMC4yODEtNy45MjYgOC4yNWMyLjgzNiAzLjcgNC40NDYgNy45MzggNC40NDYgMTIuNDUgMCAxLjUyNy0uMTk2IDMuMDIzLS41NTEgNC40NzYtLjkyNiAzLjc5Ny0zLjAwNCA3LjMwOS01Ljk2OSAxMC4zNDgtMy4wMzkgMy4xMTMtNy4wMDQgNS43My0xMS42MTcgNy42NTJhNDUgNDUgMCAwIDEtNi4zMjggMi4wNzQgNTAgNTAgMCAwIDEtMTIuMDIgMS40NWMtNS4xODcgMC0xMC4xMTctLjc3LTE0LjU4Mi0yLjE2NS02LjA4Ni0xLjg5NC0xMS4zLTQuOTMzLTE1LjExMy04Ljc0NmEyNS40IDI1LjQgMCAwIDEtMy41ODYtNC40NTNjLTEuMjIzLTEuOTM3LTIuMTI1LTQtMi42NTYtNi4xNmExOC44IDE4LjggMCAwIDEtLjU0Ny00LjQ3N2MwLTIuMDA3LjMyOC0zLjk2LjkzLTUuODM1bC05LjEwNi05LjIxNWMtMy4zMzIgNC45NDEtNS4yMTUgMTAuNTExLTUuMjE1IDE2LjQxNCAwIDEuNTIuMTQgMy4wMTEuMzgzIDQuNDguNTgyIDMuNTY3IDEuODYgNi45NzMgMy43MjMgMTAuMTQ5YTM0IDM0IDAgMCAwIDMuMjM0IDQuNjAxYzMuMjAzIDMuODY3IDcuMzMyIDcuMjU4IDEyLjE3MiAxMC4wMTIgOC40MDYgNC43ODEgMTguOTMgNy42MzMgMzAuMzYzIDcuNjMzIDcuOTk2IDAgMTUuNTUxLTEuMzk1IDIyLjI0Ni0zLjg2N2E1NSA1NSAwIDAgMCA1Ljg0NC0yLjU0M2M0LjMyLTIuMTg0IDguMTQ5LTQuODUyIDExLjM0OC03LjkwNyA1LjM2My01LjEyNSA4Ljk0OS0xMS4zMTYgMTAuMDU0LTE4LjA3OC4yNDMtMS40NjkuMzgtMi45Ni4zOC00LjQ4IDAtOC4yNzQtMy42ODQtMTUuOTEtOS45MDctMjIuMDYzIi8+PGcgY2xpcC1wYXRoPSJ1cmwoI2MpIj48cGF0aCBmaWxsPSIjMUM2M0I3IiBkPSJtMTIwLjgyIDY0LjcwMyA5LjE1MyA4Ljc4NWM0LjYwOS0xLjkyMiA4LjYwNS00LjUwOCAxMS42NDgtNy42MkwxMjkuMDc0IDUzLjgyIDEyNSA0OS45MWw5LjY3Mi0xMC4wNzQgNS4xMjktNS4zNDQgNy41MzEtNy44NDQgNi44MjQtNy4xMDUgMzAuMzcxIDI5LjE1Ni00LjA3OCA0LjI0Ni0yNC44NzkgMjUuOTA3Yy0yLjYyIDMuNTkzLTYuMDIgNi43NzctMTAuMDM1IDkuNTI3bDEwLjIxOSA5Ljg2MyA0Ny45NDUtNDkuOTNMMTUzLjc2Ni4zNjdsLTE4LjcgMTkuNDc3LTcuNDg0IDcuNzkzLTYuODgzIDcuMTcyTDEwNS44OTUgNTAuM3oiLz48L2c+PHBhdGggZmlsbD0iIzk1OTU5NiIgZD0iTTc4LjYyNSA2MS44NjdzLjIzNC4zOTUuMjY2LjQzOGMuNzMgMS4xNjQgMS43MzggMi4yMyAyLjY5MSAzLjI5M2wxNC45MTQtNi44OTEtMzQuMjczLTMxLjkyMi0uOTM4IDQuOTM4TDg4LjE4IDU4LjM0OHoiLz48cGF0aCBmaWxsPSIjOTU5NTk2IiBkPSJNMTYxLjU3IDUyLjM0NGMwIDEuNTItLjEzNiAzLjAxMS0uMzc5IDQuNDgtMS4xMDUgNi43NjItNC42OTEgMTIuOTUzLTEwLjA1NCAxOC4wNzgtMy4yIDMuMDU1LTcuMDI4IDUuNzIzLTExLjM0OCA3LjkwN2E1NSA1NSAwIDAgMS01Ljg0NCAyLjU0M2MtNi42OTUgMi40NzItMTQuMjUgMy44NjctMjIuMjQ2IDMuODY3LTExLjQzMyAwLTIxLjk1Ny0yLjg1Mi0zMC4zNjMtNy42MzMtNC44NC0yLjc1NC04Ljk2OS02LjE0NS0xMi4xNzItMTAuMDEyYTM0IDM0IDAgMCAxLTMuMjM0LTQuNjAxYy0xLjg2NC0zLjE3Ni0zLjE0LTYuNTgyLTMuNzIzLTEwLjE0OWEyNy41IDI3LjUgMCAwIDEtLjM4My00LjQ4YzAtLjQ3Ny4wMzUtLjk1LjA1OS0xLjQxOC0uMDA0LS4wMjgtLjAxMi0uMDYzLS4wMTYtLjA4Ni0uMjQyIDEuNDY5LS4wNDMgOC45NS0uMDQzIDEwLjQ2OSAwIDIuNDAyLjMyIDQuNzU0LjkxOCA3LjAzYTI5IDI5IDAgMCAwIDEuODk1IDUuMTc3YzIgNC4yMTggNS4wMDggOC4wOSA4LjgxMiAxMS40NDkgOS4xNTMgOC4wNzQgMjIuODg3IDEzLjIxNSAzOC4yNSAxMy4yMTUgMTAuNjYgMCAyMC41MjgtMi40OCAyOC42MzctNi42OTIgMS44NC0uOTU3IDMuNTk0LTIgNS4yMzgtMy4xMjkgNC4wMTYtMi43NDYgNy40MjItNS45NzYgMTAuMDQtOS41NyAzLjgtNS4xOTUgNS45NTYtMTEuMTUyIDUuOTU2LTE3LjQ4IDAtMS4zMzYuMTE4LTcuNjY0LS4wMTEtMTAuMTc2LS4wMjQtLjM0NC4wMTEuNzczLjAxMSAxLjIxIi8+PHBhdGggZmlsbD0iI0ZGRiIgZD0iTTEzLjM1NSAxMTQuMTk1aDM5LjY5MmwtMy43MzggMTUuMjg1SDMwLjI4NWwtMS44NzkgOC4wMzJINDguMjVsLTMuNDU3IDE0LjE2SDI1LjIwN2wtNC43MDMgMjAuMTIxSDB6bTQ1LjA4NiAwaDIwLjUwNEw2NS41OSAxNzEuNzkzSDQ1LjA4NnptNDEuMDEyIDI3LjQ2MWM2LjU4NiAwIDExLjE5Mi0zLjg4NiAxMS4xOTItOS40MTQgMC0yLjkzMy0yLjE2LTQuNDAyLTYuMzk1LTQuNDAyLTEuMjIzIDAtMS44NzkuMDg2LTMuMTk1LjM0NGwtMy4xMDYgMTMuMjk2Yy42NTYuMDkuNzU0LjE3NiAxLjUwNC4xNzZtLTE1LjE0LTI3LjExMyAxLjMxNi0uMTc2YzYuNTgyLS43NzMgMTQuNzY2LTEuMjkzIDE5LjI4MS0xLjI5MyA3LjUyNCAwIDEzLjM1Ni44NjQgMTcuNzc4IDIuNjc2IDUuNjQgMi4zMzIgOS4wMjcgNy40MjYgOS4wMjcgMTMuNTU5IDAgNS4yNjUtMS43ODUgMTAuMjczLTUuMTc2IDE0LjE2LTIuOTE0IDMuMzY3LTUuNTQ3IDUuMDA4LTExLjAwNCA2LjY0OGwtMS4zMTYuNDNjLjU2Ni40MzMuNzU0LjYwNSAxLjAzNS44NjcgMS42MDEgMS44MTMgNi4zOTggMTEuMTQgMTAuNDQxIDIwLjM3OWgtMjIuNTc0Yy0yLjkxNC04LjIwNy0zLjc2Mi0xMC4zNjMtNy42MTctMTkuNjkxbC00LjUxNiAxOS42OTFINzEuMDUxeiIvPjxnIGNsaXAtcGF0aD0idXJsKCNkKSI+PHBhdGggZmlsbD0iI0ZGRiIgZD0iTTE4MC4zOSAxMTQuMTk1aDQ5Ljc1bC0zLjQ3NiAxNi42NzJoLTE0Ljc2NmwtOS43OCA0MC45MjZoLTIwLjUwNWw5Ljc4Mi00MC45MjZIMTc1LjM5eiIvPjwvZz48cGF0aCBmaWxsPSIjRkZGIiBkPSJNMjExLjU3OCAxNjYuMzM2Yy40NDUgMCAuNjk1LS4yMTUuNjk1LS42MjEgMC0uMzg3LS4yMzQtLjU5OC0uNjc1LS41OTgtLjA5OCAwLS4xMTggMC0uMjE1LjAydjEuMThjLjA3OC4wMTkuMTE3LjAxOS4xOTUuMDE5bS0xLjc5Ny0yLjM5OWMuMjUtLjAxOS4yOS0uMDM5Ljc5My0uMDc4LjUtLjAzOS43MTUtLjA1OC45MjYtLjA1OCAxLjY0NSAwIDIuNDUzLjY0IDIuNDUzIDEuODU1IDAgLjczOS0uMzA1IDEuMTgtLjk2NSAxLjQzNGwtLjA3OC4wMmMuMDU5LjAzOC4wNzguMDU4LjA5OC4wOTMuMTc2LjE1Ni43NTQgMS4wMjcgMS4yMzggMS44MmgtMS44NzVjLS4zODctLjcxNC0uNTA0LS45MS0uOTg4LTEuNzIydjEuNzIyaC0xLjYwMlptMS45MzQgNi45NDJhNC4zNyA0LjM3IDAgMCAwIDQuMzg3LTQuMzcxIDQuMzczIDQuMzczIDAgMCAwLTQuMzg3LTQuMzg3IDQuMzY1IDQuMzY1IDAgMCAwLTQuMzcxIDQuMzY3YzAgMi40NTcgMS45MzMgNC4zOSA0LjM3IDQuMzltMC05LjM3OWE0Ljk5MyA0Ljk5MyAwIDAgMSA1LjAwNCA0Ljk4OCA0Ljk4IDQuOTggMCAwIDEtNS4wMDQgNS4wMDhjLTIuODA1IDAtNC45ODgtMi4xODQtNC45ODgtNS4wMDhhNC45NTMgNC45NTMgMCAwIDEgNC45ODgtNC45ODhtLTgzLjk5OSA4LjgyOWM1Ljc2MiAxLjcxMSAxMi4wNjYgMi42NzIgMTcuOTU3IDIuNjcyIDcuOTkyIDAgMTQuMTEtMS44MTIgMTkuMzc1LTUuNjEzIDUuODMyLTQuMTQ1IDkuNTk0LTEwLjUzNSA5LjU5NC0xNi4zMiAwLTMuODgzLTEuNjkyLTcuNDI2LTQuNzAzLTkuOTMtMi4zNTItMS44OTktNC43OTctMy4zNjctOS43ODItNS43bC00LjA0My0xLjg5OGMtMS4zMi0uNjkxLTEuOTc2LTEuMzgzLTEuOTc2LTIuMTYgMC0yLjA3IDIuNjMzLTMuNjI1IDYuMjA3LTMuNjI1IDIuNjc2IDAgNS44Ni43NzcgMTEuOTQ5IDIuNzdsNC4yMDMtMTUuNTljLTQuNTU1LTEuMjM5LTguOTkyLTEuODYtMTMuNDI2LTEuODYtMTYuNzQyIDAtMjkuNjI1IDkuMTUzLTI5LjYyNSAyMC45ODUgMCA2LjIxNCA0LjEzNyAxMC42MiAxNC40ODUgMTUuNDU3IDQuODkgMi4yNDIgNS43MzQgMi44NDcgNS43MzQgNC40MDIgMCAyLjMyOC0yLjUzOSAzLjgtNi42NzYgMy44LTMuNjY4IDAtOC4zNy0xLjEyNC0xNC43NjUtMy40NTZsLS4wMDguMDA0eiIvPjwvc3ZnPg==")
            # except ImportError as e:
            #     print(f"Error Pulling Team Avatars: {e}")
                
            embed.set_footer(text=lines[-1])
            await interaction.response.send_message(embed=embed)