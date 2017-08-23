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

# Todo: refactor 320 and 240 into named constants
# Also todo: refactor these two functions (they're pratically the same)
def validate_human(caller):
    if len(caller.db.desc) < 320:
        caller.msg("|500You description is too short (only " + str(len(caller.db.profile)) + " characters long).|n")
        return "node_human_validate"

    if len(caller.db.profile) < 240:
        caller.msg("|500You profile is too short (only " + str(len(caller.db.profile)) + " characters long).|n")
        return "node_human_validate"

    caller.swap_typeclass("typeclasses.characters.HumanCharacter")

def validate_demon(caller):
    if len(caller.db.desc) < 320:
        caller.msg("|500You description is too short (only " + str(len(caller.db.profile)) + " characters long).|n")
        return "node_demon_validate"

    if len(caller.db.profile) < 240:
        caller.msg("|500You profile is too short (only " + str(len(caller.db.profile)) + " characters long).|n")
        return "node_demon_validate"

    caller.swap_typeclass("typeclasses.characters.DemonCharacter")

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
    "\nIt must be 320 characters long. Longer descriptions are encouraged, however."
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
    " profile by using \"+info me\". Use |/ for new lines."
    "\nYour profile is a short summary about your character, focusing on its non-physical traits."
    " It should tell other players about your character is about; what their"
    " personality is like, what they do, some defining characteristics, and possibly some"
    " backstory. Who are they, what do they like to do, and why?"
    "\nIt must be 240 characters long. Longer profiles are encouraged, however."
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
    text = (
        "Type \"finalize\" at any time to finish chargen. Doing this will check"
        " then lengths of both your profile and description. If both are"
        " valid, will change you into a human character. You'll then be allowed"
        " to enter the in-character grid."
        )

    options = [
        { "key": ["(B)ack", "back", "b"],
          "desc": "Go back to profile",
          "goto": "node_human_profile" },
        
        { "key": "Finalize",
          "exec": validate_human,
          "goto": "node_done" }
    ]

    return text, options

# Node 1 Demon
def node_demon_desc(caller):
    text = (
    "Please describe your character using \"desc [your description]\". You can check your"
    " description by using \"look me\". Use |/ for new lines."
    "\nYour description should describe how your demon appears. There are no restrictions"
    " on how your demon may look; it doesn't even have to appear similiar to what a classical"
    " demon looks, just that is monsterous. The restrictions that do exist is that its"
    " height must be between one and ten feet, isn't invisible, and isn't a human."
    "\nYour description should information such as: their stature, heigh, and shape, what they are"
    " covered in (Scales? Feather? Fur? Red skin?), how many limbs they have, any visible"
    " features they have such as wings, clothing (if any), facial features. How would other"
    " characters see your character?"
    "\nNOTE: Mentioning that it is based"
    " on/inspired by pre-existing mythological creatures is acceptable, but please refrain from"
    " based on or saying it inspired by trademarked monsters. Please do not make your character a"
    " replicate of trademarked monsters (however, variations that make it original will be accepted)."
    "\nThe description may be 320 characters long. Longer descriptions are encouraged, however."
    )

    options = [
        { "key": ["(A)dvance", "advance", "a"],
          "desc": "Continue to profile",
          "goto": "node_demon_profile" },
        
        { "key": ["(B)ack", "back", "b"],
          "desc": "Go back to race select",
          "goto": "node_race_select" 
        }
    ]

    return text, options

# Node 2 Demon
def node_demon_profile(caller):
    text = (
    "Please summarize your demon using \"profile [your profile]\". You can check your"
    " profile by using \"+info me\". Use |/ for new lines"
    "\nYour profile is a short summary about your demon, focusing on its non-physical traits"
    " It should tell other players what your demon is; how its dangerous and how it behaves."
    " It should also tell players about your demon's personality, goals, and possibly some"
    " backstory. Who are they, what does it want to do, and why?"
    "\nIt must be 240 characters long. Longer profiles are encouraged, however."

    " It should tell other players about your character is about; what their"
    " personality is like, what they do, and defining characteristics. Who are they?"
    "\nIt must be 240 characters long. Longer profiles are encouarged, however."
    )

    options = [
        { "key": ["(A)dvance", "advance", "a"],
          "desc": "Go to demon abilities",
          "goto": "node_demon_abilities" },
        
        { "key": ["(B)ack", "back", "b"],
          "desc": "Go back to description",
          "goto": "node_demon_desc" }
    ]

    return text, options

# Node 3 Demon
def node_demon_abilities(caller):
    text = (
        "This is where you would select your demon's abilities"
        " to reflect your demon as well as give abilities to use"
        " while dungeon crawling. However, since this feature isn't"
        " implemented yet, feel free to skip to the next section of"
        " chargen."
        )

    options = [
        { "key": ["(A)dvance", "advance", "a"],
          "desc": "Go to validation",
          "goto": "node_demon_validate" },
        
        { "key": ["(B)ack", "back", "b"],
          "desc": "Go back to description",
          "goto": "node_demon_profile" }
    ]

    return text, options

# Node 4 Demon
def node_demon_validate(caller):
    text = (         
        "Type \"finalize\" at any time to finish chargen. Doing this will check"
        " then lengths of both your profile and description. If both are"
        " valid, will change you into a demon character. You'll then be allowed"
        " to enter the in-character grid."
    )

    options = [
        { "key": ["(B)ack", "back", "b"],
          "desc": "Go back to profile",
          "goto": "node_human_profile" },
        
        { "key": "Finalize",
          "desc": "Finishes character generation if everything is valid",
          "exec": validate_demon,
          "goto": "node_done" }
    ]

    return text, options


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