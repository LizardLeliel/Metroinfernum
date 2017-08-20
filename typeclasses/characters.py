"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """
    pass

    def at_object_creation(self):
        super(DefaultCharacter, self).at_object_creation()
        self.db.name_colour = "|555"

    def return_appearance(self, looker):
        appearance = super(DefaultCharacter, self).return_appearance(looker)
        appearance = self.db.name_colour + appearance[2:]
        return appearance


# 035

class HumanCharacter(Character):

    def at_object_creation(self):
        super(DefaultCharacter, self).at_object_creation()
        self.db.name_colour = "|015"

        # Permanent stats
        self.db.strength    = 1.00
        self.db.resilience  = 1.00
        self.db.proficiency = 1.00
        self.db.observation = 1.00

        # Status
        self.db.health = 100.0 # Replace with the method to calculate total health
        self.db.energy = 100.0 

        self.db.profile = None


class DemonCharacter(Character):

    def at_object_creation(self):
        super(DefaultCharacter, self).at_object_creation()
        self.db.name_colour = "|520"

        # Permanent stats - Perhaps this factor this into a common "player character"
        #  class>
        self.db.strength    = 1.00
        self.db.resilience  = 1.00
        self.db.proficiency = 1.00
        self.db.observation = 1.00

        # Status - Demons have no energy, unlike humans
        self.db.health = 100.0 # Replace with the method to calculate total health
        
        self.db.profile = None        