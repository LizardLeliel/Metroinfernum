"""
Chargen

Contains code related for a command-based chargen system

"""
from evennia import default_cmds
from evennia import CmdSet
import typeclasses.characters 

from evennia.utils.evmenu import EvMenu

# "
# text (str, tuple or None): Text shown at this node. If a tuple, the
#     second element in the tuple is a help text to display at this
#     node when the user enters the menu help command there.
# options (tuple, dict or None): (
#     {'key': name,   # can also be a list of aliases. A special key is
#                     # "_default", which marks this option as the default
#                     # fallback when no other option matches the user input.
#      'desc': description, # optional description
#      'goto': nodekey,  # node to go to when chosen. This can also be a callable with
#                        # caller and/or raw_string args. It must return a string
#                        # with the key pointing to the node to go to.
#      'exec': nodekey}, # node or callback to trigger as callback when chosen. This
#                        # will execute *before* going to the next node. Both node
#                        # and the explicit callback will be called as normal nodes
#                        # (with caller and/or raw_string args). If the callable/node
#                        # returns a single string (only), this will replace the current
#                        # goto location string in-place (if a goto callback, it will never fire).
#                        # Note that relying to much on letting exec assign the goto
#                        # location can make it hard to debug your menu logic.
#     {...}, ...)
# "

def validate_human(caller):
    # Check description
    # Check profile
    # Later: check moves
    # If all pass:
    #   Swap his type class
    #   Fill out the fields
    #   Finish!
    if len(caller.db.desc) < 320:
        caller.msg("|500You description is too short (only " + str(len(caller.db.profile)) + " characters long).|n")
        return "node_human_validate"

    if len(caller.db.profile) < 240:
        caller.msg("|500You profile is too short (only " + str(len(caller.db.profile)) + " characters long).|n")
        return "node_human_validate"

    caller.swap_typeclass("typeclasses.characters.HumanCharacter")

    pass

# Node 0
def node_race_select(caller):
    text = "Please select your race"
    options = [
        { "key": ["Human", "human"],
          "desc": "You wnat to be a human",
          "goto": "node_human_desc" },

        { "key": ["Demon", "demon"],
          "desc": "You want to be a demon",
          "goto": "node_demon_desc" }
    ]
    return text, options

# Node 1 Human
def node_human_desc(caller):
    text = (
    "Please describe your character using \"desc [your description]\". You can check your"
    " description by using \"look me\". Use |/ for new lines."
    "\nYour description should describe how your character appears, and should include"
    " details about your character's stature, clothing, recognizable facial features"
    " and outstanding characteristics"
    " like scars. How would other players see your character?"
    "\nIt must be 320 characters long. However, longer is recommended."
    )

    options = [
        { "key": ["(A)dvance", "advance", "a"],
          "desc": "Continue to profile",
          "goto": "node_human_profile" },
        
        { "key": ["(B)ack", "back", "b"],
          "desc": "Go back to race select",
          "goto": "node_race_select" 
        }
    ]
    return text, options

# Node 2 Human
def node_human_profile(caller):
    text = (
    "Please summarize your character using \"profile [your profile]\". You can check your"
    " description by using \"look me\". Use |/ for new lines"
    "Your profile is a short summary about your character."
    " It should tell other players about your character is about; what their"
    " personality is like, what they do, and defining characteristics. Who are they?"
    "\nIt must be 240 characters long. however, longer profiles are recommended."
    )

    options = [
        { "key": ["(A)dvance", "advance", "a"],
          "desc": "Go to validation",
          "goto": "node_human_validate" },
        
        { "key": ["(B)ack", "back", "b"],
          "desc": "Go back to description",
          "goto": "node_human_desc" }
    ]
    return text, options

# Node 3 Human
def node_human_validate(caller):
    text = "lel"
    options = [
        { "key": ["(B)ack", "back", "b"],
          "desc": "Go back to profile",
          # "exec": validate_human,
          # "goto": "node_done" }
          "goto": "node_human_profile" },
        
        { "key": "Finalize",
          "desc": "Finishes character generation if everything is valid",
          "exec": validate_human,
          "goto": "node_done" }
    ]
    return text, options

# Node 1 Demon
def node_demon_desc(caller):
    return "success", None

# Node 2 Demon
def node_demon_profile(caller):
    return None, None

# Node 3 Demon
def node_demon_abilities(caller):
    return None, None

# Node 4 Demon
def node_demon_validate(caller):
    return None, None


def node_done(caller):
    return None, None



class CmdChargen(default_cmds.MuxCommand):
    """
    Chargen

    Usage:
      +chargen

    Starts a simple walk-through character generation system.

    """
    key = "+chargen"

    def func(self):
        EvMenu(self.caller, 
               "commands.chargen",
               startnode = "node_race_select",
               cmdset_mergetype = "Union",
               persistent = False)

class CmdProfile(default_cmds.MuxCommand):
    """
    profile

    Usage:
      profile [desc]

    Sets someone profile. If you are not a wizard, then the only
    pofile you may set is your own, using me.

    """

    key = "profile"
    locks = "cmd:all()"

    def func(self):
        if not self.args:
            self.caller.msg("|555Please provide a profile.")
        else:
            self.caller.msg.db.profile = self.args.strip()
            self.caller.msg("You set your profile")

class CmdSetChargen(CmdSet):
    key = "Chargen"
    def at_cmdset_creation(self): 
        self.add(CmdChargen)