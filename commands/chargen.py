"""
Chargen

Contains code related for a command-based chargen system

"""
from evennia import default_cmds

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

# Node 0
def node_race_select(caller):
    text = "Please select your race"
    options = [{ "key": ["Demon", "demon"],
            "desc": "You want to be a demon",
            "goto": "node_demon_desc"
        }
    ]
    return text, options

# Node 1 Human
def node_human_desc(caller):
    return "success", [{"key": "_default", "goto": None}]

# Node 2 Human
def node_human_profile(caller):
    return None, None

# Node 3 Human
def node_validate(caller):
    return None, None

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
               cmdset_mergetype = "Replace",
               persistent = False)

from evennia import CmdSet

class CmdSetChargen(CmdSet):
    key = "Chargen"
    def at_cmdset_creation(self): 
        self.add(CmdChargen)