from game import Game


# create the game object

# g.show_start_screen()

while True:
    g = Game()
    print("Tasks done: " + str(g.missions_done))
    g.menu.game_intro()

    del g

    # g.missions_done == 0
    # g.new() # create sprites/objects/walls
    # g.run() # run the game function
s.close()


