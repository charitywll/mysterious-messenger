init -6 python:
    from datetime import datetime, date, timedelta
    from copy import copy, deepcopy

    ## This defines another voice channel which the emoji
    ## sound effects play on. Players can adjust the volume
    ## of the emojis separately from voice, music, and sfx
    renpy.music.register_channel("voice_sfx", mixer="voice_sfx", loop=False)

    def set_voicesfx_volume(value=None):
        """Set the volume of the voice sfx channel."""

        if value is None:
            return MixerValue('voice_sfx')
        else:
            return SetMixer('voice_sfx', value)

    class CConfirm(Show):
        """A specialized Action for showing confirmation prompts to the player."""

        def __init__(self, msg, yes=None, *args, **kwargs):
            if yes is None:
                yes = Hide('confirm')
                no = None
            else:
                no = Hide('confirm')
                if isinstance(yes, list):
                    yes.insert(0, Hide('confirm'))
                elif yes != Hide('confirm'):
                    yes = [Hide('confirm'), yes]
            super(CConfirm, self).__init__('confirm', None, *args, message=msg,
                yes_action=yes, no_action=no, **kwargs)


    class MyTime(object):
        """
        A class that fetches the current time/date information and stores
        it in easy-to-access fields.

        Attributes:
        -----------
        short_weekday : string
            Shortened name of the day of the week e.g. Mon
        weekday : string
            Full name of the day of the week e.g. Monday
        short_month : string
            Shortened name of the month e.g. Aug
        month : string
            Full name of the day of the month e.g. August
        month_num : string
            Number (1-12) of the month e.g. "8"
        year : string
            Year for the date e.g. "2018"
        day : string
            Day number for the date e.g. "21"
        twelve_hour : string
            Hour in twelve-hour format e.g. "10"
        military_hour : string
            Hour in military format e.g. "22"
        minute : string
            Minute for the time e.g. "32"
        second : string
            Second for the time e.g. "10"
        am_pm : string
            Equal to "PM" or "AM" depending on the time.
        """

        def __init__(self, day=None, thehour=None, themin=None):
            """
            Create a MyTime object to store date and time information.

            Parameters:
            -----------
            day : int
                A number of days (<0 in the past, >0 in the future) to use
                for this object.
            thehour : string
                The hour, in military time, for this timestamp e.g. "23"
            themin : string
                The minutes for this timestamp e.g. "42".
            """

            self.datetime = datetime.now()

            day_diff = 0
            hour_diff = 0
            min_diff = 0

            # Do some calculations for the date, if it's in the past or future
            if day is not None:
                day_diff = day * 60 * 60 * 24
            if thehour is not None:
                hour_diff = int(thehour) - int(self.datetime.strftime('%H'))
                hour_diff = hour_diff * 60 * 60
            if themin is not None:
                min_diff = int(themin) - int(self.datetime.strftime('%M'))
                min_diff = min_diff * 60

            unix_seconds = time.time()
            new_timestamp = unix_seconds + day_diff + hour_diff + min_diff

            self.datetime = datetime.fromtimestamp(new_timestamp)

        @property
        def short_weekday(self):
            return self.datetime.strftime('%a')
        @property
        def weekday(self):
            return self.datetime.strftime('%A')
        @property
        def short_month(self):
            return self.datetime.strftime('%b')
        @property
        def month(self):
            return self.datetime.strftime('%B')
        @property
        def month_num(self):
            return self.datetime.strftime('%m')
        @property
        def year(self):
            return self.datetime.strftime('%Y')
        @property
        def day(self):
            return self.datetime.strftime('%d')
        @property
        def twelve_hour(self):
            return self.datetime.strftime('%I')
        @property
        def military_hour(self):
            return self.datetime.strftime('%H')
        @property
        def minute(self):
            return self.datetime.strftime('%M')
        @property
        def second(self):
            return self.datetime.strftime('%S')
        @property
        def am_pm(self):
            return self.datetime.strftime('%p')


        def get_phone_time(self):
            """Return the time formatted as displayed for phone calls."""

            # Returns a time like 10:15 PM, 25/10
            return (self.twelve_hour + ":" + self.minute
                + " " + self.am_pm + ", " + self.day + "/"
                + self.month_num)

        def get_twelve_hour(self):
            """Return the time formatted as 10:45 AM"""

            return self.twelve_hour + ':' + self.minute + ' ' + self.am_pm

        def get_text_msg_time(self):
            """Return the time formatted for text messages."""

            return (self.day + '/' + self.month_num
                        + '/' + self.year + ' '
                        + self.twelve_hour + ':'
                        + self.minute + self.am_pm)

        def has_occurred(self):
            """
            Return True if this time has already passed compared to
            the current date and time.
            """

            try:
                if self.datetime <= datetime.now():
                    return True
                return False
            except:
                print_file("Could not compare datetime objects")

            cur_time = upTime()
            # Check the year
            if int(self.year) < int(cur_time.year):
                return True
            elif int(self.year) > int(cur_time.year):
                return False
            # Check the month
            if int(self.month_num) < int(cur_time.month_num):
                return True
            elif int(self.month_num) > int(cur_time.month_num):
                return False
            # Check the day
            if int(self.day) < int(cur_time.day):
                return True
            elif int(self.day) > int(cur_time.day):
                return False
            # Check the hour
            if int(self.military_hour) < int(cur_time.military_hour):
                return True
            elif int(self.military_hour) > int(cur_time.military_hour):
                return False
            # Check the minutes
            if int(self.minute) <= int(cur_time.minute):
                return True
            else:
                return False

        def adjust_time(self, td):
            """Adjust the datetime according to timedelta td."""
            self.datetime += td

        @property
        def stopwatch_time(self):
            return self.military_hour + ":" + self.minute + ":" + self.second

    def upTime(day=None, thetime=None):
        """
        Return a MyTime object with the current time, or a time based
        on the given arguments.

        Parameters:
        -----------
        day : None or int
            The number of days in the past (<0) or in the future (>0) this
            timestamp should be created for.
        thetime : string
            A string in the format "00:00" that represents the time this
            timestamp should represent.

        Returns:
        --------
        MyTime
            If day=None, returns a MyTime object representing the current
            date with either the specified time or the given time.
            If thetime=None, the time in the MyTime object will reflect the
            current time.
        """

        if day is not None and thetime is None:
            return MyTime(day)
        elif thetime is not None:
            # Get the hour and minute
            thehour = thetime[:2]
            themin = thetime[-2:]
            return MyTime(day, thehour, themin)
        else:
            return MyTime()

    def new_route_setup(route, chatroom_label='starter_chat', participants=None):
        """Set up variables for a new route."""

        global story_archive, current_timeline_item, starter_story

        if (isinstance(route, store.Route) or isinstance(route, Route)):
            # Got a Route object; use the default route
            try:
                route = route.default_branch
            except AttributeError:
                print_file("Error: Given Route object does not have a default_branch field.")

        if (len(route) > 0
                and (isinstance(route[0], RouteDay)
                    or isinstance(route[0], store.RouteDay))):
            story_archive = route
        else:
            story_archive = route[1:]

        if participants is None:
            participants = []
        define_variables()
        current_timeline_item = ChatRoom('Starter Chat', chatroom_label,
                                        '00:00', participants)
        # This sets a specific variable that lets you have phone calls/
        # VNs for a starter chat/opening
        starter_story = True
        renpy.retain_after_load()
        return

    def hide_all_popups():
        """Hide all popup screens in-game."""

        renpy.hide_screen('text_msg_popup')
        renpy.hide_screen('hide screen text_pop_2')
        renpy.hide_screen('hide screen text_pop_3')
        renpy.hide_screen('hide screen email_popup')
        hide_stackable_notifications()
        hide_heart_icons()

    def btn_hover_img(s):
        """A displayable prefix function to make button hover images."""

        return Fixed(s, Transform(s, alpha=0.5))

    def center_bg_img(s):
        """
        A displayable prefix function to display backgrounds and
        their shake counterparts.
        """

        return Fixed(Image(s, xalign=0.5, yalign=0.5), size=(750,1334))

    def center_crop_bg_img(s):
        """
        A displayable prefix function which crops and centers a background
        image to display as 'shake'.
        """

        return Fixed(Crop((0, (1334-1125)//2, 750, 1125), s,
                    xalign=0.5, yalign=0.5), size=(750,1334))

    def get_text_width(the_text, the_style='default'):
        """Return the width of text with a certain style applied."""
        return int(Text(the_text, style=the_style).size()[0])

    def print_file(*args):
        """Print debug statements to a file for debugging."""

        DEBUG = False
        if DEBUG is None:
            return

        if not DEBUG:
            print(*args)
            return
        # Otherwise, print this to a file for debugging
        try:
            f = open("debug.txt", "a")
            print(*args, file=f)
            f.close()
        except:
            print("Print to file did not work:", args)

    def combine_lists(*args):
        """Combine args into one giant list and return it."""

        result = []
        for arg in args:
            if isinstance(arg, list):
                for pic in arg:
                    if pic not in result:
                        result.append(pic)
            else:
                if arg not in result:
                    result.append(arg)
        return result

    def handle_missing_image(img):
        """Give a generic image to use when an image cannot be found."""
        # Currently unimplemented due to engine bug where the program does not
        # recognize files in the `gui` folder

        print("WARNING: Could not find the image", img)
        renpy.show_screen('script_error',
                message=("Could not find the image " + str(img)))

        return Image('Menu Screens/Main Menu/loading_close.png', size=(100, 100))

    def handle_missing_label(lbl):
        """
        Determine how Ren'Py should proceed if it cannot find the given label.
        """

        if lbl in ['main_menu', '_library_main_menu']:
            return None
        print("WARNING: Could not find the label", lbl)
        renpy.show_screen('script_error',
                message=("Could not find the label " + str(lbl)))

        if lbl == store.current_timeline_item.item_label:
            # Couldn't find this item's correct label; use `just_return` as a
            # replacement since it just returns
            return 'just_return'
        if lbl == store.current_timeline_item.expired_label:
            # Try jumping to the regular, non-expired label
            return store.current_timeline_item.item_label
        # Otherwise, it might be more of an internal issue
        return None

    def change_some_vars():
        """For testing."""
        print("\nbefore: my_test_var", my_test_var, "store.my_test_var", store.my_test_var)
        if store.my_test_var == "Nothing":
            store.my_test_var = "Ping!"
        elif store.my_test_var == "Ping!":
            store.my_test_var = "Pong!"
        else:
            store.my_test_var = "Nothing"
        print("\nafter: my_test_var", my_test_var, "store.my_test_var", store.my_test_var)
        return

    def context_test():
        return
        print("We're in a new context")
        print("The call stack depth is", renpy.call_stack_depth())
        print("Nesting level is", renpy.context_nesting_level())
        print("Current context is", renpy.context())

    config.displayable_prefix["btn_hover"] = btn_hover_img
    config.displayable_prefix["center_bg"] = center_bg_img
    config.displayable_prefix["center_crop_bg"] = center_crop_bg_img

# This tells the program to randomly shuffle the order
# of responses
default shuffle = True
default my_test_var = "Nothing"
## A label the program can jump to in the event it cannot find a
## regular label to jump to
label just_return():
    return

init python:
    # This lets the program shuffle menu options
    renpy_menu = menu
    def menu(items):
        # Copy the items list
        items = list(items)
        global shuffle
        if shuffle and shuffle != "last":
            renpy.random.shuffle(items)
        elif shuffle == "last":
            last = items.pop()
            renpy.random.shuffle(items)
            items.append(last)
        shuffle = True


        # If observing, check which items have already been seen
        if store.observing:
            items = [ i for i in items if i[1].get_chosen() ]
        # For testing
        print_file("List of items is:")
        for i in items:
            print_file("   ", i[0])
        return renpy_menu(items)

    # Don't let the player rollback the game
    # by scrolling
    config.keymap['rollback'].remove('mousedown_4')


# Name of the currently played day, e.g. '1st'
default current_day = False
# Number of the day the player is currently
# going through
default current_day_num = 0
# Number of the day considered 'today'
default today_day_num = 0
# Useful when unlocking the next 24 hours
# of chats in real-time mode
default unlock_24_time = False
# Keeps track of how far the game should
# continue expiring chatrooms
default days_to_expire = 1
# Keeps a record of the current time to compare
# with load times so it knows when to make days
# available
default current_game_day = date.today()
# Lets the program know how to advance days when loading
default persistent.load_instr = False
# List of calls the player can make (outgoing)
default available_calls = []
# History of phone calls
default call_history = []
# If there's an incoming call after a chatroom,
# it will be defined here
default incoming_call = False #e.g. PhoneCall(ju)
# Lets the program know it's in VN mode
default vn_choice = False
# Keeps track of the current call the player is in
default current_call = False
# True if the player is beginning a new game
default starter_story = False
# When expiring items, this is equal to the item being expired
default expiring_item = None

# VN mode preferences
default preferences.afm_time = 15
default preferences.skip_unseen = True
default preferences.skip_after_choices = True

# The automatic save file used by the program
define mm_auto = "mm_auto_save"
# "Unlocks" some developer options for testing
default persistent.testing_mode = False



#************************************
# Chatroom Backgrounds
#************************************

image bg morning = "center_bg:Phone UI/bg-morning.png"
image bg evening = "center_bg:Phone UI/bg-evening.png"
image bg night = "center_bg:Phone UI/bg-night.png"
image bg earlyMorn = "center_bg:Phone UI/bg-earlyMorn.png"
image bg noon = "center_bg:Phone UI/bg-noon.png"

image bg hack = "Phone UI/bg-hack.jpg"
image bg redhack = "Phone UI/bg-redhack.jpg"
image bg redcrack = "Phone UI/bg-redhack-crack.png"

# image morning = "bg morning"
# image evening = "bg evening"
# image night = "bg night"
# image earlyMorn = "bg earlyMorn"
# image noon = "bg noon"

# image hack = "center_crop_bg:bg hack"
# image redhack = "center_crop_bg:bg redhack"
# image redcrack = "center_crop_bg:bg redcrack"
image black = "#000000"

# A starry night background with some static stars;
# used in menu screens
image bg starry_night = "Menu Screens/Main Menu/bg-starry-night.png"
image hack_long = "Phone UI/Hack-Long.png"
image red_hack_long = "Phone UI/Hack-Red-Long.png"
image transparent_img = '#0000'

# ********************************
# Short forms/Startup Variables
# ********************************


# Displays all the messages in a chatroom
default chatlog = []
# A list of the characters currently in the chatroom
default in_chat = []
default current_chatroom = None # old version; unused
default current_timeline_item = ChatRoom('title', 'chatroom_label', '00:00')
# Chat that should be used when saving the game
default most_recent_chat = None # old version; unused
default most_recent_item = None
default name = 'Rainbow'
default hacked_effect = False
# True if the player can receive hourglasses in chatrooms
default persistent.receive_hg = True

# Checks if the player is on a route or not
default persistent.on_route = False
# Checks if it's the first time you've started the game
default persistent.first_boot = True
# Determines if the program should run in real-time or not
default persistent.real_time = False
# Check if the program needs to manually load the chat home screen
default persistent.just_loaded = False


# Set to True if you're viewing a previously-seen chatroom/call/etc
default observing = False

# Detects if you're choosing an option from a menu
# If so, the program uses this variable to disable most buttons
default choosing = False

# Detects if the answer screen should be showing. Useful if you
# view a CG when you should be answering a prompt
default pre_choosing = False

# This keeps track of the sorts of heart points earned over a timeline item
# so it can reset them if the player backs out of it.
default chatroom_hp = None # Old version; unused
default collected_hp = {'good': [], 'bad': [], 'break': []}
# Total number of hg (hourglasses) earned per timeline item
default chatroom_hg = None # Old version; unused
default collected_hg = 0

# Keeps track of the ending the game should show the player
default ending = False

# These are primarily used when setting the nickname colour
# via $ nickColour = black or $ nickColour = white
define white = "#ffffff"
define black = "#000000"

image new_sign = "Bubble/main01_new.png"

define _preferences.show_empty_window = False



#************************************
# Persistent Variables
#************************************

default persistent.pronoun = "non binary"

default persistent.MC_pic = 'Profile Pics/MC/MC-1.png'
default persistent.name = "Rainbow"

default persistent.HP = 0
default persistent.HG = 100



##******************************
## Image Definitions - Menu
##******************************



image greeting_bubble = Frame("Menu Screens/Main Menu/greeting_bubble.png", 40, 10, 10, 10)
image greeting_panel = Frame("Menu Screens/Main Menu/greeting_panel.png", 20, 20)

image rfa_greet:
    Text("{k=-1}>>>>>>>{/k}  Welcome to Rika's Fundraising Association",
                color="#ffffff", size=30, slow=True,
                font=curlicue_font, slow_cps=8, bold=True)
    10.0
    "transparent"
    0.2
    repeat

# Background Menu Squares
image right_corner_menu = Frame("Menu Screens/Main Menu/right_corner_menu.png", 45, 45)
image right_corner_menu_hover = Transform('right_corner_menu', alpha=0.5)
image left_corner_menu = Frame("Menu Screens/Main Menu/left_corner_menu.png", 45, 45)
image left_corner_menu_hover = Transform('left_corner_menu', alpha=0.5)

# Menu Icons
image menu_after_ending = "Menu Screens/Main Menu/after_ending.png"
image menu_dlc = "Menu Screens/Main Menu/dlc.png"
image menu_history = "Menu Screens/Main Menu/history.png"
image menu_save_load = "Menu Screens/Main Menu/save_load.png"
image menu_original_story = "Menu Screens/Main Menu/original_story.png"

# Settings panel
image menu_settings_panel = Frame("Menu Screens/Main Menu/settings_sound_panel.png",60,200,60,120)
image menu_settings_panel_bright = Frame("Menu Screens/Main Menu/settings_sound_panel_bright.png",60,200,60,120)
image menu_settings_panel_light = Frame("Menu Screens/Main Menu/settings_sound_panel_light.png",60,200,60,120)
image menu_sound_sfx = "Menu Screens/Main Menu/settings_sound_sfx.png"
image menu_other_box = Frame("Menu Screens/Main Menu/settings_sound_sfx.png", 10, 10)
image menu_ringtone_box = Frame("Menu Screens/Main Menu/daychat01_3.png", 35, 35)

# Settings tabs
image menu_tab_inactive = Frame("Menu Screens/Main Menu/settings_tab_inactive.png",10,10)
image menu_tab_inactive_hover2 = Frame("Menu Screens/Main Menu/settings_tab_inactive_hover2.png",10,10)
image menu_tab_active = Frame("Menu Screens/Main Menu/settings_tab_active.png",25,25)
image menu_tab_inactive_hover = Frame("Menu Screens/Main Menu/settings_tab_inactive_hover.png",10,10)

# Header Images
image header_plus = "Menu Screens/Main Menu/header_plus.png"
image header_plus_hover = "Menu Screens/Main Menu/header_plus_hover.png"
image header_tray = "Menu Screens/Main Menu/header_tray.png"
image header_hg = "Menu Screens/Main Menu/header_hg.png"
image header_heart = "Menu Screens/Main Menu/header_heart.png"

# Profile Page
image menu_header = Frame("Menu Screens/Main Menu/menu_header.png", 0, 50)
image menu_back = "Menu Screens/Main Menu/menu_back_btn.png"
image save_btn = "Menu Screens/Main Menu/menu_save_btn.png"
image load_btn = "Menu Screens/Main Menu/menu_load_btn.png"
image name_line = "Menu Screens/Main Menu/menu_underline.png"
image menu_edit = "Menu Screens/Main Menu/menu_pencil_long.png"
image menu_pencil = "Menu Screens/Main Menu/menu_pencil.png"

image radio_on = "Menu Screens/Main Menu/menu_radio_on.png"
image radio_off = "Menu Screens/Main Menu/menu_radio_off.png"

image settings_gear = "Menu Screens/Main Menu/menu_settings_gear.png"

# Save/Load
image save_auto_idle = Frame("Menu Screens/Main Menu/save_auto_idle.png", 20, 20)
image save_auto_hover = Frame("btn_hover:save_auto_idle", 20, 20)


# Just for fun, this is the animation when you hover over the settings
# button. It makes the gear look like it's turning
image settings_gear_rotate:
    "Menu Screens/Main Menu/menu_settings_gear.png"
    xpos -10
    ypos -10
    block:
        rotate 0
        linear 1.0 rotate 45
        repeat

# Other Settings
image menu_select_btn = Frame("Menu Screens/Main Menu/menu_select_button.png",60, 70, 130, 60)
image menu_select_btn_hover = Transform('menu_select_btn', alpha=0.5)
image menu_select_btn_inactive = Frame("Menu Screens/Main Menu/menu_select_button_inactive.png",60,60)


## ********************************
## Chat Home Screen
## ********************************

image gray_chatbtn = "Menu Screens/Chat Hub/main01_chatbtn.png"
image gray_chatbtn_hover = "btn_hover:gray_chatbtn"
image rfa_chatcircle:
    "Menu Screens/Chat Hub/main01_chatcircle.png"
    block:
        rotate 0
        alignaround(.5, .5)
        linear 13.0 rotate -360
        repeat
image blue_chatcircle:
    "Menu Screens/Chat Hub/main01_chatcircle_big.png"
    block:
        rotate 60
        alignaround(.5, .5)
        linear 4 rotate 420
        repeat

image chat_icon = "Menu Screens/Chat Hub/main01_chaticon.png"
image gray_mainbtn = "Menu Screens/Chat Hub/main01_mainbtn.png"
image gray_mainbtn_hover = "btn_hover:gray_mainbtn"
image blue_mainbtn = "Menu Screens/Chat Hub/main01_mainbtn_lit.png"
image blue_mainbtn_hover = 'btn_hover:blue_mainbtn'
image gray_maincircle:
    "Menu Screens/Chat Hub/main01_maincircle.png"
    block:
        rotate -120
        alignaround(.5, .5)
        linear 4 rotate -480
        repeat
image blue_maincircle:
    "Menu Screens/Chat Hub/main01_maincircle_lit.png"
    block:
        rotate 180
        alignaround(.5, .5)
        linear 4 rotate 540
        repeat
image call_mainicon = "Menu Screens/Chat Hub/main01_mainicon_call.png"
image email_mainicon = "Menu Screens/Chat Hub/main01_mainicon_email.png"
image msg_mainicon = "Menu Screens/Chat Hub/main01_mainicon_message.png"

image profile_pic_select_square = Transform("Menu Screens/Chat Hub/profile_pic_select_square.png", size=(95, 95))

image white_hex = "Menu Screens/Chat Hub/main01_subbtn.png"
image blue_hex = "Menu Screens/Chat Hub/main01_subbtn_lit.png"
image red_hex = "Menu Screens/Chat Hub/main01_subbtn_shop.png"
image white_hex_hover = 'btn_hover:white_hex'
image blue_hex_hover = 'btn_hover:blue_hex'
image red_hex_hover = 'btn_hover:red_hex'

image album_icon = "Menu Screens/Chat Hub/main01_subicon_album.png"
image guest_icon = "Menu Screens/Chat Hub/main01_subicon_guest.png"

image loading_circle_stationary = "Menu Screens/Main Menu/loading_circle.png"

## ********************************
## Profile Picture Screen
## ********************************
image profile_outline = Frame('#fff', 5, 5)
image profile_cover_photo = "Cover Photos/profile_cover_photo.png"


image input_close = "Menu Screens/Main Menu/main02_close_button.png"
image input_close_hover = "Menu Screens/Main Menu/main02_close_button_hover.png"
image input_square = Frame("Menu Screens/Main Menu/main02_text_input.png",40,40)
image input_popup_bkgr = Frame("Menu Screens/Main Menu/menu_popup_bkgrd.png",70,70)
image input_popup_bkgr_hover = Frame("Menu Screens/Main Menu/menu_popup_bkgrd_hover.png",70,70)




## ********************************
## Text Message Screen
## ********************************

image new_text_envelope = 'Text Messages/main03_email_unread.png'
image read_text_envelope = 'Text Messages/main03_email_read.png'
image new_text = 'Text Messages/new_text.png'
image header_envelope = 'Text Messages/header_envelope.png'

image message_idle_bkgr = Frame('Text Messages/message_idle_background.png',20,20,20,20)
image message_hover_bkgr = 'btn_hover:message_idle_bkgr'
image unread_message_idle_bkgr = Frame('Text Messages/message_idle_background_unread.png',20,20,20,20)
image unread_message_hover_bkgr = 'btn_hover:unread_message_idle_bkgr'

image text_msg_line = Frame('Text Messages/msgsl_line.png', 40,2)
image text_answer_active = 'Text Messages/msgsl_button_answer_active.png'
image text_answer_inactive = 'Text Messages/msgsl_button_answer_inactive.png'
image text_answer_text = 'Text Messages/msgsl_text_answer.png'
image text_answer_animation:
    'Text Messages/answer_animation/1.png'
    0.1
    'Text Messages/answer_animation/2.png'
    0.1
    'Text Messages/answer_animation/3.png'
    0.1
    'Text Messages/answer_animation/4.png'
    0.1
    'Text Messages/answer_animation/5.png'
    0.1
    'Text Messages/answer_animation/6.png'
    0.1
    'Text Messages/answer_animation/7.png'
    0.1
    'Text Messages/answer_animation/8.png'
    0.1
    'Text Messages/answer_animation/9.png'
    0.1
    'Text Messages/answer_animation/10.png'
    0.1
    'Text Messages/answer_animation/11.png'
    0.1
    'Text Messages/answer_animation/12.png'
    0.1
    'Text Messages/answer_animation/13.png'
    0.1
    'Text Messages/answer_animation/14.png'
    0.1
    'Text Messages/answer_animation/15.png'
    0.1
    'Text Messages/answer_animation/16.png'
    0.1
    'Text Messages/answer_animation/17.png'
    0.1
    repeat

image text_pause_button = 'Text Messages/msgsl_text_pause.png'
image text_play_button = 'Text Messages/msgsl_text_play.png'

image text_popup_bkgr = "Text Messages/msgsl_popup_edge.png"
image text_popup_msg = Frame("Text Messages/msgsl_popup_text_bg.png", 0,0)
image text_answer_idle = "Text Messages/chat-bg02_2.png"
image text_answer_hover = "Text Messages/chat-bg02_3.png"
image new_text_count = "Text Messages/new_msg_count.png"

image mc_text_msg_bubble = Frame("Text Messages/msgsl_text_player.png", 60,60,60,10)
image npc_text_msg_bubble = Frame("Text Messages/msgsl_text_npc.png", 60,60,60,10)


## ********************************
## Chat Select Screen
## ********************************

image day_selected = Frame('Menu Screens/Day Select/daychat01_day_mint.png', 50, 50)
image day_selected_hover = Frame('Menu Screens/Day Select/daychat01_day_mint_hover.png', 50, 50)
image day_inactive = Frame('Menu Screens/Day Select/daychat01_day_inactive.png', 50, 50)
image day_active = Frame('Menu Screens/Day Select/daychat01_day_active.png', 50, 50)
image day_active_hover = Frame('Menu Screens/Day Select/daychat01_day_active_hover.png', 50, 50)
image day_reg_hacked = 'Menu Screens/Day Select/chatlist_hacking.png'
image day_reg_hacked_long = 'Menu Screens/Day Select/chatlist_hacking_long.png'

image chat_hack_thin = 'Menu Screens/Day Select/chat_hacking_thin.png'
image chat_hack_thick = 'Menu Screens/Day Select/chat_hacking_thick.png'
image chat_hack_filled = 'Menu Screens/Day Select/chat_hacking_filled.png'

image hacked_white_squares:

    block:
        choice:
            Transform('chat_hack_thin', yzoom=0.3, alpha=0.4, yoffset=800)
            pause 0.02
            Transform('chat_hack_thin', yzoom=0.3, alpha=0.0, yoffset=800)
            pause 0.02
        choice:
            Transform('chat_hack_thin', yzoom=0.3, alpha=0.4, yoffset=800)
            pause 0.02
            Transform('chat_hack_thin', yzoom=0.3, alpha=0.0, yoffset=800)
            pause 0.02
        choice:
            Transform('chat_hack_thin', yzoom=0.01, alpha=0.45, yoffset=720)
            pause 0.02
            Transform('chat_hack_thin', yzoom=1.0, alpha=0.95, yalign=0.6)
            pause 0.02
    block:
        choice:
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.9, yalign=1.0)
            pause 0.02
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.0, yalign=1.0)
            pause 0.03
        choice:
            Transform('chat_hack_thin', yzoom=1.0, alpha=0.95, yalign=0.6)
            pause 0.02
            Transform('chat_hack_filled', yzoom=0.3, alpha=0.8, yalign=1.0)
            pause 0.02
        choice:
            Transform('chat_hack_thick', yzoom=0.3, alpha=0.98, yalign=0.5)
            pause 0.02
            Transform('chat_hack_thick', yzoom=0.3, alpha=0.0, yalign=0.5)
            pause 0.04
    block:
        choice:
            Transform('chat_hack_thin', yzoom=1.0, alpha=0.95, yalign=0.6)
            pause 0.02
            Transform('chat_hack_filled', yzoom=0.4, alpha=0.8, yalign=0.85)
            pause 0.02
        choice:
            Transform('chat_hack_thin', yzoom=1.0, alpha=0.95, yalign=0.6)
            pause 0.02
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.9, yalign=1.0)
            pause 0.02
        choice:
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.0, yalign=1.0)
            pause 0.05
            Transform('chat_hack_thick', yzoom=0.3, alpha=0.98, yalign=0.5)
            pause 0.02
    block:
        choice:
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.0, yalign=1.0)
            pause 0.1
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.9, yalign=1.0)
            pause 0.02
        choice:
            Transform('chat_hack_thick', yzoom=0.3, alpha=0.98, yalign=0.5)
            pause 0.02
            Transform('chat_hack_thick', yzoom=0.1, alpha=0.7, yalign=0.6)
            pause 0.02
        choice:
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.0, yalign=1.0)
            pause 0.05
            Transform('chat_hack_filled', yzoom=0.4, alpha=0.5, yalign=0.85)
            pause 0.02
    block:
        choice:
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.0, yalign=1.0)
            pause 0.1
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.9, yalign=1.0)
            pause 0.02
        choice:
            Transform('chat_hack_thick', yzoom=0.3, alpha=0.98, yalign=0.5)
            pause 0.02
            Transform('chat_hack_thick', yzoom=0.1, alpha=0.7, yalign=0.6)
            pause 0.02
        choice:
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.0, yalign=1.0)
            pause 0.05
            Transform('chat_hack_filled', yzoom=0.4, alpha=0.5, yalign=0.85)
            pause 0.02
    block:
        choice:
            Transform('chat_hack_thin', yzoom=1.0, alpha=0.95, yalign=0.6)
            pause 0.02
            Transform('chat_hack_filled', yzoom=0.4, alpha=0.8, yalign=0.85)
            pause 0.02
        choice:
            Transform('chat_hack_thin', yzoom=1.0, alpha=0.95, yalign=0.6)
            pause 0.02
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.9, yalign=1.0)
            pause 0.02
        choice:
            Transform('chat_hack_filled', yzoom=0.45, alpha=0.0, yalign=1.0)
            pause 0.05
            Transform('chat_hack_thick', yzoom=0.3, alpha=0.98, yalign=0.5)
            pause 0.02
    block:
        choice:
            Transform('chat_hack_thin', yzoom=0.3, alpha=0.4, yoffset=800)
            pause 0.02
            Transform('chat_hack_thin', yzoom=0.3, alpha=0.0, yoffset=800)
            pause 0.02
        choice:
            Transform('chat_hack_thin', yzoom=0.3, alpha=0.4, yoffset=800)
            pause 0.02
            Transform('chat_hack_thin', yzoom=0.3, alpha=0.0, yoffset=800)
            pause 0.02
        choice:
            Transform('chat_hack_thin', yzoom=0.01, alpha=0.45, yoffset=720)
            pause 0.02
            Transform('chat_hack_thin', yzoom=1.0, alpha=0.95, yalign=0.6)
            pause 0.02
    Transform('chat_hack_filled', yzoom=0.4, alpha=0.0, yalign=0.85)



image day_today:
    'Menu Screens/Day Select/daychat_today.png'
    block:
        easein 0.5 yoffset -20
        easeout 0.5 yoffset 0
        repeat
image final_day = 'Menu Screens/Day Select/daychat_finalday.png'
image day_percent = Frame('Menu Screens/Day Select/daychat_percent.png', 15, 15)
image day_percent_bg = Frame('Menu Screens/Day Select/daychat_percent_bg.png', 15, 15)
image day_percent_border = Frame('Menu Screens/Day Select/daychat_percent_border.png', 15, 15)
image day_hlink = 'Menu Screens/Day Select/daychat_hlink.png'
image plot_lock = 'Menu Screens/Day Select/plot_lock.png'
image expired_chat = 'Menu Screens/Day Select/daychat_hg.png'

image day_vlink = Tile('Menu Screens/Day Select/daychat_vlink.png')
image vn_inactive = 'Menu Screens/Day Select/vn_inactive.png'
image vn_selected = 'Menu Screens/Day Select/daychat01_vn_mint.png'
image vn_active = 'Menu Screens/Day Select/vn_active.png'
image vn_selected_hover = 'Menu Screens/Day Select/daychat01_vn_mint_hover.png'
image vn_active_hover = 'Menu Screens/Day Select/vn_active_hover.png'
image vn_inactive_hover = 'vn_inactive'
image vn_marker = 'Menu Screens/Day Select/daychat01_vn_marker.png'
image vn_time_bg = 'Menu Screens/Day Select/daychat01_chat_timebg.png'

image solo_vn_active = "Menu Screens/Day Select/solo_vn_active.png"
image solo_vn_inactive = "Menu Screens/Day Select/solo_vn_inactive.png"
image solo_vn_selected = "Menu Screens/Day Select/solo_vn_mint.png"
image solo_vn_hover = "Menu Screens/Day Select/solo_vn_hover.png"

image chat_active = Frame('Menu Screens/Day Select/daychat01_chat_active.png',190, 70, 40, 50)
image chat_inactive = Frame('Menu Screens/Day Select/daychat01_chat_inactive.png',190, 70, 40, 50)
image chat_continue = Frame('Menu Screens/Day Select/daychat01_chat_continue.png',190, 70, 40, 20)
image chat_selected = Frame('Menu Screens/Day Select/daychat01_chat_mint.png',190, 70, 40, 50)
image chat_timeline_hover = Frame('Menu Screens/Day Select/daychat01_chat_hover.png', 190, 70, 40, 50)

image story_call_active = Frame('Menu Screens/Day Select/story_call_active.png', 290, 56, 40, 50)
image story_call_inactive = Frame('Menu Screens/Day Select/story_call_inactive.png', 290, 56, 40, 50)
image story_call_selected = Frame('Menu Screens/Day Select/story_call_mint.png', 290, 56, 40, 50)
image story_call_hover = Frame('Menu Screens/Day Select/story_call_hover.png', 290, 56, 40, 50)
image story_call_history = 'Menu Screens/Day Select/story_call_history.png'

## ********************************
## Phone Call Screen
## ********************************

image call_back = 'Phone Calls/call.png'

image call_signal_sl:
    Transform('Phone Calls/call_ani_0.png', xzoom=-1)
    block:
        alpha 0.0
        1.0
        alpha 0.8
        3.0
        repeat
image call_signal_ml:
    Transform('Phone Calls/call_ani_1.png', xzoom=-1)
    block:
        alpha 0.0
        2.0
        alpha 0.8
        2.0
        repeat
image call_signal_ll:
    Transform('Phone Calls/call_ani_2.png', xzoom=-1)
    block:
        alpha 0.0
        3.0
        alpha 0.8
        1.0
        repeat
image call_signal_sr:
    'Phone Calls/call_ani_0.png'
    block:
        alpha 0.0
        1.0
        alpha 0.8
        3.0
        repeat
image call_signal_mr:
    'Phone Calls/call_ani_1.png'
    block:
        alpha 0.0
        2.0
        alpha 0.8
        2.0
        repeat
image call_signal_lr:
    'Phone Calls/call_ani_2.png'
    block:
        alpha 0.0
        3.0
        alpha 0.8
        1.0
        repeat

image call_overlay = Frame('Phone Calls/call_back_screen.png', 0, 0)
image call_answer = 'Phone Calls/call_button_answer.png'
image call_hang_up = 'Phone Calls/call_button_hang_up.png'
image call_pause = 'Phone Calls/call_button_pause.png'
image call_play = 'Phone Calls/call_button_play.png'
image call_replay_active = 'Phone Calls/call_button_replay_active.png'
image call_replay_inactive = 'Phone Calls/call_button_replay_inactive.png'
image call_connect_triangle = 'Phone Calls/call_connect_waiting.png'

image contact_icon = 'Phone Calls/call_icon_contacts.png'
image call_headphones = 'Phone Calls/call_icon_earphone_en.png'
image call_history_icon = 'Phone Calls/call_icon_history.png'
image call_incoming = 'Phone Calls/call_icon_incoming.png'
image call_missed = 'Phone Calls/call_icon_missed.png'
image call_outgoing = 'Phone Calls/call_icon_outgoing.png'
image call_voicemail = 'Phone Calls/call_icon_voicemail.png'

image call_choice = Frame('Phone Calls/call_select_button.png', 70, 70)
image call_choice_hover = Frame('Phone Calls/call_select_button_hover.png', 90, 90)

image call_choice_check = Frame('Phone Calls/call_select_button_check.png', 70, 70)
image call_choice_check_hover = Frame('Phone Calls/call_select_button_hover_check.png', 90, 90)



## ********************************
## Email Screen
## ********************************

image email_completed_3 = "Email/main03_email_completed_01.png"
image email_completed_2 = "Email/main03_completed_02.png"
image email_completed_1 = "Email/main03_completed_03.png"
image email_failed = "Email/main03_email_failed.png"
image email_timeout = "Email/main03_email_timeout.png"
image email_good = "Email/main03_email_good.png"
image email_bad = "Email/main03_email_bad.png"
image email_inactive = "Email/main03_email_inactive.png"
image email_panel = "Email/main03_email_panel.png"
image email_read = "Email/main03_email_read.png"
image email_replied = "Email/main03_email_replied.png"
image email_unread = "Email/main03_email_unread.png"
image email_next = "Email/main03_email_next_button.png"
image email_mint = "Email/main03_email_mint.png"
image white_transparent = Frame("Email/white_transparent.png", 0, 0)
image email_open_transparent = Frame("Email/email_open_transparent.png", 0, 0)
image left_corner_menu_dark = Frame("Email/left_corner_menu_dark.png", 45, 45)

