# ######################################################
# This file contains many of the primary menu screens
# used throughout the game. It's organized as follows:
#   python definitions:
#       class NameInput(InputValue)
#       def chat_greet(hour, greet_char)
#       def set_pronouns()
#   variable definitions
#   screen main_menu()
#       screen route_select_screen()
#   screen save/load
#       screen file_slots(title)
#   screen menu_header(title, return_action, envelope)
#   screen chat_home(reshow)
#       screen chara_profile(who)   
# ######################################################


init python:

    import time

    # Used to get the player's name from input
    class NameInput(InputValue):
        def __init__(self):
            self.the_name = "Rainbow"
                                    
        def get_text(self):
            global persistent
            return persistent.name
            
        def set_text(self, s):
            s = s.strip()  
            self.the_name = s       
            global name, m, persistent
            # Ensure the given name is valid
            if (len(s) < 2
                    or not has_alpha(s)
                    or not has_valid_chars(s)):
                # renpy.show_screen('notify', 
                #     message=("Names must be between 2 and 20 characters long"
                #     + " and can only contain alphabet characters, dashes,"
                #     + " spaces, and apostrophes."))
                pass
            else:
                persistent.name = self.the_name
                renpy.save_persistent()
                name = persistent.name  
                m.name = name 
                renpy.retain_after_load()  
            
        def enter(self):
            global name, m, persistent
            if (len(self.the_name) < 2
                    or not has_alpha(self.the_name)
                    or not has_valid_chars(self.the_name)):
                renpy.show_screen('notify', 
                    message=("Names must be between 2 and 20 characters long"
                    + " and can only contain alphabet characters, dashes,"
                    + " spaces, and apostrophes."))
            else:
                persistent.name = self.the_name
                renpy.save_persistent()
                name = persistent.name  
                m.name = name 
                renpy.retain_after_load()  
                renpy.hide_screen('input_popup')
            # renpy.run(self.Disable())                
            # raise renpy.IgnoreEvent()
            
    ## Checks if the given string has at least one letter from the alphabet
    def has_alpha(mystring):
        for c in "aeiouyAEIOUYbcdfghjklmnpqrstvwxzBCDFGHJKLMNPQRSTVWXZ":
            if c in mystring:
                return True
        return False

    ## Ensures the given string only includes alphabet characters and 
    ## spaces, dashes, or apostrophes
    def has_valid_chars(mystring):
        for c in mystring:
            if c not in " -'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                return False
        return True
        
    ## This picks a greeting depending on the time of day and plays it
    ## Makes use of a class called Day_Greeting to find sound clips and the 
    ## corresponding translations
    def chat_greet(hour, greet_char):  
        global greeted, greet_text_english, greet_text_korean
        greeted = True
        greet_text_english = "Welcome to my Mystic Messenger Generator!"
        
        if hour >= 6 and hour < 12:  # morning
            greet_text_english = "Good morning! " + greet_text_english
            
            num_greetings = len(morning_greeting[greet_char])
            the_greeting = renpy.random.randint(1, num_greetings) - 1
            # If translations were included, the text would be set like this
            # greet_text_english = morning_greeting[greet_char][the_greeting].english
            # greet_text_korean = morning_greeting[greet_char][the_greeting].korean
            renpy.play(morning_greeting[greet_char][the_greeting].sound_file, channel="voice_sfx")
            
        elif hour >=12 and hour < 18:    # afternoon
            greet_text_english = "Good afternoon! " + greet_text_english
            
            num_greetings = len(afternoon_greeting[greet_char])
            the_greeting = renpy.random.randint(1, num_greetings) - 1
            renpy.play(afternoon_greeting[greet_char][the_greeting].sound_file, channel="voice_sfx")
            
        elif hour >= 18 and hour < 22:  # evening
            greet_text_english = "Good evening! " + greet_text_english
            
            num_greetings = len(evening_greeting[greet_char])
            the_greeting = renpy.random.randint(1, num_greetings) - 1
            renpy.play(evening_greeting[greet_char][the_greeting].sound_file, channel="voice_sfx")
            
        elif hour >= 22 or hour < 2: # night
            greet_text_english = "It's getting late! " + greet_text_english
            
            num_greetings = len(night_greeting[greet_char])
            the_greeting = renpy.random.randint(1, num_greetings) - 1
            renpy.play(night_greeting[greet_char][the_greeting].sound_file, channel="voice_sfx")
            
        else:   # late night/early morning
            greet_text_english = "You're up late! " + greet_text_english
            
            num_greetings = len(late_night_greeting[greet_char])
            the_greeting = renpy.random.randint(1, num_greetings) - 1
            renpy.play(late_night_greeting[greet_char][the_greeting].sound_file, channel="voice_sfx")
        
        
    # Sets the player's pronouns, if they change them
    def set_pronouns():
        global they, them, their, theirs, themself, they_re
        global They, Them, Their, Theirs, Themself, They_re
        global is_are, has_have, s_verb
        if persistent.pronoun == "female":
            they = "she"
            them = "her"
            their = "her"
            theirs = "hers"
            themself = "herself"
            they_re = "she's"
            They_re = "She's"
            They = "She"
            Them = "Her"
            Their = "Her"
            Theirs = "Hers"
            Themself = "Herself"   
            is_are = "is"
            has_have = "has"
            s_verb = "s"
        elif persistent.pronoun == "male":
            they = "he"
            them = "him"
            their = "his"
            theirs = "his"
            themself = "himself"
            they_re = "he's"
            They_re = "He's"
            They = "He"
            Them = "Him"
            Their = "His"
            Theirs = "His"
            Themself = "Himself"
            is_are = "is"
            has_have = "has"
            s_verb = "s"
        elif persistent.pronoun == "non binary":
            they = "they"
            them = "them"
            their = "their"
            theirs = "theirs"
            themself = "themself"
            they_re = "they're"
            They_re = "They're"
            They = "They"
            Them = "Them"
            Their = "Their"
            Theirs = "Theirs"
            Themself = "Themself"
            is_are = "are"
            has_have = "have"
            s_verb = ""
        renpy.retain_after_load()

    # Ensures the player's name and profile picture are correctly set
    def set_name_pfp():
        global name, persistent, m
        name = persistent.name
        if m.prof_pic != persistent.MC_pic and isImg(persistent.MC_pic):
            m.prof_pic = persistent.MC_pic
        else:
            m.prof_pic = 'Profile Pics/MC/MC-1.png'
        if m.name != persistent.name:
            m.name = persistent.name
        renpy.retain_after_load()
        return
      
            

# Variable to help determine when there should be Honey Buddha
# Chips available
default hbc_bag = RandomBag([ False, False, False, 
                              False, False, True, True ])

# This lets it randomly pick a profile picture to display        
default greet_char = "s"
define greet_list = ['ja', 'ju', 'sa', 'ri', 's', 
                                 'u', 'v', 'y', 'z']

# Greeting Text
# (Eventually these will be stored in the Day_Greet object to be
# pulled alongside the sound file)
default greet_text_korean = "제 프로그램으로 환영합니다!"
default greet_text_english = "Welcome to my Mystic Messenger Generator!"

# A variable that keeps track of whether or not the player has been "greeted"
# in order to prevent it from constantly greeting you when you switch screens
default greeted = False


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
## Also shows a greeting from a random character
##

screen main_menu():

    tag menu
    
    python:    
        # This if statement just makes sure the menu music isn't
        # constantly restarting
        if renpy.music.get_playing(channel='music') != mystic_chat:
            renpy.music.play(mystic_chat, loop=True)
                               
        hour = time.strftime('%H', time.localtime())
        hour = int(hour)    # gets the hour, makes it an int
        greet_char = renpy.random.choice(greet_list)
        if not greeted:
            chat_greet(hour, greet_char)
        
    
    # This adds the 'starry night' background with a few animated stars
    # You can see the background defined in 'starry night bg.rpy'
    use starry_night()
        
        
    ## Greeting Bubble/Dialogue
    add "rfa_greet" yalign 0.01 xalign 0.25 
    
    window:
        xysize(670,140)
        xpos 380
        ypos 260
        add "greeting_panel"
        
    hbox:
        window:
            xysize(143,127)
            add 'greet [greet_char]':
                xpos 65 ypos 140
        window:
            xysize(500,120)
            xpos 305
            ypos 250
            add "greeting_bubble"
    
    window:
        style "greet_box"
        text "{size=-2}" + "[greet_text_korean]" + "{/size}" style "greet_text"
        text "[greet_text_english]" style "greet_text" yalign 0.5

    
    # The main menu buttons. Note that some currently don't take
    # you to the screen you'd want as those features have yet to be added
    window:
        xysize(695, 650)
        xalign 0.6
        yalign 0.62
        vbox:
            hbox:
                window:
                    xysize(450,420)
                    padding (10, 10)
                    # Original Story
                    # Top left
                    button:
                        xysize(430,400)
                        focus_mask True
                        background "left_corner_menu"
                        hover_foreground 'left_corner_menu_hover'
                        activate_sound "audio/sfx/UI/select_4.mp3"
                        if persistent.on_route:
                            # This is the auto save that gets loaded every 
                            # time you load the game
                            action [SetField(persistent, 'just_loaded', True),
                                    FileLoad(mm_auto)]  
                        else:
                            # Note: this screen only has a placeholder
                            # but can easily be customized (see below)
                            action Show('route_select_screen') 
                        
                        vbox:    
                            align(0.5, 0.5)
                            add "menu_original_story" xpos 20
                            text "Original\nStory":
                                style "menu_text_big"  
                                ypos 15
                
                vbox:
                    window:
                        xysize(225, 210)
                        padding (10, 10)
                        # Save and Load
                        # Top Right
                        button:
                            xysize(205, 190)
                            focus_mask True
                            background "right_corner_menu" 
                            hover_foreground 'right_corner_menu_hover'
                            action Show("load")    
                            
                            vbox:                               
                                align(0.5, 0.5)
                                add "menu_save_load" xpos 25
                                text "Save & Load":
                                    style "menu_text_small" 
                                    ypos 10
                            
                    window:
                        xysize(225, 210)
                        padding (10, 10)
                        # After Ending
                        # Mid Right
                        button:
                            xysize(205, 190)
                            focus_mask True
                            background "right_corner_menu" 
                            hover_foreground 'right_corner_menu_hover'
                            # action NullAction                            
                            vbox:                               
                                xcenter 0.5
                                ycenter 0.5
                                add "menu_after_ending" xpos 40
                                text "After Ending":
                                    style "menu_text_small" 
                                    ypos 20
            hbox:
                window:
                    xysize(450,210)
                    padding (10, 10)
                    # History
                    # Bottom Left
                    button:
                        xysize(430,190)
                        focus_mask True
                        background "left_corner_menu"
                        hover_foreground "left_corner_menu_hover"
                        action Show('select_history', Dissolve(0.5))                 
                        vbox:                               
                            align(0.5, 0.5)
                            add "menu_history" xpos 15 ypos 3
                            text "History" style "menu_text_big" ypos 13
                    
                window:
                    xysize(225, 210)
                    padding (10, 10)
                    # DLC
                    # Bottom Right
                    button:
                        xysize (205,190)
                        focus_mask True
                        background "right_corner_menu" 
                        hover_foreground 'right_corner_menu_hover'
                        # action Show('create_archive') 
                        # Leads to the create-a-chatroom screens
                        
                        vbox:                               
                            align(0.5, 0.5)
                            add "menu_dlc"
                            text "DLC" style "menu_text_small" xpos 25 ypos 15
     
     

    
    
## A short, not completely implemented screen where you select
## which route you'd like to start on. Can be customized to lead
## the player to a route to select, but as of now simply starts
## the game
screen route_select_screen():

    tag menu

    use menu_header("Mode Select", Show('main_menu', Dissolve(0.5))):
        fixed:   
            xysize (720, 1170)
            yalign 1.0
            xalign 0.5  
            window:
                xysize(700, 350)
                padding (10, 10)
                xalign 0.5
                yalign 0.4
                button:
                    focus_mask True
                    background 'right_corner_menu'
                    hover_foreground 'right_corner_menu_hover'
                    # Note that here we tell the program which "route"
                    # we'd like the player to be on -- in this case,
                    # tutorial_good_end, without the title (which is why
                    # we need to follow it with [1:])
                    action [SetVariable('chat_archive', tutorial_good_end[1:]),
                            Function(set_pronouns), Function(set_name_pfp),
                            Start()]         
                text 'Start Game':
                    style 'menu_text_small' 
                    xalign 0.5 
                    yalign 0.5
        

  
## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##

screen save():

    tag save_load
    modal True

    use menu_header("Save", Hide('save', Dissolve(0.5))):
        use file_slots(_("Save"))

screen load():

    tag save_load
    modal True
    
    use menu_header("Load", Hide('load', Dissolve(0.5))):
        use file_slots(_("Load"))

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), 
                        auto=_("Automatic saves"), quick=_("Quick saves"))
        
    default the_day = "1st"
    
    python:      
        # Retrieve the name and day of the most recently completed
        # chatroom for the save file name  
        if most_recent_chat == None:
            most_recent_chat = Chat_History('Example Chatroom', 'example_chat', '00:01')
        for day in chat_archive:
            if most_recent_chat in day.archive_list:
                the_day = day.day
                        
    
    fixed:
        ## This ensures the input will get the enter event before any of the
        ## buttons do.
        order_reverse True

        ## Contains the save slots. I've added many more than were originally
        ## available, but it's personal preference
        vpgrid id 'save_load_vp':
            style_prefix "slot"
            rows gui.file_slot_rows
            draggable True
            mousewheel True
            scrollbars "vertical"    
            side_spacing 12
            yalign 1.0
            
            # This adds the 'backup' save slot to the top when loading
            if title == "Load" and FileLoadable(mm_auto):
                $ save_title = (most_recent_chat.save_img + '|' 
                                + the_day + '|' + most_recent_chat.title)
                if '|' in FileSaveName(mm_auto):
                    $ rt, dn, cn = FileSaveName(mm_auto).split('|')
                else:                    
                    $ rt, dn, cn = save_title.split('|')
            
                button:
                    background 'save_auto_idle'
                    hover_background 'save_auto_hover'
                    if persistent.real_time:
                        action [SetField(persistent, 'on_route', True), 
                                SetField(persistent, 'load_instr', 'Auto'), 
                                SetField(persistent, 'just_loaded', True),
                                FileAction(mm_auto),
                                renpy.restart_interaction]
                    else:
                        action [SetField(persistent, 'on_route', True), 
                                SetField(persistent, 'just_loaded', True),
                                FileAction(mm_auto),
                                renpy.restart_interaction]
                    hbox:                        
                        window:
                            align (0.5, 0.5)
                            xysize(120, 120)
                            add 'save_auto' xalign 0.5 yalign 0.5
                        
                        window:
                            xysize (400, 120)
                            yalign 0.0
                            has vbox
                            spacing 8
                            fixed:
                                ysize 75
                                text ("This is a backup file that"
                                        + " is auto-generated"):
                                    style "save_slot_text" 
                                    yalign 0.0
                            text "Today: [dn] DAY":
                                style "save_slot_text" 
                                yalign 1.0

                        window:
                            xysize (155,120)
                            has vbox                            
                            fixed:
                                xsize 155
                                yfit True
                                text FileTime(mm_auto, 
                                    format=_("{#file_time}%m/%d %H:%M"), 
                                    empty=_("empty slot")):
                                    style "save_timestamp"                                
                            spacing 30
                            fixed:
                                xsize 155
                                yfit True
                                # Can't delete this file

            ## This displays all the regular save slots
            for i in range(gui.file_slot_cols * gui.file_slot_rows):

                $ slot = i + 1
                
                
                $ save_title = (most_recent_chat.save_img + '|' 
                                + the_day + '|' + most_recent_chat.title)
                if '|' in FileSaveName(slot):
                    $ rt, dn, cn = FileSaveName(slot).split('|')
                else:                    
                    $ rt, dn, cn = save_title.split('|')
                    
                $ file_time = FileTime(slot, empty="00:00")[-5:]
                $ file_hour = file_time[:2]
                $ file_min = file_time[-2:]
                $ next_day_name = False
                
                python:
                    # Compare file times to now
                    # E.g. if we saved at 20:30, if now is 20:29 or earlier,
                    # we want it to be the next day
                    if int(file_hour) > int(datetime.now().strftime('%H')):
                        # Hour of save is greater; proceed to next day
                        # Gets the name of the next day for loading purposes
                        for index, archive in enumerate(chat_archive):
                            if dn == archive.day:
                                if index+1 < len(chat_archive):
                                    next_day_name = chat_archive[index+1].day
                                    break
                    elif int(file_hour) == int(datetime.now().strftime('%H')):
                        # Check minutes
                        if int(file_min) > int(datetime.now().strftime('%M')):
                            # Minutes of save are greater; proceed to
                            # next day. Gets the name of the next day
                            # for loading purposes
                            for index, archive in enumerate(chat_archive):
                                if dn == archive.day:
                                    if index+1 < len(chat_archive):
                                        next_day_name = (chat_archive[index+1].
                                                                            day)
                                        break
                    else:
                        next_day_name = False
                
                    
                    
                    
                    
                if next_day_name:
                    $ long_msg = ("There is a difference between the save"
                                  + " time and the present time. It may cause"
                                  + " missed conversations or phone calls"
                                  + " during the time gap. Would you like to"
                                  + " continue?\n\nSave Time: " + dn 
                                  + " DAY " + file_time + "\n\nLoad Time: " 
                                  + next_day_name + " DAY " 
                                  + datetime.now().strftime('%H') + ":" 
                                  + datetime.now().strftime('%M'))
                else:
                    $ long_msg = ("There is a difference between the save"
                                  + " time and the present time. It may cause"
                                  + " missed conversations or phone calls"
                                  + " during the time gap. Would you like to"
                                  + " continue?\n\nSave Time: " + dn + " DAY " 
                                  + file_time + "\n\nLoad Time: " + dn 
                                  + " DAY " + datetime.now().strftime('%H') 
                                  + ":" + datetime.now().strftime('%M'))
               

                button:
                    if title == "Save":
                        action [SetVariable('save_name', save_title), 
                                FileAction(slot),
                                renpy.restart_interaction]
                    else: # title == "Load"
                        if (next_day_name and FileLoadable(slot) 
                                and persistent.real_time):
                            action [Show("confirm", message=long_msg, 
                                        yes_action=[
                                        SetField(persistent, 'just_loaded',
                                                     True),
                                        SetField(persistent, 'on_route',
                                                     True), 
                                        SetField(persistent, 'load_instr',
                                                     '+1 day'), 
                                        FileLoad(slot)], 
                                        no_action=Hide('confirm'))]
                        elif FileLoadable(slot) and persistent.real_time:
                            action [Show("confirm", message=long_msg, 
                                        yes_action=[
                                        SetField(persistent, 'just_loaded', 
                                                                    True),
                                        SetField(persistent, 'on_route',
                                                                    True), 
                                        SetField(persistent, 'load_instr',
                                                                 'Same day'),
                                        FileLoad(slot)], 
                                        no_action=Hide('confirm'))]
                        elif not persistent.real_time and FileLoadable(slot):
                            action [SetField(persistent, 'on_route', True), 
                                    SetField(persistent, 'just_loaded', True),
                                    FileAction(slot)]

                    hbox:   
                        window:
                            xysize(120, 120)
                            align (0.5, 0.5)
                            # Adds the correct save image to the left
                            if FileLoadable(slot):
                                add 'save_' + rt xalign 0.5 yalign 0.5
                            else:
                                add 'save_empty' xalign 0.5 yalign 0.5
                        
                        window:
                            xysize (400, 120)
                            yalign 0.0
                            has vbox
                            spacing 8
                            # Displays the most recent chatroom title + day
                            if FileLoadable(slot):
                                fixed:
                                    ysize 75
                                    text "[cn]":
                                        style "save_slot_text" 
                                        yalign 0.0
                                text "Today: [dn] DAY":
                                    style "save_slot_text" 
                                    yalign 1.0
                            else:
                                fixed:
                                    ysize 75
                                    text "Empty Slot":
                                        style "save_slot_text"
                                        yalign 0.0
                                text "Tap an empty slot to save":
                                    style 'save_slot_text'
                                    yalign 1.0
                            
                        window:
                            xysize (155,120)
                            has vbox
                            # Displays the time the save was created
                            # and the delete button
                            fixed:
                                xsize 155
                                yfit True
                                text FileTime(slot, 
                                        format=_("{#file_time}%m/%d %H:%M"), 
                                        empty=_("empty slot")):
                                    style "save_timestamp"
                                
                            spacing 30

                            fixed:
                                xsize 155
                                yfit True
                                imagebutton:
                                    hover Transform('save_trash',zoom=1.05)
                                    idle 'save_trash'
                                    xalign 1.0
                                    action FileDelete(slot)

                    key "save_delete" action FileDelete(slot)




        
    
########################################################
## Just the header that often shows up over menu items;
## put in a separate screen for less repeating code
########################################################

default my_menu_clock = Clock()
    
screen menu_header(title, return_action=NullAction, 
                    envelope=False, hide_bkgr=False):

    python:
        # Ensures the background music is playing
        if title != "In Call":
            if (renpy.music.get_playing(channel='music') != mystic_chat 
                    and not hacked_effect):
                renpy.music.play(mystic_chat, loop=True)
            elif (hacked_effect
                    and renpy.music.get_playing(channel='music') 
                        != mystic_chat_hacked):
                renpy.music.play(mystic_chat_hacked, loop=True)
    
    if not hide_bkgr:
        use starry_night()


    # If we're on real-time, check once a minute if it's time for the
    # next chatroom
    if persistent.just_loaded and renpy.get_screen('chat_home') is None:
        # Check if we should show the chat_hub 
        on 'show' action [SetField(persistent, 'just_loaded', False),
                            #Hide('chip_end'),
                            Show('chat_home')]
        on 'replace' action [SetField(persistent, 'just_loaded', False),
                            #Hide('chip_end'),
                            Show('chat_home')]
    if persistent.real_time and not main_menu and not starter_story:
        timer 60 action Function(next_chatroom) repeat True
        on 'show' action Function(next_chatroom)
        on 'replace' action Function(next_chatroom)
        
    if (not renpy.get_screen('text_message_screen') 
            and not main_menu 
            and not starter_story 
            and num_undelivered()):
        timer 0.5 action If(randint(0,3), deliver_next, []) repeat True
        timer 0.4 action Function(deliver_next)

    hbox:
        add my_menu_clock xalign 0.0 yalign 0.0 xpos 5
    
    
    if not persistent.first_boot:
        window:
            xysize(600, 80)
            yalign 0.01
            xalign 0.86
            hbox:
                yalign 0.01
                xalign 0.5
                add 'header_tray'
                imagebutton:
                    idle "header_plus"
                    hover "header_plus_hover"
                    #if not renpy.get_screen("choice"):
                    #    action NullAction
                add 'header_tray'
                
            add "header_hg" yalign 0.03 xalign 0.16
            add "header_heart" yalign 0.03 xalign 0.65
            
            text "[persistent.HG]":
                style "hg_heart_points" 
                xalign 0.35 yalign 0.01
            text "[persistent.HP]":
                style "hg_heart_points" 
                xalign 0.83 yalign 0.01
        
        
    # Header
    if title != "Original Story" and title != "In Call":
        window:
            ysize 80
            yalign 0.058
            add "menu_header"                
            
        if not envelope:
            text title:
                color "#ffffff" 
                size 40 
                xalign 0.5 yalign 0.072
                text_align 0.5 
        else:
            hbox:
                xalign 0.5 
                yalign 0.072
                spacing 15
                add 'header_envelope' xalign 0.5 yalign 0.5
                text title color "#ffffff" size 40 text_align 0.5
        
                
        
    if not persistent.first_boot:
        if title != "Original Story" and title != "In Call":
            # Back button
            imagebutton:
                xalign 0.013
                yalign 0.068
                idle "menu_back"
                focus_mask None
                hover Transform("menu_back", zoom=1.1)
                activate_sound 'audio/sfx/UI/back_button.mp3'
                if not renpy.get_screen("choice"):                
                    if persistent.first_boot or not persistent.on_route:
                        action [SetField(persistent, 'first_boot', False), 
                                return_action]
                    elif (envelope and (not text_person 
                            or not text_person.real_time_text)):
                        action Show('text_message_hub', Dissolve(0.5))
                    # If we're texting in real time, leaving text messages 
                    # works differently
                    elif text_person and text_person.real_time_text:
                        action Show("confirm", 
                                    message="Do you really want to leave this text message? You won't be able to continue this conversation.", 
                                    yes_action=[Hide('confirm'), 
                                    Jump('leave_inst_text')], 
                                    no_action=Hide('confirm'))    
                    else:
                        action return_action

        # Settings gear
        if title != "Setings":
            imagebutton:
                xalign 0.98
                yalign 0.01
                idle "settings_gear"
                hover "settings_gear_rotate"
                focus_mask None
                # Eventually I'd like to get the settings button 
                # working during phone calls, but there are too 
                # many bugs so it's commented out
                # if renpy.get_screen("in_call") and not renpy.get_screen("choice"):
                #     action [Preference("auto-forward", "disable"), Show("preferences")]
                if (not renpy.get_screen("choice") 
                        and not renpy.get_screen("in_call") 
                        and not text_person):
                    if renpy.get_screen('settings_screen'):
                        action [Hide('preferences'), 
                                Hide('profile_pic'), 
                                Hide('other_settings'), 
                                Show('preferences')]
                    else:
                        action Show("preferences")  
    if title == "Save" or title == "Load":
        transclude
    else:
        window:
            if title != "Original Story" and title != "In Call":
                xysize (750, 1180)
            else:
                xysize (750, 1180+80)
            yalign 1.0
            has vbox
            align (0.5, 0.0)
            spacing 10
            null height 5
            transclude
      

  

########################################################
## The 'homepage' from which you interact with the game
## after the main menu
########################################################
    
default chips_available = False
default spaceship_xalign = 0.04
default reset_spaceship_pos = False

screen chat_home(reshow=False):

    tag menu     
    modal True
    
    # Every time you go back to this screen, the game will auto-save
    on 'show':
        action If(renpy.get_screen('chip_tap') 
                    or renpy.get_screen('chip_cloud')
                    or renpy.get_screen('chip_end'),
                NullAction(),
                [Hide('chip_end'), renpy.retain_after_load,
                FileSave(mm_auto, confirm=False)]) 
 
    on 'replace':
        action If(renpy.get_screen('chip_tap') 
                    or renpy.get_screen('chip_cloud') 
                    or renpy.get_screen('chip_end'),
                NullAction(),
                [Hide('chip_end'), renpy.retain_after_load, 
                FileSave(mm_auto, confirm=False)]) 

    use menu_header("Original Story"):
        # Note that only characters in the list 'character_list' will
        # show up here as profile pictures
        # Also usually the characters have "generic" profile
        # pictures, but I've chosen to simply include their current
        # profile picture
        window:
            xysize(741, 206)
            xalign 0.5
            yalign 0.08
            vbox:
                spacing 8
                hbox:
                    spacing 8
                    xalign 0.0
                    yalign 0.0
                    for person in character_list[:7]:    
                        imagebutton:
                            hover "profile_pic_select_square"
                            idle Transform(person.prof_pic, size=(99,99))
                            background Transform(person.prof_pic, 
                                                            size=(99,99))
                            if person == m:
                                action Show('profile_pic')
                            else:
                                action Show('chara_profile', who=person)
                            activate_sound 'audio/sfx/UI/profile_screen_select.mp3'

                hbox:
                    spacing 8
                    for person in character_list[7:]:
                        imagebutton:
                            hover "profile_pic_select_square"
                            idle Transform(person.prof_pic, size=(99,99))
                            background Transform(person.prof_pic, 
                                                            size=(99,99))
                            action Show('chara_profile', who=person)
                            activate_sound 'audio/sfx/UI/profile_screen_select.mp3'
        window:
            xysize (750, 1170) 
            yoffset -140       
            # Text Messages
            button:
                xysize(168,168)
                xalign 0.62
                if len(character_list) > 10:
                    yalign 0.2
                else:
                    yalign 0.1
                if new_message_count() > 0:
                    background 'blue_mainbtn'
                    hover_background 'blue_mainbtn_hover'
                else:
                    background "gray_mainbtn"
                    hover_background "gray_mainbtn_hover"
                action Show('text_message_hub', Dissolve(0.5))
                activate_sound 'audio/sfx/UI/select_phone_text.mp3'
                if new_message_count() > 0:
                    add 'blue_maincircle' xalign 0.5 yalign 0.5
                    window:
                        xysize(45,45)
                        xalign 1.0
                        yalign 0.0
                        background 'new_text_count' 
                        text str(new_message_count()) style 'text_num'
                else:
                    add "gray_maincircle" xalign 0.5 yalign 0.5
                add "msg_mainicon" xalign 0.5 yalign 0.5
                add "msg_maintext" xalign 0.5 yalign 0.85
                
            # Calls
            button:
                xysize(168,168) 
                xalign 0.91
                if len(character_list) > 10:
                    yalign 0.4
                else:
                    yalign 0.3
                if unseen_calls > 0:
                    background "blue_mainbtn"
                    hover_background "blue_mainbtn_hover"
                else:
                    background "gray_mainbtn"
                    hover_background "gray_mainbtn_hover"
                action [SetVariable('unseen_calls', 0), Show('phone_calls')]  
                activate_sound 'audio/sfx/UI/select_phone_text.mp3'        
                if unseen_calls > 0:
                    add "blue_maincircle" xalign 0.5 yalign 0.5  
                    window:
                        xysize(45,45)
                        xalign 1.0
                        yalign 0.0
                        background 'new_text_count' 
                        text "[unseen_calls]" style 'text_num'
                else:
                    add "gray_maincircle" xalign 0.5 yalign 0.5
                
                add "call_mainicon" xalign 0.5 yalign 0.5
                add "call_maintext" xalign 0.5 yalign 0.85
            
            # Emails
            button:
                xysize(168,168)
                xalign 0.342
                if len(character_list) > 10:
                    yalign 0.4
                else:
                    yalign 0.3
                if unread_emails() > 0:
                    background "blue_mainbtn"
                    hover_background "blue_mainbtn_hover"
                else:
                    background "gray_mainbtn"
                    hover_background "gray_mainbtn_hover"
                action Show('email_hub', Dissolve(0.5))
                activate_sound 'audio/sfx/UI/select_email.mp3'
                if unread_emails() > 0:
                    add "blue_maincircle" xalign 0.5 yalign 0.5
                    window:
                        xysize(45, 45)
                        xalign 1.0
                        yalign 0.0
                        background 'new_text_count'
                        text str(unread_emails()) style 'text_num'
                else:
                    add "gray_maincircle" xalign 0.5 yalign 0.5
                add "email_mainicon" xalign 0.5 yalign 0.5
                add "email_maintext" xalign 0.5 yalign 0.85
                
            # Main Chatroom
            button:
                xysize(305,305)
                xalign 0.65
                yalign 0.722
                background "gray_chatbtn"
                hover_background "gray_chatbtn_hover"
                if persistent.real_time:
                    action [Function(next_chatroom), 
                            Function(deliver_all), 
                            Show('chat_select')]
                else:
                    action [Function(deliver_all), Show('chat_select')]
                activate_sound "audio/sfx/UI/chatroom_select.mp3"
                add "rfa_chatcircle" yalign 0.5 xalign 0.5
                add "blue_chatcircle" xalign 0.5 yalign 0.5
                add "chat_icon" xalign 0.5 yalign 0.5
                add "chat_text" xalign 0.5 yalign 0.8
            

            # Links/etc on the left side of the screen
            window:
                xysize(140, 1000)
                xalign 0.03
                yalign 0.98
                has vbox
                spacing 20
                # Album
                button:
                    xysize(130,149)
                    if new_cg:
                        background "blue_hex"
                        hover_background "blue_hex_hover"
                        add 'new_text' align (1.0, 0.1) xoffset 15
                    else:
                        background "white_hex"
                        hover_background "white_hex_hover"
                    action [SetVariable('new_cg', False), 
                            Show('photo_album', Dissolve(0.5))]
                    add "album_icon" xalign 0.5 yalign 0.35
                    add "album_text" xalign 0.5 yalign 0.8
                    
                # Guest
                button:
                    xysize(130,149)
                    background "white_hex"
                    hover_background "white_hex_hover"
                    #action NullAction
                    action ToggleScreen('hack_rectangle')
                    add "guest_icon" xalign 0.5 yalign 0.3
                    add "guest_text" xalign 0.5 yalign 0.8
                    
                # Shop
                button:
                    xysize(130,149)
                    background "red_hex"
                    hover_background "red_hex_hover"
                    #action NullAction
                    add "shop_icon" xalign 0.55 yalign 0.35
                    add "shop_text" xalign 0.5 yalign 0.8
                    
                # Notice
                button:
                    xysize(130,149)
                    background "white_hex"
                    hover_background "white_hex_hover"
                    #action NullAction
                    add "notice_icon" xalign 0.5 yalign 0.3
                    add "notice_text" xalign 0.5 yalign 0.8
                    
                # Link            
                button:
                    xysize(130,149)
                    background "white_hex"
                    hover_background "white_hex_hover"
                    #action SetVariable('chips_available', True)            
                    add "link_icon" xalign 0.5 yalign 0.3
                    add "link_text" xalign 0.5 yalign 0.8
                    
                    
            ## Spaceship    
            add "dot_line" xalign 0.5 yalign .97
                
            $ spaceship_xalign = spaceship_get_xalign(True)
                
            if chips_available:       
            
                if not reshow:
                    window at chip_anim:
                        xysize(90,70)
                        xalign 0.93
                        yalign 0.942
                        add "space_chip_explode"
                        
                    add "space_chip_active" xalign 0.92 yalign 0.98
                    
                    window at spaceship_chips(1.0):
                        xysize (100,110)
                        xalign 0.96
                        yalign 1.0
                        add "space_flame" xalign 0.5 yalign 1.0
                        add "spaceship" xalign 0.5 yalign 0.0
                        imagebutton:
                            idle "space_transparent_btn"
                            focus_mask None
                            activate_sound 'audio/sfx/UI/select_6.mp3'
                            action Show('chip_tap')
                
                if reshow:
                    window at chip_anim(0):
                        xysize(90,70)
                        xalign 0.93
                        yalign 0.942
                        add "space_chip_explode"
                        
                    add "space_chip_active2" xalign 0.92 yalign 0.98
                    
                    window at spaceship_chips:
                        xysize (100,110)
                        xalign 0.96
                        yalign 1.0
                        add "space_flame" xalign 0.5 yalign 1.0
                        add "spaceship" xalign 0.5 yalign 0.0
                        imagebutton:
                            idle "space_transparent_btn"
                            focus_mask None
                            activate_sound 'audio/sfx/UI/select_6.mp3'
                            action Show('chip_tap')
            
            else:            
                add "space_chip_inactive" xalign 0.92 yalign 0.98
                
                window at spaceship_flight:
                    xysize (100,110)
                    xalign 0.04#spaceship_xalign
                    yalign 1.0
                    add "space_flame" xalign 0.5 yalign 1.0
                    add "spaceship" xalign 0.5 yalign 0.0
                    imagebutton:
                            idle "space_transparent_btn"
                            focus_mask None
                            activate_sound 'audio/sfx/UI/select_6.mp3'
                            action Show('spaceship_thoughts', Dissolve(0.5))
                    
             
     
########################################################
## The Profile Screen for each of the characters
########################################################
        
screen chara_profile(who):

    tag settings_screen
    modal True

    use menu_header("Profile", Hide('chara_profile', Dissolve(0.5))):
        window:
            xysize (750, 1170)

            add who.cover_pic 
            
            fixed:
                xfit True yfit True
                xalign 0.1 yalign 0.6
                add Transform(who.big_prof_pic, size=(314,314))
                add 'profile_outline'    
            window:
                xysize (350,75)
                xalign 0.96
                yalign 0.64
                text who.name style "profile_header_text"
            window:  
                xysize (700, 260)
                yalign 0.9
                text who.status style "profile_status"
    

        