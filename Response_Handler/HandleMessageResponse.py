from .API_Library.API_Models.Team import Stats, Info
from .API_Library.API_Models.Event import Alliance, Match
from .FindData import FindData

class HandleMessageResponse:
    """
    Example Usage
    -----
    
    message = HandleMessageResponse.match_message_data([1454, 284], [1454, 284]) \n
    """
    
    @staticmethod
    def team_message_data(teamNumber):
        """
        Returns a Team Summary Object containing the data necessary for the team message.

        """
        data_search = FindData()
        try:
                
            team_stats = data_search.find_team_stats_from_json(teamNumber)
            team_info = data_search.callForTeamInfo(teamNumber)
            
            if team_info and team_info is not None:
                return (team_stats + team_info) # Summary Object
            else:
                return KeyError("Team not found.")
        except Exception:
            raise KeyError("Data message not found.")

    @staticmethod
    def get_team_stats(team):
        try:
            return HandleMessageResponse.team_message_data(team)['stats']
        except KeyError as e:
            raise e

    @staticmethod
    def form_alliance(color, teams):
        """Creates an Alliance object from a list of team numbers"""
        team_objects = [HandleMessageResponse.get_team_stats(team) for team in teams]
        if len(team_objects) != 2:
            raise ValueError("Alliances are required to have exactly two teams.")
        return Alliance(team1=team_objects[0], team2=team_objects[1], color=color)

    @staticmethod
    def match_message_data(redAlliance, blueAlliance=None):
        """
        Returns a Match object containing the data necessary for the match message.

        Args:
            redAlliance (list): List of team numbers for the red alliance.
            blueAlliance (list, optional): List of team numbers for the blue alliance. Defaults to None.

        Returns:
            Match: A Match object containing the red and blue alliances.
        """
        if len(redAlliance) > 2 or (blueAlliance is not None and len(blueAlliance) > 2):
            raise ValueError("Exactly two teams are required to form an alliance.")

        red_alliance = HandleMessageResponse.form_alliance('Red', redAlliance)
        blue_alliance = HandleMessageResponse.form_alliance('Blue', blueAlliance) if blueAlliance else None

        return Match(redAlliance=red_alliance, blueAlliance=blue_alliance) if blueAlliance else red_alliance

# Example usage
# message = HandleMessageResponse.match_message_data([14584, 14584])
# print(message)