# This variable keeps track of all the routes you've defined in order
# to display it in the History screen from the main menu.
# You should generally not need to modify it.
init -7:
    default all_routes = []

# This archive will store every chatroom in the game. If done correctly,
# the program will automatically set variables and make the story available
# for you.
default chat_archive = None
default story_archive = []

default tutorial_good_end = ["Good End",
    RouteDay('Tutorial',
        [ChatRoom('Example Chatroom', 'example_chat', '00:01'),
        ChatRoom('Inviting Guests','example_email', '09:11', [z]),
        ChatRoom('Text Message Example', 'example_text', '09:53', [r]),
        ChatRoom('Timed Menus', 'timed_menus', '11:28', [s]),
        ChatRoom('Other Storytelling Features', 'other_storytelling', '13:44', [y]),
        ChatRoom('Pass Out After Drinking Caffeine Syndrome', 'tutorial_chat', '15:05', [s]),
        ChatRoom('Invite to the meeting', 'popcorn_chat', '18:25', [ja, ju], save_img='ju'),
        StoryMode("Story Mode without Chatrooms", "example_solo_vn", "19:55", v),
        ChatRoom('Hacking', 'hack_example', '20:41'),
        ChatRoom('Plot Branches', 'plot_branch_tutorial', '21:44', [], plot_branch=PlotBranch(True)),
        ChatRoom("Onwards!", 'tutorial_end_example', '22:26', [u]),
        TheParty('tutorial_good_end_party', '23:54')
        ]),
    RouteDay('1st'),
    RouteDay('2nd'),
    RouteDay('3rd'),
    RouteDay('4th'),
    RouteDay('5th'),
    RouteDay('6th'),
    RouteDay('7th'),
    RouteDay('8th'),
    RouteDay('9th'),
    RouteDay('10th'),
    RouteDay('Final')]

default tutorial_bad_end = ["Bad Story End",
    RouteDay('Tutorial',
        [ChatRoom('An Unfinished Task', 'tutorial_bad_end', '23:26', [v])] )]
default tutorial_bre = ["Bad Relationship End",
    RouteDay('Tutorial',
            branch_vn=BranchStoryMode('plot_branch_bre'))]
default tutorial_normal_end = ["Normal End",
    RouteDay('Tutorial',
        [TheParty('plot_branch_normal_end', '23:54')])]

default tutorial_route = Route(
                        default_branch=tutorial_good_end,
                        branch_list=[tutorial_normal_end,
                                     tutorial_bad_end,
                                     tutorial_bre],
                        route_history_title='Tutorial',
                        history_background="Menu Screens/Main Menu/tutorial_day_route_bg.webp")




# This is an example of how multiple routes may be set up to all
# be displayed properly in the History

# default seven_good_end = ["Good End", RouteDay("5th", [...])]
# default seven_bad_end_1 = ["Bad Story End 1", RouteDay("7th", [...])]
# default seven_bad_end_2 = ["Bad Story End 2", RouteDay("9th", [...])]
# default seven_bad_end_3 = ["Bad Story End 3", RouteDay("10th", [...])]
# default seven_bre_1 = ["Bad Relationship End 1", RouteDay("7th", [...])]
# default seven_bre_2 = ["Bad Relationship End 1", RouteDay("10th", [...])]
# default seven_normal_end = ["Normal End", RouteDay("Final",
#                                 [TheParty('seven_route_normal_party', '12:00')])]

# default seven_route = Route(
#     default_branch=seven_good_end,
#     branch_list=[seven_bad_end_1, seven_bad_end_2,
#         seven_bad_end_3, seven_bre_1, seven_bre_2, seven_normal_end],
#         route_history_title="707")

# default zen_good_end = ["Good End", RouteDay("5th", [...])]
# default zen_bad_end_1 = ["Bad Story End 1", RouteDay("7th", [...])]
# default zen_bad_end_2 = ["Bad Story End 2", RouteDay("9th", [...])]
# default zen_bad_end_3 = ["Bad Story End 3", RouteDay("10th", [...])]
# default zen_bre_1 = ["Bad Relationship End 1", RouteDay("7th", [...])]
# default zen_bre_2 = ["Bad Relationship End 2", RouteDay("10th", [...])]
# default zen_normal_end = ["Normal End", RouteDay("Final",
#                                 [TheParty('zen_route_normal_party', '12:00')])]

# default zen_route = Route(
#     default_branch=zen_good_end,
#     branch_list=[zen_bad_end_1, zen_bad_end_2,
#     zen_bad_end_3, zen_bre_1, zen_bre_2, zen_normal_end],
#     route_history_title="ZEN")

# default common_route_good = ["Good End", RouteDay("1st", [...])]
# default common_route_bad = ["Bad Story End", RouteDay("4th", [...])]

# default common_route = Route(
#     default_branch=common_route_good,
#     branch_list=[common_route_bad],
#     route_history_title="Common",
#     has_good_end=False)
