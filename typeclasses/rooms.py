"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    def return_appearance(self, looker):
        visible = (con for con in self.contents if True and
                   con.access(looker, "view"))

        exits, users, things = [], [], []
        
        for con in visible:
            key = con.get_display_name(looker)
            
            if con.destination:
                exits.append(key)
            elif con.has_player:
                # This was originally |c%s|n
                users.append("%s" % key)
            else:
                things.append(key)

        seperator_line = self.format_colour + "-"*78 + "|n\n"

        # get description, build string
        return_string = self.name_colour + "%s|n\n" % self.get_display_name(looker)
        desc = self.db.desc
    
        if desc:
            # Also try |542
            return_string += self.desc_colour + "%s|n\n" % desc 
        else:
            return_string += self.error_colour + "This room has no description|n\n"

        return_string += seperator_line
        return_string += "  " + self.format_colour + "Exits:" + "|n\n"

        if exits:
            return_string += self.hold_colour + "\n".join(exits) + "|n\n"
        else:
            return_string += "|500This room has no exits|n\n"

        if users:
            return_string += seperator_line
            return_string += "  " + self.format_colour + "Players:|n\n"
            return_string += self.hold_colour + ", ".join(users) + "|n\n"

        if things:
            return_string += seperator_line
            return_string += "  " + self.format_colour + "Objects:|n\n"
            return_string += self.hold_colour + ", ".join(things) + "|n\n"


        return_string += seperator_line

        return return_string

    
    def at_object_creation(self):
        self.name_colour   = "|555"
        self.format_colour = "|555"
        self.hold_colour   = "|n"
        self.desc_colour   = "|n"
        self.error_colour  = "|500"



class TestRoom(Room):
    def format_room_appearance(self,
                               looker,
                               title_colour, 
                               format_colour, 
                               object_colour, 
                               desc_colour = "|555",
                               error_colour = "|500"):

        # get and identify all objects
        # (NOTE: replace True with 'con != looker' if you want to not show yourself)
        visible = (con for con in self.contents if True and
                   con.access(looker, "view"))

        exits, users, things = [], [], []
        
        for con in visible:
            key = con.get_display_name(looker)
            
            if con.destination:
                exits.append(key)
            elif con.has_player:
                # This was originally |c%s|n
                users.append("%s" % key)
            else:
                things.append(key)

        seperator_line = format_colour + "-"*78 + "|n\n"

        # get description, build string
        return_string = title_colour + "%s|n\n" % self.get_display_name(looker)
        desc = self.db.desc
    
        if desc:
            # Also try |542
            return_string += desc_colour + "%s|n\n" % desc 
        else:
            return_string += "|500This room has no description|n\n"

        return_string += seperator_line
        return_string += "  " + format_colour + "Exits:" + "|n\n"

        if exits:
            return_string += object_colour + "\n".join(exits) + "|n\n"
        else:
            return_string += "|500This room has no exits|n\n"

        if users:
            return_string += seperator_line
            return_string += "  " + format_colour + "Players:|n\n"
            return_string += object_colour + ", ".join(users) + "|n\n"

        if things:
            return_string += seperator_line
            return_string += "  " + format_colour + "Objects:|n\n"
            return_string += object_colour + ", ".join(things) + "|n\n"


        return_string += seperator_line

        return return_string

    def return_appearance(self, looker):
        if not looker:
            return ""

        orange_xterm = self.format_room_appearance(looker, "|520", "|520", "|540")
        blue_xterm   = self.format_room_appearance(looker, "|015", "|015", "|215")


        seperator = "-"*78 + "\n"

        # room_desc = self.db.desc

        test_colours = "|_\n|_\n|_\n|500" + seperator \
             + "|510" + seperator \
             + "|520" + seperator \
             + "|530" + seperator \
             + "|540" + seperator \
             + "|550" + seperator \
             + "|005" + seperator \
             + "|015" + seperator \
             + "|115" + seperator \
             + "|215" + seperator \
             + "|315" + seperator \
             + "|415" + seperator \
             + "|515" + seperator 

             # + "|105" + seperator \
             # + "|205" + seperator \
             # + "|305" + seperator \
             # + "|405" + seperator \
             # + "|505" + seperator \

        return orange_xterm + "\n" + blue_xterm + test_colours