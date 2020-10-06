init python:

    class Email(renpy.store.object):
        """
        Class that holds information needed for an email's delivery, timeout,
        failure, and more.

        Attributes:
        -----------
        guest : Guest
            Guest object of the sender of this email.
        msg : string
            Content of the email.
        reply_label : string
            Label to jump to in order to reply to this email.
        msg_num : int (0-3)
            Reply number. 0 is the first message sent to the player, and
            3 is the email accepting the player's invitation.
        failed : bool
            True if this email chain has been failed.
        timeout_count : int
            If the player doesn't respond within this many chatrooms, the
            email is considered "timed out" and cannot be interacted with.
        deliver_reply : int or "wait"
            How many chatrooms the player must wait before the guest replies
            to their email, or "wait" if it's the player's turn to reply.
        reply : string or False
            Contains the message to be delivered when the guest replies
            to the player's message, or False if it's the player's turn
            to send a message.
        timeout : bool
            True if this message has timed out.
        sent_time : MyTime
            MyTime object containing the time the last email was sent at.
        read : bool
            True if this email has been read
        notified : bool
            True if the player has received a popup informing them of this
            email.
        before_branch : bool
            Only used for the tutorial guest. If True, the program attempts
            to finish sending emails before it reaches a plot branch.
        """

        def __init__(self, guest, msg, reply_label):
            """
            Create an Email object.

            Parameters:
            -----------
            guest : Guest
                Guest object of the sender of this email.
            msg : string
                Content of the email.
            reply_label : string
                Label to jump to in order to reply to this email.
            """

            self.guest = guest
            self.msg = msg
            self.reply_label = reply_label
            self.msg_num = 0
            self.failed = False
            self.timeout_count = 25
            self.deliver_reply = "wait"
            self.reply = False
            self.timeout = False
            self.sent_time = upTime()
            self.__read = False
            self.notified = False
            self.before_branch = (guest.thumbnail
                == "Email/Thumbnails/rainbow_unicorn_guest_icon.webp")

        def __eq__(self, other):
            """
            Check for equality between two Email objects.
            Allows this class to be persistent.
            """

            if getattr(other, 'guest', False):
                return self.guest == other.guest
            else:
                return False

        def __ne__(self, other):
            """Check for inequality between two Email objects."""

            if getattr(other, 'guest', False):
                return self.guest != other.guest
            else:
                return False

        @property
        def read(self):
            """Return whether this email has been read."""
            return self.__read

        @read.setter
        def read(self, new_status):
            """
            Set this email's read status and whether or not the guest is
            attending the party, if this email chain is finished.
            """

            self.__read = new_status
            self.set_attendance()
            return

        def deliver(self):
            """
            Deliver the next email in the chain to the player and
            notify them of its delivery with a popup.
            """

            global email_list

            # If you're waiting on a reply, decrease the timer
            if self.deliver_reply != "wait":
                self.deliver_reply -= 1
                renpy.retain_after_load()

            # If it's your turn to reply, decrease the timeout counter,
            # Unless this is the final message and there's no need to reply
            # If this is the first message, show a popup
            elif (self.deliver_reply == "wait"
                    and self.msg_num <= 2
                    and not self.timeout):
                self.timeout_count -= 1
                if not self.notified and self.msg_num == 0 and not self.read:
                    # Notify the player of the delivered message
                    renpy.show_screen('email_popup', e=self)
                    self.notified = True
                    renpy.retain_after_load()
                    renpy.restart_interaction()

            # If the timeout counter reaches 0, timeout becomes True
            if (self.timeout_count == 0
                    and self.msg_num <= 2
                    and not self.failed):
                self.timeout = True
                renpy.retain_after_load()

            # If the timer <= 0 and there's a reply to be
            # delivered, deliver it
            if (self.deliver_reply != "wait"
                    and self.deliver_reply <= 0
                    and self.reply):
                self.read = False
                self.reply += "\n\n------------------------------------------------\n\n"
                self.msg = self.reply + self.msg
                self.reply = False
                self.sent_time = upTime()
                self.timeout_count = 25 # resets the timeout counter
                self.deliver_reply = "wait"
                email_list.remove(self)
                email_list.insert(0, self) # Moves to the front of the list
                renpy.restart_interaction()
                # Notify the player of the delivered message
                self.notified = True
                renpy.music.play(persistent.email_tone, 'sound')
                renpy.show_screen('email_popup', e=self)
                renpy.retain_after_load()


        def set_reply(self, iscorrect, deliver_reply=False):
            """Set the guest's reply and decide when it should be delivered."""

            test = False

            if iscorrect:
                if self.msg_num == 0:
                    self.reply = self.guest.reply1_good
                    self.reply_label = self.guest.label2
                elif self.msg_num == 1:
                    self.reply = self.guest.reply2_good
                    self.reply_label = self.guest.label3
                elif self.msg_num == 2:
                    self.reply = self.guest.reply3_good
                    self.reply_label = False
                self.add_msg(True)
            else:
                if self.msg_num == 0:
                    self.reply = self.guest.reply1_bad
                elif self.msg_num == 1:
                    self.reply = self.guest.reply2_bad
                elif self.msg_num == 2:
                    self.reply = self.guest.reply3_bad
                self.add_msg(False)
                self.failed = True
                self.reply_label = False

            # If a number is given, the reply will be delivered
            # within that many chatrooms. Otherwise, the program
            # calculates a number range for the email so it can
            # be delivered before the party
            if deliver_reply != False:
                self.deliver_reply = deliver_reply
            else:
                if not test:
                    max_num = num_future_timeline_items(self.before_branch) - 1
                    min_num = 1
                    msg_remain = 3 - self.msg_num
                    if msg_remain == 0:
                        msg_remain = 1
                    # The program ensures there are enough
                    # chatrooms left to finish delivering the
                    # emails e.g. if there are 30 chatrooms left
                    # and there are another 3 replies to deliver,
                    # max_num will be 10 and min_num will be 3, so
                    # the message will be delivered sometime after
                    # the next 3-10 chatrooms
                    max_num = min(max_num / msg_remain, 13)
                    min_num = max(max_num-7, 1)
                    if max_num <= min_num:
                        self.deliver_reply = min_num
                    else:
                        self.deliver_reply = renpy.random.randint(min_num,
                                                                    max_num)
                else:
                    self.deliver_reply = renpy.random.randint(5, 10)

            self.sent_time = upTime()
            self.timeout_count = 2
            self.set_attendance()
            renpy.retain_after_load()

        def set_attendance(self):
            """Set whether this guest is attending the party."""

            if self.completed():
                # 3/3 messages correct
                self.guest.attending = True
            elif self.timeout:
                self.guest.attending = False
            elif self.is_failed():
                # 2/3 messages correct
                if self.second_msg() == 'email_good':
                    self.guest.attending = renpy.random.choice([True,
                                                            True, False])
                # 1/3 messages correct
                elif self.first_msg() == 'email_good':
                    self.guest.attending = renpy.random.choice([True,
                                                            False, False])
                else:
                    self.guest.attending = False
            return

        def add_msg(self, iscorrect):
            """Add the player's message to the guest to the email."""

            the_msg = ""

            if iscorrect:
                if self.msg_num == 0:
                    the_msg = self.guest.msg1_good
                elif self.msg_num == 1:
                    the_msg = self.guest.msg2_good
                elif self.msg_num == 2:
                    the_msg = self.guest.msg3_good
            else:
                if self.msg_num == 0:
                    the_msg = self.guest.msg1_bad
                elif self.msg_num == 1:
                    the_msg = self.guest.msg2_bad
                elif self.msg_num == 2:
                    the_msg = self.guest.msg3_bad

            self.msg_num += 1
            the_msg += "\n\n------------------------------------------------\n\n"
            self.msg = the_msg + self.msg
            renpy.retain_after_load()

        def completed(self):
            """Return True if the email chain was successfully completed."""

            if self.failed or not self.read:
                return False
            if self.msg_num == 3 and self.reply == False:
                return True
            else:
                return False

        def is_failed(self):
            """Return True if the email chain was failed."""
            if self.failed and self.read and not self.reply:
                return True
            else:
                return False

        def first_msg(self):
            """Return the email icon for the first message."""

            if self.msg_num <= 0:
                return 'email_inactive'
            elif self.msg_num == 1 and self.failed:
                return 'email_bad'
            else:
                return 'email_good'

        def second_msg(self):
            """Return the email icon for the second message."""

            if self.msg_num <= 1:
                return 'email_inactive'
            elif self.msg_num == 2 and self.failed:
                return 'email_bad'
            else:
                return 'email_good'

        def third_msg(self):
            """Return the email icon for the third message."""

            if self.msg_num <= 2:
                return 'email_inactive'
            elif self.msg_num == 3 and self.failed:
                return 'email_bad'
            else:
                return 'email_good'

        def send_reply(self):
            """Send the email reply."""

            global email_reply
            email_reply = True
            renpy.call_in_new_context(self.reply_label)
            email_reply = False
            renpy.retain_after_load()
            return

        def send_sooner(self):
            """Increase the timeout and deliver_reply counters. For testing."""

            if self.deliver_reply != "wait":
                self.deliver_reply -= 5
            self.timeout_count -= 5


    class Guestv2(renpy.store.object):
        """
        This class stores necessary information about the guest, including
        all of their email replies as well as their image thumbnail and name.
        It is used for program versions earlier than v3.0.

        Attributes:
        -----------
        name : string
            Name of the guest as it shows up in email replies.
        thumbnail : string
            File path to the thumbnail used for this guest's emails. Ideally
            155x155 pixels.
        start_msg : string
            Initial message sent to the player upon agreeing to invite
            this guest.
        msg1_good : string
            Player's correct response to the first email.
        msg2_good : string
            Player's correct response to the second email.
        msg3_good : string
            Player's correct response to the third email.
        reply1_good : string
            Guest's response to the first correct reply.
        reply2_good : string
            Guest's response to the second correct reply.
        reply3_good : string
            Guest's response to the third correct reply.
        reply1_bad : string
            Guest's response to the first incorrect reply.
        reply2_bad : string
            Guest's response to the second incorrect reply.
        reply3_bad : string
            Guest's response to the third incorrect reply.
        msg1_bad : string
            Player's incorrect response to the first email.
        msg2_bad : string
            Player's incorrect response to the second email.
        msg3_bad : string
            Player's incorrect response to the third email.
        label1 : string
            Label to jump to to answer the first email.
        label2 : string
            Label to jump to to answer the second email.
        label3 : string
            Label to jump to to answer the third email.
        attending : bool
            True if the guest is attending the party.
        large_img : string
            File path to the full-body image of this guest. Shown when
            they attend the party.
        short_desc : string
            Short description of the guest, shown in the guestbook.
        personal_info : string
            A longer description of the guest, viewable only after they
            have attended the party.
        comment_who : ChatCharacter
            The ChatCharacter object of the character who will talk about
            this guest in the guestbook.
        comment_what : string
            What the comment_who character will say about the guest.
        comment_img : string
            A string corresponding to a defined image or layeredimage attributes
            that will be used to display the sprite of the character speaking
            about this guest e.g. "zen front party happy".
        dialogue_name : string
            The name of the guest as it should appear in their dialogue box
            when they arrive at the party e.g. "Long Cat"
        dialogue_what : string
            The guest's comment upon arriving at the party.
        """

        def __init__(self, name, thumbnail, start_msg,
                        msg1_good, reply1_good, msg1_bad, reply1_bad,
                        msg2_good, reply2_good, msg2_bad, reply2_bad,
                        msg3_good, reply3_good, msg3_bad, reply3_bad,
                        large_img=False, short_desc="", personal_info="",
                        comment_who=None, comment_what="", comment_img='#000',
                        dialogue_name="", dialogue_what=""):
            """
            Create a Guest object to store information about their emails
            and guestbook details.

            Parameters:
            -----------
            name : string
                Name of the guest as it shows up in email replies.
            thumbnail : string
                File path to the thumbnail used for this guest's emails. Ideally
                155x155 pixels.
            start_msg : string
                Initial message sent to the player upon agreeing to invite
                this guest.
            msg1_good : string
                Player's correct response to the first email.
            reply1_good : string
                Guest's response to the first correct reply.
            msg1_bad : string
                Player's incorrect response to the first email.
            reply1_bad : string
                Guest's response to the first incorrect reply.
            msg2_good : string
                Player's correct response to the second email.
            reply2_good : string
                Guest's response to the second correct reply.
            msg2_bad : string
                Player's incorrect response to the second email.
            reply2_bad : string
                Guest's response to the second incorrect reply.
            msg3_good : string
                Player's correct response to the third email.
            reply3_good : string
                Guest's response to the third correct reply.
            msg3_bad : string
                Player's incorrect response to the third email.
            reply3_bad : string
                Guest's response to the third incorrect reply.
            large_img : string
                File path to the full-body image of this guest. Shown when
                they attend the party.
            short_desc : string
                Short description of the guest, shown in the guestbook.
            personal_info : string
                A longer description of the guest, viewable only after they
                have attended the party.
            comment_who : ChatCharacter
                The ChatCharacter object of the character who will talk about
                this guest in the guestbook.
            comment_what : string
                What the comment_who character will say about the guest.
            comment_img : string
                A string corresponding to a defined image or layeredimage
                attributes that will be used to display the sprite of the
                character speaking about this guest e.g. "zen front party happy"
            dialogue_name : string
                The name of the guest as it should appear in their dialogue box
                when they arrive at the party e.g. "Long Cat"
            dialogue_what : string
                The guest's comment upon arriving at the party.
            """

            self.name = name
            self.thumbnail = thumbnail

            self.start_msg = start_msg
            self.msg1_good = msg1_good
            self.msg2_good = msg2_good
            self.msg3_good = msg3_good

            self.reply1_good = reply1_good
            self.reply2_good = reply2_good
            self.reply3_good = reply3_good

            self.reply1_bad = reply1_bad
            self.reply2_bad = reply2_bad
            self.reply3_bad = reply3_bad

            self.msg1_bad = msg1_bad
            self.msg2_bad = msg2_bad
            self.msg3_bad = msg3_bad

            # Make sure the name does not have spaces or apostrophes
            name = convert_to_file_name(name)

            self.label1 = name + '_reply1'
            self.label2 = name + '_reply2'
            self.label3 = name + '_reply3'

            self.attending = False

            self.large_img = large_img
            self.short_desc = short_desc
            self.personal_info = personal_info
            self.comment_who = comment_who
            self.comment_what = comment_what
            self.comment_img = comment_img
            self.dialogue_name = dialogue_name
            self.dialogue_what = dialogue_what

            # Attempt to set some of the comment info manually if not provided
            if not self.large_img:
                self.large_img = self.thumbnail
            if not self.short_desc:
                self.short_desc = ("No description was entered in this guest's"
                    + " Guest definition.")
            if not self.personal_info:
                self.personal_info = ("No personal info was given in this"
                    " guest's Guest definition")
            if not self.comment_who:
                self.comment_who = store.narrator
            if not self.comment_what:
                self.comment_what = "No comment was entered for this guest."
            if not self.dialogue_name:
                self.dialogue_name = string.capwords(self.name)
            if not self.dialogue_what:
                self.dialogue_what = "This guest was not given anything to say."

            # Add the guest to the guestbook
            if self.name not in store.persistent.guestbook:
                store.persistent.guestbook[self.name] = None
            if self not in store.all_guests:
                store.all_guests.append(self)

        def __eq__(self, other):
            """Check for equality between Guestv2 objects."""

            if (getattr(other, 'name', False)
                    and getattr(other, 'thumbnail', False)):
                return (self.name == other.name
                        and self.thumbnail.split('.')[0]
                            == other.thumbnail.split('.')[0])
            else:
                return False

        def __ne__(self, other):
            """Check for inequality between Guestv2 objects."""

            return not self.__eq__(other)

    class Guestv3(renpy.store.object):
        """
        This class stores necessary information about the guest, and will
        automatically generate the menus for the player to reply to their
        emails.

        Attributes:
        -----------
        name : string
            Name of the guest as it shows up in email replies.
        dialogue_name : string
            The name of the guest as it should appear in their dialogue box
            when they arrive at the party e.g. "Long Cat".
        thumbnail : string
            File path to the thumbnail used for this guest's emails. Ideally
            155x155 pixels.
        large_img : string
            File path to the full-body image of this guest. Shown when
            they attend the party.
        short_desc : string
            Short description of the guest, shown in the guestbook.
        personal_info : string
            A longer description of the guest, viewable in the guestbook only
            after they have attended the party.
        start_msg : string
            Initial message sent to the player upon agreeing to invite
            this guest.
        choices : EmailReply[]
            A list of EmailReply objects containing the choices offered to
            reply to each email.
        num_correct : int
            The number of emails the player must exchange with the guest to
            fully complete the email chain.
        dialogue_what : string
            The guest's comment upon arriving at the party.
        comment_who : ChatCharacter
            The ChatCharacter object of the character who will talk about
            this guest in the guestbook.
        comment_what : string
            What the comment_who character will say about the guest.
        comment_img : string
            A string corresponding to a defined image or layeredimage attributes
            that will be used to display the sprite of the character speaking
            about this guest e.g. "zen front party happy".
        attending : bool
            True if the guest is attending the party.
        reply_icons : string[]
            A list of the types of icons that should be used to display
            whether a particular email in the chain was passed or failed.
        """

        def __init__(self, name, dialogue_name, thumbnail, large_img,
                short_desc, personal_info, start_msg, choices,
                num_correct=3, dialogue_what=None, comment_who=None,
                comment_what=None, comment_img=None):

            self.name = name
            self.dialogue_name = dialogue_name
            self.thumbnail = thumbnail
            self.large_img = large_img
            self.short_desc = short_desc
            self.personal_info = personal_info
            self.start_msg = start_msg
            self.choices = choices
            self.num_correct = num_correct
            self.dialogue_what = dialogue_what or ("This guest was not "
                + "given anything to say.")
            self.comment_who = comment_who or store.narrator
            self.comment_what = comment_what or ("No comment was entered "
                + "for this guest")
            self.comment_img = comment_img or "#000"

            self.attending = False
            self.reply_icons = []

            if self.name not in store.persistent.guestbook:
                store.persistent.guestbook[self.name] = None
            if self not in store.all_guests:
                store.all_guests.append(self)

        def __eq__(self, other):
            """Check for equality between Guestv3 objects."""

            if (getattr(other, 'name', False)
                    and getattr(other, 'thumbnail', False)):
                return (self.name == other.name
                        and self.thumbnail.split('.')[0]
                            == other.thumbnail.split('.')[0])
            else:
                return False

        def __ne__(self, other):
            """Check for inequality between Guestv3 objects."""

            return not self.__eq__(other)



    class EmailReply(renpy.store.object):
        """
        A class intended to facilitate writing email replies.

        Attributes:
        -----------
        choice_text : string
            The text of the choice to reply to the email.
        player_msg : string
            The message the player writes after the choice is made.
        guest_reply : string
            The guest's reply to the player's message.
        continue_chain : EmailReply[]
            If this email chain will continue after the player selects this
            reply, this is a list of EmailReply objects that will be available
            the next time the player is given the opportunity to reply.
        email_success : bool or None
            If explicitly set to a boolean value, this indicates if it ends
            the email chain in a good (True) or bad (False) way.
        """

        def __init__(self, choice_text, player_msg, guest_reply,
                continue_chain=None, email_success=None):

            self.choice_text = choice_text
            self.player_msg = player_msg
            self.guest_reply = guest_reply
            self.continue_chain = continue_chain or []
            self.email_success = email_success




    def Guest(*args):
        # Returns an appropriate Guest object depending on which version the
        # user is on.
        if store.use_2_2_guest:
            # Use the old Guest style
            return Guestv2(*args)
        # Otherwise, use the new Guest style
        return Guestv3(*args)

    def unread_emails():
        """Return the number of unread emails in the player's inbox."""

        unread = [ x for x in store.email_list if not x.read]
        return len(unread)

    def deliver_emails():
        """Deliver the emails in email_list."""

        for e in store.email_list:
            e.deliver()

    def attending_guests():
        """
        Return the number of guests attending the party. If a guest's email
        chain is completed, they are guaranteed to come. If two email messages
        were correct and the third was incorrect, the guest has a 67% chance
        of coming. If the first message was correct and the second was not,
        the guest has a 33% chance of coming. Guests will only attend if all
        of their messages have been replied to and read.
        """

        num_guests = 0
        for e in store.email_list:
            if e.guest.attending:
                num_guests += 1
        return num_guests

default email_list = []
default email_reply = False
# List of all the guests the player has successfully
# invited to the party
default persistent.guestbook = { }
default all_guests = [ ]
default current_email = None

########################################################
## This screen shows a popup to notify you when you
## have a new email
########################################################
screen email_popup(e):

    #modal True
    zorder 100

    frame:
        style_prefix 'email_popup'
        imagebutton:
            align (1.0, 0.0)
            idle 'input_close'
            hover 'input_close_hover'
            action Hide('email_popup')
        hbox:
            add 'new_text_envelope'
            text 'NEW'
        vbox:
            hbox:
                style_prefix 'email_popup2'
                add Transform(e.guest.thumbnail, zoom=0.6)
                text "You have a new message from @" + e.guest.name

            # This button takes you directly to the email. It is
            # included so long as the email popup is not shown
            # during phone calls or chatrooms.
            textbutton _('Go to'):
                if (not (renpy.get_screen('in_call')
                        or renpy.get_screen('incoming_call')
                        or renpy.get_screen('outgoing call'))):
                    action If (((not (renpy.get_screen('in_call')
                            or renpy.get_screen('incoming_call')
                            or renpy.get_screen('outgoing call')))),
                        [Hide('email_popup'),
                            Hide('save_load'),
                            Hide('menu'),
                            Hide('chat_footer'),
                            Hide('phone_overlay'),
                            Hide('settings_screen'),
                            Show('email_hub')], None)

    timer 3.25 action Hide('email_popup', Dissolve(0.25))

style email_popup_frame:
    xysize (510,300)
    background 'left_corner_menu_dark'
    xalign 0.5
    yalign 0.4

style email_popup_hbox:
    yalign 0.09
    xalign 0.05
    spacing 15

style email_popup_text:
    color '#73f1cf'
    yalign 1.0
    font gui.sans_serif_1b

style email_popup_vbox:
    align (0.5, 0.72)
    spacing 15
    xysize (450, 100)

style email_popup_button:
    xalign 0.5
    xsize 220
    ysize 70
    padding (20,20)
    background 'menu_select_btn'
    hover_foreground 'menu_select_btn_hover'

style email_popup_button_text:
    is mode_select
    size 28

style email_popup2_hbox:
    align (0.5, 0.5)
    xsize 470
    spacing 10

style email_popup2_text:
    color '#fff'
    size 25
    align(0.5, 0.5)


########################################################
## This screen shows a list of the emails you've
## received
########################################################
screen email_hub():

    tag menu

    default current_page = 0
    default num_pages = (len(email_list) + 7 - 1) // 7

    on 'replace' action FileSave(mm_auto, confirm=False)
    on 'show' action FileSave(mm_auto, confirm=False)


    use menu_header('Email', Show('chat_home', Dissolve(0.5))):
        frame:
            style_prefix 'email_hub'
            has vbox
            null height -15
            if len(email_list) == 0:
                text "Inbox is empty"
            for e in email_list[current_page*7:current_page*7+7]:
                use email_button(e)

        hbox:
            style_prefix 'email_hub'
            imagebutton:
                idle Transform("email_next", xzoom=-1)
                align (0.5, 0.5)
                if current_page > 0:
                    action SetScreenVariable('current_page', current_page-1)
                    activate_sound 'audio/sfx/UI/email_next_arrow.mp3'

            for index in range(num_pages):
                textbutton _(str(index+1)):
                    action SetScreenVariable('current_page', index)

            imagebutton:
                idle "email_next"
                align (0.5, 0.5)
                if current_page < num_pages - 1:
                    action SetScreenVariable('current_page', current_page+1)
                    activate_sound 'audio/sfx/UI/email_next_arrow.mp3'

style email_hub_frame:
    background 'left_corner_menu'
    padding (20,20)
    xysize (685, 1100)
    align (0.5, 0.75)

style email_hub_vbox:
    spacing 40
    align (0.5, 0.0)

style email_hub_text:
    color '#fff'
    xalign 0.5
    yalign 0.0

style email_hub_hbox:
    align (0.5, 0.99)
    spacing 15

style email_hub_button:
    align (0.5, 0.5)
    activate_sound 'audio/sfx/UI/email_next_arrow.mp3'

style email_hub_image_button:
    is email_hub_button

style email_hub_button_text:
    color '#fff'


########################################################
## This shows the buttons you can click on in order to
## open and read your emails
########################################################
screen email_button(e):
    button:
        style_prefix 'email_btn'
        if e.read:
            background 'email_panel'
        else:
            background 'email_mint'

        action [SetVariable("current_email", e),
                SetField(e, 'read', True),
                Show('open_email', e=e)]

        hbox:
            fixed:
                if not e.read:
                    add 'email_unread' align(1.0, 0.5)
                elif e.reply_label:
                    add 'email_read' align(1.0, 0.5)
                else:
                    add 'email_replied' align(1.0, 0.5)
            add Transform(e.guest.thumbnail, size=(94, 94)) align(0.5, 0.3)
            null width -10
            vbox:
                frame:
                    text '@' + e.guest.name
                hbox:
                    align(0.3, 0.5)
                    spacing 8
                    add e.first_msg()
                    add e.second_msg()
                    add e.third_msg()
            frame:
                xysize(240,90)
                align (0.0, 0.3)
                if e.completed():
                    # 3/3 messages correct
                    add 'email_completed_3' align(0.5, 0.5)
                elif e.is_failed():
                    # 2/3 messages correct
                    if e.second_msg() == 'email_good':
                        add 'email_completed_2' align(0.5, 0.5)
                    # 1/3 messages correct
                    elif e.first_msg() == 'email_good':
                        add 'email_completed_1' align(0.5, 0.5)
                    # 0/3 messages correct
                    else:
                        add 'email_failed' align(0.5, 0.5)
                elif e.timeout:
                    add 'email_timeout' align(0.5, 0.5)

style email_btn_button:
    align (0.5, 0.5)
    xysize (644, 111)
    hover_foreground 'white_transparent'

style email_btn_hbox:
    align (0.0, 0.0)
    spacing 10

style email_btn_fixed:
    xysize (80,111)
    align (0.5, 0.5)

style email_btn_vbox:
    align(0.5, 0.2)
    spacing 12

style email_btn_frame:
    align(0.0, 0.0)
    xysize(185, 38)

style email_btn_text:
    font gui.curlicue_font
    color '#fff'
    size 27
    align (0.0, 0.0)


########################################################
## This is the screen that displays the email you've
## selected, and lets you reply
########################################################
screen open_email(e):
    modal True
    zorder 100

    add 'choice_darken'

    frame:
        style_prefix 'open_email'
        imagebutton:
            idle 'input_close'
            hover 'input_close_hover'
            action Hide('open_email')
        vbox:
            hbox:
                add e.guest.thumbnail
                vbox:
                    spacing 10
                    fixed:
                        text 'From: ' + e.guest.name
                    text ('[[Date] ' + e.sent_time.month_num
                            + '/' + e.sent_time.day):
                                size 27
                    text ('[[Time] ' + e.sent_time.get_twelve_hour()):
                                size 27

                textbutton _('Reply'):
                    if e.reply_label and not e.reply and not e.timeout:
                        action e.send_reply
                    else:
                        foreground 'menu_select_btn_inactive'

            frame:
                style 'open_email_frame2'
                viewport:
                    scrollbars 'vertical'
                    mousewheel True
                    draggable True
                    text e.msg size 28 color "#000"

style open_email_frame:
    maximum(685, 800)
    background 'left_corner_menu_dark' padding(20,20)
    align (0.5, 0.5)

style open_email_image_button:
    align (1.0, 0.0)
    xoffset 20
    yoffset -20

style open_email_vbox:
    spacing 15
    align (0.0, 0.0)

style open_email_hbox:
    spacing 10
    align (0.0, 0.0)

style open_email_fixed:
    align (0.0, 0.0)
    xsize 280
    ysize 80

style open_email_text:
    color "#fff"

style open_email_button:
    align (0.5, 1.0)
    xsize 170
    ysize 70
    size 28
    background 'menu_select_btn'
    padding (20,20)
    hover_foreground 'menu_select_btn_hover'

style open_email_button_text:
    is mode_select

style open_email_frame2:
    background 'email_open_transparent'
    padding(20,20)
    xysize (625, 585)
    align (0.5,0.5)

style open_email_viewport:
    align (0.5, 0.5)
    xysize (585, 545)



## This is the label you call at the end of
## an email choice menu
label email_end():
    $ renpy.retain_after_load()
    return

image img_locked = "CGs/album_unlock.webp"

screen guestbook():
    tag menu

    if not main_menu:
        on 'replace' action FileSave(mm_auto, confirm=False)
        on 'show' action FileSave(mm_auto, confirm=False)

    if main_menu:
        $ return_action = Show('select_history', Dissolve(0.5))
    else:
        $ return_action = Show('chat_home', Dissolve(0.5))
    $ num_rows = -(-len(persistent.guestbook) // 4)
    use menu_header("Guest", return_action):
        vpgrid id 'guest_vp':
            xysize (740, 1200)
            yfill True
            rows num_rows
            cols 4
            draggable True
            mousewheel True
            scrollbars "vertical"
            side_xalign 1.0
            side_spacing 15
            align (0.5, 1.0)
            spacing 20

            for guest in all_guests:
                button:
                    xysize (155, 155)
                    # Do some checks on whether the player
                    # finished inviting the guest or not
                    if persistent.guestbook[guest.name] == "seen":
                        # The player has invited this guest but the
                        # guest hasn't attended the party
                        background guest.thumbnail
                        action Show('guest_info_popup',
                                guest=guest, unlocked=False)
                    elif (persistent.guestbook[guest.name] == "attended"
                            or persistent.guestbook[guest.name] == 'viewed'):
                        # The guest has attended the party
                        background guest.thumbnail
                        action Show('guest_info_popup',
                            guest=guest, unlocked=True)
                    else:
                        # This guest is unknown to the player
                        background 'img_locked'
                        action CConfirm("You have not yet\nencountered this guest")

            for i in range((4*num_rows) - len(persistent.guestbook)):
                null

image guest_story = 'Email/story_available.webp'
image guest_story_locked = 'Email/story_locked.webp'
image guest_descrip_bg = Frame('Email/guest_orange_shade.webp', 0, 0)

default viewing_guest = False
screen guest_info_popup(guest, unlocked):

    modal True
    add "#0005"
    frame:
        style_prefix "guest_info"
        has fixed
        yfit True
        imagebutton:
            idle 'input_close'
            hover 'input_close_hover'
            action [Hide('guest_info_popup')]
        vbox:
            text '@[guest.name]':
                size 40 font gui.sans_serif_1b xoffset 40
            text guest.short_desc:
                size 28 text_align 0.5 xalign 0.5 layout 'subtitle'
            null height 5
            hbox:
                style_prefix 'guest_desc'
                vbox:
                    text "[[Personal Info]" size 25 font gui.sans_serif_1b
                    frame:
                        if unlocked:
                            text guest.personal_info
                        else:
                            vbox:
                                null height 10
                                add 'plot_lock' align (0.5, 0.5)
                                text ("Information will be unlocked when"
                                + " this guest attends the party.")
                vbox:
                    fixed:
                        xsize 620//2
                        yfit True
                        align (0.5, 0.5)
                        add guest.large_img
                    fixed:
                        xysize (int(273*1.1), int(93*1.1))
                        imagebutton:
                            align (0.5, 0.5)
                            if unlocked:
                                idle 'guest_story'
                                hover Transform('guest_story', zoom=1.1)
                                action [Preference('auto-forward',
                                        'disable'),
                                    Replay('guest_info',
                                    {'guest_replay_info' :
                                        guest}, False),
                                    SetDict(persistent.guestbook,
                                        guest.name, 'viewed'),
                                    Function(renpy.retain_after_load)]
                            else:
                                idle 'guest_story_locked'

default guest_replay_info = None
label guest_info():
    python:
        who = guest_replay_info.comment_who
        what = guest_replay_info.comment_what
        expr = guest_replay_info.comment_img

        # Award an hourglass if this is the first time
        # the player has seen this guest's guestbook
        if persistent.guestbook[guest_replay_info.name] == 'attended':
            persistent.guestbook[guest_replay_info.name] = 'viewed'
            if not persistent.animated_icons:
                renpy.show_screen(allocate_notification_screen(False),
                    message="Hourglass +1")
            else:
                renpy.show_screen(allocate_hg_screen())
            renpy.music.play("audio/sfx/UI/select_4.mp3", channel='sound')
            persistent.HG += 1

    $ begin_timeline_item(StoryMode("Guest", "guest_info", "00:00"))
    $ viewing_guest = True
    scene bg rfa_party_3
    show expression expr
    who "[what]"
    $ viewing_guest = False
    $ renpy.end_replay()
    return

style guest_info_frame:
    background 'input_popup_bkgr'
    align (0.5, 0.5)
    xsize 630
    yminimum 400
    ymaximum 900

style guest_info_image_button:
    align (1.0, 0.0)
    yoffset -3 xoffset 3

style guest_info_vbox:
    xalign 0.5
    xsize 620
    spacing 30
    yoffset 20

style guest_info_text:
    color "#fff"

style guest_desc_vbox:
    spacing 10
    yalign 0.5

style guest_desc_text:
    color "#fff"

style guest_desc_frame:
    background 'guest_descrip_bg'
    padding (5, 5)
    xsize 620//2-30
