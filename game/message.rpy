
init -4 python:

    ## This is the object that each chat is stored in
    ##  Who = the speaker, What = the text they're saying, thetime keeps track
    ##  of the current time, 'bounce' indicates whether the message is
    ##  supposed to animate in with a bounce or not (by default is false), and
    ##  specBubble is a variable that holds the name of any special speech bubbles
    ##  that should be used when displaying the text (by default is empty and a regular
    ##  bubble is used)
    class Chatentry(object):
        def __init__(self, who, what, thetime, img=False, bounce=False, specBubble=None):
            self.who = who
            self.what = what
            self.thetime = thetime
            self.img = img
            self.bounce = bounce
            self.specBubble = specBubble
            
    
    ##************************************
    ## For ease of adding Chatlog entries
    ##************************************   
    
    ## This corrects the dialogue into a filepath for the program
    def cg_helper(what):
        album, cg_name = what.split('/')
        if album[-6:] != '_album':
            album += '_album'
        # These will be equal to a path like
        # CGs/common_album/cg-1.png
        return 'CGs/' + album + '/' + cg_name
    
    def addchat(who, what, pauseVal, img=False, bounce=False, specBubble=None):
        global choosing, pre_choosing, pv, chatbackup, oldPV, observing
        global persistent, cg_testing
        choosing = False
        pre_choosing = False
                
        if pauseVal == None:
            pauseVal = pv
                        
        if len(chatlog) > 1:
            finalchat = chatlog[-2]
            if finalchat.who.file_id == 'delete':
                # This bubble doesn't display; delete it
                del chatlog[-2]
                
        if who.file_id != 'delete':
            pauseFailsafe()
            chatbackup = Chatentry(who, what, upTime(), img, bounce, specBubble)
            oldPV = pauseVal
            
        if pauseVal == 0:
            pass
        elif who.file_id == 'delete':
            renpy.pause(pv)
        else:
            typeTime = what.count(' ') + 1 # equal to the number of words
            # Since average reading speed is 200 wpm or 3.3 wps
            typeTime = typeTime / 3
            if typeTime < 1.5:
                typeTime = 1.5
            typeTime = typeTime * pauseVal
            renpy.pause(typeTime)
            
        if img == True:
            if what in emoji_lookup:
                renpy.play(emoji_lookup[what], channel="voice_sfx")
            elif "{image=" not in what and not observing:
                # We want to unlock the CG in the gallery
                # These will be equal to a path like
                # CGs/common_album/cg-1.png
                cg_filepath = cg_helper(what)
                album, cg_name = what.split('/')
                if album[-6:] != '_album':
                    album += '_album'
                cg_testing = ""
                cg_testing += album + " "
                cg_testing += cg_filepath
                # Now we need to search for that CG
                for photo in getattr(persistent, album):
                    if cg_filepath == photo.img:
                        cg_testing += "found it "
                        photo.unlock()
                        break
                    else:
                        cg_testing += "didn't find it "
        
        chatlog.append(Chatentry(who, what, upTime(), img, bounce, specBubble))
        
    
            
    ## Function that checks if an entry was successfully added to the chat
    ## A temporary fix for the pause button bug
    ## This also technically means a character may be unable to post the exact
    ## same thing twice in a row depending on when the pause button is used
    def pauseFailsafe():
        global reply_instant
        if len(chatlog) > 0:
            last_chat = chatlog[-1]
        else:
            return
        if last_chat.who.file_id == 'delete':
            if len(chatlog) > 1:
                last_chat = chatlog[-2]
            else:
                return
        elif last_chat.who == filler:
            return
                
        if last_chat.who.file_id == chatbackup.who.file_id and last_chat.what == chatbackup.what:
            # the last entry was successfully added; we're done
            return
        else:
            # add the backup entry
            if reply_instant:
                reply_instant = False
            else:
                typeTime = chatbackup.what.count(' ') + 1
                typeTime = typeTime / 3
                if typeTime < 1.5:
                    typeTime = 1.5
                typeTime = typeTime * oldPV
                renpy.pause(typeTime)
            
            if chatbackup.img == True:
                if chatbackup.what in emoji_lookup:
                    renpy.play(emoji_lookup[chatbackup.what], channel="voice_sfx")
               
            chatlog.append(Chatentry(chatbackup.who, chatbackup.what, upTime(), chatbackup.img, chatbackup.bounce, chatbackup.specBubble))

   
    ### Set a variable to infinity, to be used later -- it keeps the viewport scrolling to the bottom
    yadjValue = float("inf")
    ### Create a ui.adjustment object and assign it to a variable so that we can reference it later. 
    # I'll assign it to the yadjustment property of our viewport later.
    yadj = ui.adjustment()
    
    # This is mostly changed automatically for you when you call
    # chat_begin("night") etc, but if you want to change it on an
    # individual basis this is the colour of the characters' nicknames
    nickColour = "#000000"   

default chatbackup = Chatentry(filler,"","")
default pv = 0.8
default oldPV = pv
default cg_testing = False

#####################################
# Chat Setup
#####################################

# This simplifies things when you're setting up a chatroom,
# so call it when you're about to begin
# If you pass it the name of the background you want (enclosed in
# single ' or double " quotes) it'll set that up too
# Note that it automatically clears the chatlog, so if you want
# to change the background but not clear the messages on-screen,
# you'll also have to pass it 'False' as its second argument

label chat_begin(background=None, clearchat=True, resetHP=True):
    stop music
    if clearchat:
        $ chatlog = []
        # $ pv = 0.8    # This resets the chatroom "speed"
                        # Ordinarily it would reset for every
                        # new chatroom, and if you want that
                        # functionality you can un-comment this
                        # line
    if resetHP:
        $ chatroom_hp = 0
    hide screen starry_night
    show screen phone_overlay
    show screen messenger_screen 
    show screen pause_button
    
    # Hide all the popup screens
    hide screen text_msg_popup
    hide screen text_msg_popup_instant
    hide screen email_popup
    
    $ inst_text = False
    window hide
    $ reply_screen = False
    $ in_phone_call = False
    $ vn_choice = False
    $ email_reply = False
    # Fills the beginning of the screen with 'empty space' so the messages begin
    # showing up at the bottom of the screen (otherwise they start at the top)
    if clearchat:
        $ addchat(filler, "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n", 0)
        
    # Sets the correct background and nickname colour
    # You'll need to add other backgrounds here if you define
    # new ones
    if background == "morning":
        scene bg morning
        $ nickColour = black
    elif background == "noon":
        scene bg noon
        $ nickColour = black
    elif background == "evening":
        scene bg evening
        $ nickColour = black
    elif background == "night":
        scene bg night
        $ nickColour = white
    elif background == "earlyMorn":
        scene bg earlyMorn
        $ nickColour = white
    elif background == "hack":
        scene bg hack
        $ nickColour = white
    elif background == "redhack":
        scene bg redhack
        $ nickColour = white
    elif background == "redcrack":
        scene bg redcrack
        $ nickColour = white
    else:
        scene bg black
        $ nickColour = white
        
    # If you've already played this chatroom in your current runthrough,
    # viewing it again causes this variable to be True. It prevents you
    # from receiving heart points again and only lets you select choices
    # you've selected on this or previous playthroughs
    if current_chatroom.played:
        if not persistent.testing_mode:
            $ observing = True
        else:
            pass
    else:
        $ observing = False
        
        
    if resetHP:
        $ in_chat = []
        python:
            for person in current_chatroom.participants:
                if person.name not in in_chat:
                    in_chat.append(person.name)
            
        # If the player is participating, add them to the list of
        # people in the chat
        if not current_chatroom.expired or current_chatroom.buyback or current_chatroom.buyahead:
            $ in_chat.append(m.name)
        
    return

# Call this label to show the save & exit sign
label chat_end:
    $ addchat(answer, '', 0.2)
    if starter_story:        
        $ persistent.first_boot = False
        $ persistent.on_route = True
    call screen save_and_exit    
    return
    
label chat_end_route(type='good'):
    $ addchat(answer, '', 0.2)
    call screen save_and_exit(True)
    $ config.skipping = False
    $ greeted = False
    $ choosing = False
    hide screen phone_overlay
    hide screen messenger_screen
    stop music
    
    if type == 'good':
        scene bg good_end
    elif type == 'normal':
        scene bg normal_end
    elif type == 'bad':
        scene bg bad_end
    pause
    return

screen messenger_screen:

    tag menu

    python:
        #if yadj.value == yadj.range:
        #    yadj.value = yadjValue
        #elif yadj.value == 0:
        #    yadj.value = yadjValue
            
        #if len(chatlog) > 0:
        #    finalchat = chatlog[-1]
        #    if finalchat.who == filler:
        #        yadj.value = yadjValue
        #if len(chatlog) < 3:
        #    yadj.value = yadjValue
        #yinitial = yadjValue
        yadj.value = yadjValue   
            
    #else:
        #image "Phone UI/new_message_banner.png" ypos 170
        #$ new_msg_clicked = False
        #imagebutton:
        #    xanchor 0.0
        #    yanchor 0.0
        #    xpos 0
        #    ypos 169
        #    focus_mask True
        #    idle "new_messages"
        #    action [SetVariable("new_msg_clicked", True), renpy.restart_interaction]
        #if new_msg_clicked:
        #    $ new_msg_clicked = False
        #    $ yadj.value = yadjValue
        #    $ renpy.hide_screen("new_message_screen")
    # else: could have a "new_messages" notification


    window:
        align (0.5, 0.6)
        xfill True
        ysize 1050

        viewport yadjustment yadj: # viewport id "VP":
            draggable True
            mousewheel True
            ysize 1050
                            
            has vbox:
                spacing gui.phone_spacing
                if gui.phone_height:
                    vpgrid:
                        cols 1
                        yinitial 1.0

                        use chat_dialogue()

                else:

                    use chat_dialogue()
                                
                            

screen chat_dialogue():
 
    python:
        chatLength = len(chatlog) - 1
        begin = chatLength - 10
        if begin >= 0:
            pass
        else:
            begin = 0
        
        if chatLength > 0:
            finalchat = chatlog[-1]
            if finalchat.who == answer:
                if begin > 0:
                    begin -= 1
                
    for i index id(i) in chatlog[begin:]:
        use chat_animation(i)
                      
                      
                      
screen chat_animation(i, animate=True):

    python:
        include_new = False
        
        if i.bounce:
            transformVar = incoming_message_bounce
            include_new = False
        else:
            transformVar = incoming_message
            include_new = True
            
        if i.who == m:
            nameStyle = 'chat_name_MC'
            include_new = False
        else:
            nameStyle = 'chat_name'
            
            
        if i.who.file_id:
            if i.specBubble != None and i.specBubble != 'glow2':
                include_new = False
                bubbleBackground = "Bubble/Special/" + i.who.file_id + "_" + i.specBubble + ".png"    
            elif i.specBubble != None and i.specBubble == 'glow2':
                include_new = False
                bubbleBackground = "Bubble/Special/" + i.who.file_id + "_" + i.specBubble + ".png"
            elif i.bounce: # Not a special bubble; just glow
                include_new = False
                if not i.who.glow_color:
                    bubbleBackground = "Bubble/" + i.who.file_id + "-Glow.png"
                else:
                    bubbleBackground = DynamicDisplayable(glow_bubble_fn, glow_color=i.who.glow_color)
            elif i.who != 'answer':
                if not i.who.bubble_color:
                    bubbleBackground = "Bubble/" + i.who.file_id + "-Bubble.png"
                else:
                    bubbleBackground = DynamicDisplayable(reg_bubble_fn, bubble_color=i.who.bubble_color)
            
            if i.specBubble != None:
                # Some characters have more than one round or square bubble
                # but they follow the same style as "round" or "square"
                if i.specBubble[:6] == "round2":
                    bubbleStyle = "round_" + i.specBubble[-1:]
                elif i.specBubble[:7] == "square2":
                    bubbleStyle = "square_" + i.specBubble[-1:]
                elif i.specBubble == "glow2":
                    bubbleStyle = 'glow_bubble'
                else:
                    bubbleStyle = i.specBubble
            
            if i.img == True:
                include_new = False
                if "{image=" in i.what:
                    pass
                else:
                    transformVar = small_CG
                    
            ## This determines how long the line of text is. If it needs to wrap
            ## it, it will pad the bubble out to the appropriate length
            ## Otherwise each bubble would be exactly as wide as it needs to be and no more
            t = Text(i.what)
            z = t.size()
            my_width = int(z[0])
            my_height = int(z[1])
                    
            global choosing
            
        if not animate:
            global f_style_begin, f_style_end
            transformVar = null_anim
            nickColour = white
            dialogue = f_style_begin + i.what + f_style_end
        else:
            dialogue = i.what
            
        
    ## First, the profile picture and name, no animation
    if i.who.name == 'msg' or i.who.name == 'filler':
        window:
            style i.who.name + '_bubble'
            text dialogue style i.who.name + '_bubble_text'
            
    elif i.who.file_id != 'delete':#i.who != answer and i.who != chat_pause:
        window:
            if i.who == m:
                style 'MC_profpic'
                if not animate:
                    xoffset -40
            else:
                style 'profpic'
                
            add Transform(i.who.prof_pic, size=(110,110))
            
        if animate:
            text i.who.name style nameStyle color nickColour
        elif i.who == m:
            text i.who.name style nameStyle color nickColour xoffset -30 yoffset 102
        else:
            text i.who.name style nameStyle color nickColour yoffset 102
        
        ## Now add the dialogue
        
        if not include_new: # Not a 'regular' dialogue bubble
            window at transformVar:                 
                ## Check if it's an image
                if i.img == True:
                    if i.who == m:
                        style 'mc_img_message'
                    else:
                        style 'img_message'
                    if not animate:
                        yoffset 135
                    # Check if it's an emoji
                    if "{image=" in i.what:
                        text i.what
                    else:   # it's a CG
                        $ fullsizeCG = cg_helper(i.what)
                        imagebutton:
                            bottom_margin -100
                            focus_mask True
                            idle fullsizeCG
                            if not choosing:
                                action [SetVariable("fullsizeCG", cg_helper(i.what)), Call("viewCG"), Return()]
                                
                                
                ## Check if it's a special bubble
                elif i.specBubble != None and i.specBubble != 'glow2':
                    style bubbleStyle 
                    if not animate:
                        yoffset 125
                    background bubbleBackground # e.g. style "sigh_m" 
                    text dialogue style "special_bubble"
                    
                ## Dialogue is either 'glow' or 'regular' variant
                elif i.bounce:
                    # Note: MC has no glowing bubble so there is no variant for them
                    style 'glow_bubble' 
                    if not animate:
                        yoffset 138
                    background Frame(bubbleBackground, 25, 25)
                    # This checks if the text needs to wrap or not
                    if my_width > gui.longer_than:
                        text dialogue style "bubble_text_long" min_width gui.long_line_min_width
                    else:            
                        text dialogue style "bubble_text"
                        
                else:
                    style 'reg_bubble_MC'
                    if not animate:
                        yoffset 138 xoffset -35
                    if my_width > gui.longer_than:
                        text dialogue style "bubble_text_long" min_width gui.long_line_min_width
                    else:            
                        text dialogue style "bubble_text"
                        
        else:
            if my_width > gui.longer_than:
                fixed at transformVar:
                    pos (138, -85)
                    xanchor 0
                    yanchor 0
                    yfit True
                    if not animate:
                        yoffset 135
                    
                    vbox:
                        spacing -55
                        order_reverse True
                        add 'new_sign' xalign 1.0 yalign 0.0 yoffset 0 xoffset 40 at new_fade
                        window:                        
                            background Frame(bubbleBackground, 25,18,18,18)
                            style 'reg_bubble'                            
                            text dialogue style "bubble_text_long" min_width gui.long_line_min_width
                           
            else:
                fixed at transformVar:
                    pos (138, -85)
                    xanchor 0
                    yanchor 0
                    ysize my_height - 20
                    if not animate:
                        yoffset 135
                    
                    vbox:
                        spacing -55
                        order_reverse True
                        add 'new_sign' xalign 1.0 yalign 0.0 yoffset 0 xoffset 40 at new_fade
                        window:                        
                            background Frame(bubbleBackground, 25,18,18,18)                          
                            style 'reg_bubble_short'                            
                            text dialogue style "bubble_text"
                    
        if animate:
            use anti_animation(i)  

#******************************************
#  This code 'cancels out' the animation  *
#   for Mystic messenger; otherwise the   *
# bottom of the viewport would 'slide in' *
#******************************************           
screen anti_animation(i):
    
    python:
        include_new = False
        if i.bounce:
            transformVar = anti_incoming_message_bounce
            include_new = False
        else:
            transformVar = anti_incoming_message
            include_new = True
            
        if i.who == m:
            include_new = False
            
        if i.bounce:
            if i.specBubble and i.specBubble == 'glow 2':
                bubbleBackground = "Bubble/Special/" + i.who.file_id + "_" + i.specBubble + ".png"
            else:
                if not i.who.glow_color:
                    bubbleBackground = "Bubble/" + i.who.file_id + "-Glow.png"
                else:
                    bubbleBackground = DynamicDisplayable(glow_bubble_fn, glow_color=i.who.glow_color)
            include_new = False
        else:
            if not i.who.bubble_color:
                bubbleBackground = "Bubble/" + i.who.file_id + "-Bubble.png"
            else:
                bubbleBackground = DynamicDisplayable(reg_bubble_fn, bubble_color=i.who.bubble_color)
            
            
        if i.specBubble != None:
            if i.specBubble[:6] == "round2":
                bubbleStyle = "round_" + i.specBubble[-1:]
            elif i.specBubble[:7] == "square2":
                bubbleStyle = "square_" + i.specBubble[-1:]
            elif i.specBubble == "glow2":
                bubbleStyle = 'glow_bubble'
            else:
                bubbleStyle = i.specBubble
                
        if i.specBubble != None and i.specBubble != 'glow2':
            include_new = False
            bubbleBackground = "Bubble/Special/" + i.who.file_id + "_" + i.specBubble + ".png"
            
        if i.img == True:
            include_new = False
            if "{image=" in i.what:
                pass
            else:
                transformVar = anti_small_CG
                
        t = Text(i.what)
        z = t.size()
        my_width = int(z[0])
        my_height = int(z[1])
        
        global choosing
        
    if not include_new:
        window at transformVar:
            if i.img == True:
                style "img_message"
                # Check if it's an emoji
                if "{image=" in i.what:
                    # there's an image to display
                    text i.what
                else:   # presumably it's a CG
                    bottom_margin -100
                    $ fullsizeCG = cg_helper(i.what)
                    add fullsizeCG
                    
            elif i.specBubble != None and i.specBubble != 'glow2':                        
                style bubbleStyle background bubbleBackground # e.g. style "sigh_m" 
                text i.what style "special_bubble"
                
            ## Dialogue is either 'glow' or 'regular' variant
            elif i.bounce:
                style 'glow_bubble' 
                background Frame(bubbleBackground, 25, 25)
                if my_width > gui.longer_than:
                    text i.what style "bubble_text_long" min_width gui.long_line_min_width
                else:            
                    text i.what style "bubble_text"
                    
            else:
                style 'reg_bubble_MC'
                if my_width > gui.longer_than:
                    text i.what style "bubble_text_long" min_width gui.long_line_min_width
                else:            
                    text i.what style "bubble_text"

    
    else:
        if my_width > gui.longer_than:
            fixed at transformVar:
                pos (138, -85)
                xanchor 0
                yanchor 0
                yfit True
                
                vbox:
                    spacing -55
                    order_reverse True
                    add 'new_sign' xalign 1.0 yalign 0.0 yoffset 0 xoffset 40 at new_fade
                    window:                        
                        background Frame(bubbleBackground, 25,18,18,18)
                        style 'reg_bubble'
                        text i.what style "bubble_text_long" min_width gui.long_line_min_width
                       
        else:
            fixed at transformVar:
                pos (138, -85)
                xanchor 0
                yanchor 0
                ysize my_height - 20
                
                vbox:
                    spacing -55
                    order_reverse True
                    add 'new_sign' xalign 1.0 yalign 0.0 yoffset 0 xoffset 40 
                    window:                        
                        background Frame(bubbleBackground, 25,18,18,18)   
                        style 'reg_bubble_short'
                        text i.what style "bubble_text"

            
            

            