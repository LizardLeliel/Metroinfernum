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
        self.db.race = None

    def return_appearance(self, looker):
        appearance = super(Character, self).return_appearance(looker)
        # Perhaps change the line below
        appearance = self.db.name_colour + appearance[2:]
        return appearance

# Meant to represent things that in-game characters will have
#  that newly created characters won't until they completed char gen.
class PlayerCharacter(Character):
    def at_object_creation(self):
        super(PlayerCharacter, self).at_object_creation()
        


class HumanCharacter(PlayerCharacter):
    def at_object_creation(self):
        super(HumanCharacter, self).at_object_creation()
        self.db.name_colour = "|015"
        self.db.race = "Human"


class DemonCharacter(PlayerCharacter):
    def at_object_creation(self):
        super(DemonCharacter, self).at_object_creation()
        self.db.name_colour = "|520"
        self.db.race = "Demon"
