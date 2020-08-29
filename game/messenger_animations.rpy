#************************************
# Heart Icons
#************************************

init python:
    def allocate_heart_screen():
        """Allocate a screen to display a heart icon."""

        return allocate_screen(["heart_icon_screen", "hicon2", "hicon3"], True)

    def allocate_hg_screen():
        """Allocate a screen to award an hourglass."""

        return allocate_screen(['hourglass_animation', 'hg_icon2', 'hg_icon3'])

    def allocate_notification_screen(can_pause=False):
        """Allocate a screen to display a popup notification."""

        return allocate_screen(["stackable_notifications",
                            "stackable_notifications_2",
                            "stackable_notifications_3",
                            "stackable_notifications_4",
                            "stackable_notifications_5"], can_pause)

    def allocate_screen(possible_screens, can_pause=False):
        """Generic allocate screen function."""

        available_screens = [ x for x in possible_screens
                                if not renpy.get_screen(x) ]
        if can_pause and len(available_screens) < len(possible_screens):
            renpy.pause(0.1)
        if available_screens:
            return available_screens[0]
        else:
            renpy.hide_screen(possible_screens[0])
            return possible_screens[0]

    def hide_stackable_notifications():
        """Hide all notification screens."""

        renpy.hide_screen('hourglass_animation')
        renpy.hide_screen('hg_icon2')
        renpy.hide_screen('hg_icon3')

        renpy.hide_screen('stackable_notifications')
        renpy.hide_screen('stackable_notifications_2')
        renpy.hide_screen('stackable_notifications_3')
        renpy.hide_screen('stackable_notifications_4')
        renpy.hide_screen('stackable_notifications_5')
        return

    def hide_heart_icons():
        """Hide all the heart icon screens."""

        renpy.hide_screen('heart_icon_screen')
        renpy.hide_screen('hicon2')
        renpy.hide_screen('hicon3')
        return

    def heart_icon(character):
        """
        Dynamically recolour the heart icon to the colour associated with
        this character.
        """
        try:
            return im.MatrixColor("Heart Point/Unknown Heart Point.webp",
                im.matrix.colorize("#000000", character.heart_color))
        except:
            return "Heart Point/Unknown Heart Point.webp"

    def heart_break_img(picture, character):
        """
        Dynamically recolour the heartbreak icon to the colour associated
        with this character.
        """

        if character.heart_color:
            return im.MatrixColor(picture,
                    im.matrix.colorize("#000000", character.heart_color))
        else:
            return "Heart Point/heartbreak_0.webp"

# Display the heart icon on-screen
screen heart_icon_screen(character, hide_screen='heart_icon_screen'):
    zorder 20

    fixed at heart:
        yfit True
        xfit True
        add heart_icon(character)

    timer 0.62 action [Hide('heart_icon_screen')]

# Additional screens for allocation
screen hicon2(character):
    zorder 20
    use heart_icon_screen(character, 'hicon2')

screen hicon3(character):
    zorder 20
    use heart_icon_screen(character, 'hicon3')

## This screen is used to display text notifications
## as an alternative to animated icons
screen stackable_notifications(message, hide_screen='stackable_notifications'):
    zorder 100
    button at stack_notify_appear:
        style 'notify_frame'
        xalign 1.0 yalign 0.92
        text "[message!tq]" style 'notify_text'
        action Hide(hide_screen)
    timer 5.25 action Hide(hide_screen)

screen stackable_notifications_2(message):
    zorder 101
    use stackable_notifications(message, 'stackable_notifications_2')

screen stackable_notifications_3(message):
    zorder 102
    use stackable_notifications(message, 'stackable_notifications_3')

screen stackable_notifications_4(message):
    zorder 103
    use stackable_notifications(message, 'stackable_notifications_4')

screen stackable_notifications_5(message):
    zorder 104
    use stackable_notifications(message, 'stackable_notifications_5')

transform stack_notify_appear:
    yoffset 0
    on show:
        alpha 0 yoffset 30
        linear .25 alpha 1.0 yoffset 0
        linear 5 yoffset -250
    on hide:
        linear .5 alpha 0.0 yoffset -310


# Display the heartbreak on-screen
screen heart_break_screen(character):
    zorder 20

    fixed at heartbreak(0.0):
        yfit True
        xfit True
        add heart_break_img("Heart Point/heartbreak_0.webp", character)
    fixed at heartbreak(0.12):
        yfit True
        xfit True
        add heart_break_img("Heart Point/heartbreak_1.webp", character)
    fixed at heartbreak(0.24):
        yfit True
        xfit True
        add heart_break_img("Heart Point/heartbreak_2.webp", character)
    fixed at heartbreak(0.36):
        yfit True
        xfit True
        add heart_break_img("Heart Point/heartbreak_3.webp", character)
    fixed at heartbreak(0.48):
        yfit True
        xfit True
        add heart_break_img("Heart Point/heartbreak_4.webp", character)

    timer 0.6 action [Hide('heart_break_screen')]


image hg_1 = "Heart Point/hourglass_1.webp"
image hg_2 = "Heart Point/hourglass_2.webp"

## Screen that displays the hourglass animation when the player
## receives an hourglass
screen hourglass_animation(hide_screen='hourglass_animation'):

    zorder 20

    add 'hg_1' at hourglass_anim(0.0) align (0.5, 0.5)
    add 'hg_2' at hourglass_anim_2(firstbouncein
            + firstbounceout + secbouncein, 0.7):
        align (0.5, 0.5)

    timer arbitrary_delay+smallzoom+0.3+zoomouttime:
        action Hide(hide_screen)

## Additional screens for allocation
screen hg_icon2():
    zorder 20
    use hourglass_animation('hg_icon2')

screen hg_icon3():
    zorder 20
    use hourglass_animation('hg_icon3')


transform hourglass_anim(delay=0.0):
    zoom 1.0
    parallel:
        # Bounce 1
        easein firstbouncein zoom 2.6
        easeout firstbounceout zoom 1.0
        # Bounce 2
        easein secbouncein zoom 2.1
        easeout smallzoom zoom 1.15
        # Grow larger
        easein bigzoom zoom 5.75
    parallel:
        # And fade out
        linear firstbouncein + firstbounceout + secbouncein + smallzoom
        linear fadeinout alpha 0.0

transform hourglass_anim_2(delay=0.0, proportion=1.0):
    alpha 0.0 zoom proportion*2.1#1.83
    linear delay
    parallel:
        # Image gets smaller
        easeout smallzoom zoom 1.15*proportion#1.0
    parallel:
        # Image becomes visible
        linear arbitrary_delay
        linear 0.3 alpha 1.0
    parallel:
        # Image becomes larger
        easeout smallzoom
        easein bigzoom zoom proportion*5.75#5.0
    parallel:
        # Image becomes transparent
        linear arbitrary_delay+smallzoom
        linear zoomouttime-0.3 alpha 0.0


define firstbouncein = 0.23 # 1.0
define firstbounceout = 0.23 # 0.8
define secbouncein = 0.2 # 0.5
define smallzoom = 0.32 # 0.7
define bigzoom = 1.2 # 2.0
define arbitrary_delay = 0.1 # 0.3
define zoomouttime = 0.8 # 1.6
define fadeinout = 0.6


#####################################
# Chat Speed Modifiers
#####################################

init python:

    def speed_num_fn(st, at):
        """Display the SPEED number in-chat."""

        speednum = "!!"
        # Minimum pv is 0.1, maximum is ~1.4
        # 5 = 0.8
        # So it goes 1.4, 1.25, 1.1, 0.95, 0.8, 0.65, 0.5, 0.35, 0.2
        speednum = str(int((round(9.0 - ((store.pv - 0.2) / 0.15), 1))))

        speedtxt = Text("SPEED", style='speednum_style', size=30)
        numtxt = Text(speednum, style='speednum_style', align=(.5,.5))
        return VBox(speedtxt, numtxt), 0.05

# The number that shows up when adjusting the chatroom speed
style speednum_style is text:
    xalign 0.97
    yalign 0.22
    color "#ffffff"
    font gui.sans_serif_1b
    size 45
    text_align 0.5

image speed_num_img = DynamicDisplayable(speed_num_fn)

screen speed_num():

    add 'speed_num_img' align(0.98, 0.2)

    timer 0.4 action Hide('speed_num', Dissolve(0.4))

#####################################
# Hack scrolls, banners, enter/exit
#####################################

#************************************
# Hack Scrolls
#************************************
# Displays the scrolled hacking effect

screen hack_screen(hack):
    zorder 10
    modal True
    add 'black'
    imagebutton at flicker:
        xysize (750,1334)
        idle hack
        if observing and not _in_replay:
            action Hide('hack_screen')

    timer 3.0 action Hide('hack_screen')


label hack():
    if (not observing and not persistent.testing_mode
            and not vn_choice):
        $ hack_entry = ("hack", "regular")
        $ current_timeline_item.replay_log.append(hack_entry)
    if persistent.hacking_effects:
        show screen hack_screen('hack scroll')
        pause 3.0
        hide screen hack_screen
    return

label redhack():
    if (not observing and not persistent.testing_mode
            and not vn_choice):
        $ hack_entry = ("hack", "red")
        $ current_timeline_item.replay_log.append(hack_entry)
    if persistent.hacking_effects:
        show screen hack_screen('redhack scroll')
        pause 3.0
        hide screen hack_screen
    return

#************************************
# Banners
#************************************

# These are the special "banners" that crawl across the screen
# Call them using "call banner('well')" etc

label banner(banner):
    if (not observing and not persistent.testing_mode
            and not vn_choice):
        $ banner_entry = ("banner", banner)
        $ current_timeline_item.replay_log.append(banner_entry)
    if persistent.banners:
        show screen banner_screen(banner)
    return

screen banner_screen(banner):
    zorder 10
    fixed:
        xysize (750, 230)
        align (.5, .5)
        add 'banner ' + banner align (0.5, 1.0)

    timer 0.72 action Hide('banner_screen')
