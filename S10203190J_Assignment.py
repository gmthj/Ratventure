#Tan Hiang Joon Gabriel (S10203190) P06
#PRG1 Assignment

###############################################################
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#this program will write text files to the same location
#that this python file is saved in your machine
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
###############################################################

from random import randint
import sys

#Text for various menus
main_text = ["New Game",\
             "Resume Game",\
             "View Leaderboard",\
             "Exit Game"]

town_text = ["View Character",\
             "View Map",\
             "Move",\
             "Rest",\
             "Save Game",\
             "Exit Game"]

open_text = ["View Character",\
             "View Map",\
             "Move",\
             "Sense Orb",\
             "Exit Game"]

fight_text = ["Attack",\
              "Run"]

# world_map = [['H/T', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
#              [' ', ' ', ' ', 'T', ' ', ' ', ' ', ' '],\
#              [' ', ' ', ' ', ' ', ' ', 'T', ' ', ' '],\
#              [' ', 'T', ' ', ' ', ' ', ' ', ' ', ' '],\
#              [' ', ' ', ' ', ' ', ' ', ' ', 'O', ' '],\
#              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
#              [' ', ' ', ' ', ' ', 'T', ' ', ' ', ' '],\
#              [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'K']]

# enemy_state = [['T', '1', '1', '1', '1', '1', '1', '1'],\
#                ['1', '1', '1', 'T', '1', '1', '1', '1'],\
#                ['1', '1', '1', '1', '1', 'T', '1', '1'],\
#                ['1', 'T', '1', '1', '1', '1', '1', '1'],\
#                ['1', '1', '1', '1', '1', '1', '1', '1'],\
#                ['1', '1', '1', '1', '1', '1', '1', '1'],\
#                ['1', '1', '1', '1', 'T', '1', '1', '1'],\
#                ['1', '1', '1', '1', '1', '1', '1', 'K']]

start_stats = ['Name\n', 'The Hero\n', 'Damage\n', '[2, 4]\n', 'Defence\n', '1\n', 'HP\n', '20\n', 'Day\n', '1\n']
orb_of_power = 0 #0:False: not holding orb; 1:True:holding orb

#function to display options of the input menu; gets user input for menu choice; returns choice number
def menu_choice(menu):
    for i in range(len(menu)): #displays menu based on items in menu
        print(str(i + 1) + ') ' + menu[i])

    choice = input('Enter choice: ') #gets choice input from user
    while not choice.isdigit() or int(choice) < 1 or int(choice) > len(menu): #validating choice is from 1 to length of menu
        print('Invalid choice.') #error message
        choice = input('Enter choice: ') #get choice again
    print()
    return choice

#generates new game save file; returns save file name
def new_game_save_file_name():
    try:
        file = open('records_save_file.txt', 'r')
        lines = file.readlines() #each line in records_save_file.txt stored as an item in a list lines
        save_count = str(int(lines[0][6:-1]) + 1) #obtains current save count number from record file
        file.close()

        lines[0] = lines[0][:6] + save_count + '\n' #changes the save count in the list lines

        file = open('records_save_file.txt', 'w')
        file.writelines(lines) #rewrites the new data into the record file
        file.close()

        file = open('save_file_' + save_count + '.txt', 'w') #creating new save file using save count number
        file.writelines(start_stats) #initialise character stats into save file

        world_map = gen_new_map()
        for line in world_map: #initialise world map into save file
            file.write(str(line) + '\n')

        for line in gen_enemy(world_map): #initialise enemy states into save file
            file.write(str(line) + '\n')

        file.write('orb of power\n' + str(orb_of_power) + '\n') #initialise orb state, 0:False: not holding orb; 1:True:holding orb

        file.close()
        return 'save_file_' + save_count + '.txt' #outputs save file name

    except FileNotFoundError: #in the odd case that the record file gets deleted midway through the game
        print('Error! Records save file removed.\nReinitialising records save file') #display error message
        file = open('records_save_file.txt','w')
        file.write('saves:0\nhighscores:[0, 0, 0, 0, 0]') #reinitialises record file start data
        file.close()
        return new_game_save_file_name() #runs the function again to continue to start a new game

#returns day state message based on character location
def day_location(world_map):
    for row in world_map: #cycles through each spot on the map looking for character location: 'H'
        for spot in row: #and returns appropriate day state message
            if spot == 'H/T':
                return 'You are in a town.'
            if spot == 'H/K':
                return 'You see the Rat King!'
            if spot == 'H' or spot == 'H/O': #outdoor or on the orb but still outdoor
                return 'You are out in the open.'

#displays world map
def view_map():
    line_break = '+---+---+---+---+---+---+---+---+'
    for row in world_map:
        print(line_break) #adds line break before every row
        for col in row:
            if col == 'O': #does not display the orb of power
                col = ' '
            if col == 'H/O':
                col = 'H'
            print('|{:^3}'.format(col),end = '')
        print('|') #adds | at the end of each row
    print(line_break) #adds line break again at the very end

#displays character's stats
def view_character():
    print(character_stats[1]) #displays hero name
    print('{:>8}: {}-{}'.format(character_stats[2],character_stats[3][0],character_stats[3][1])) #displays damage stats

    for i in range(4,8,2): #displays rest of character stats: defence, health
        print('{:>8}: {}'.format(character_stats[i],character_stats[i+1]))

    if bool(int(orb_of_power)): #displays holding orb message if orb_of_power is 1: True, holding orb
        print('You are holding the Orb of Power.')
    print() #displays a blank line

#returns character's world map coordinates and cell state in the form of (row_index,col_index, cell state) as in (y,x)
def get_char_pos(char):
    for row_index in range(len(world_map)): #cycles through every spot in the world map
        for col_index in range(len(world_map[row_index])):
            if char in world_map[row_index][col_index]: #and looks for char ('H') in each spot
                hero_coordinates = [row_index, col_index, world_map[row_index][col_index]]
    return hero_coordinates #returns a list of the char coordinates and the spot contents

#returns a list of invalid moves; moves that would go out of the map
def move_wall_validation():
    hero_coordinates = get_char_pos('H') #gets current location

    invalid_moves = []
    if hero_coordinates[0] == 0: #checks if char is on the top row: cannot go up: w
        invalid_moves += ['W']
    if hero_coordinates[1] == 0: #checks if char is on the left column: cannot go left: a
        invalid_moves += ['A']
    if hero_coordinates[0] == 7: #checks if char is on the bottom row: cannot go down: s
        invalid_moves += ['S']
    if hero_coordinates[1] == 7: #checks if char is on the right column: cannot go right: d
        invalid_moves += ['D']
    return invalid_moves

#gets move direction choice with validation; returns plain english direct i.e. up, down, left, right
def move_direction():
    print('W = up; A = left; S = down; D = right')
    direct_dict = {'W' : 'up' , 'A' : 'left' , 'S' : 'down' , 'D' : 'right'}

    direction = input('Your move: ')
    #validates that choice is alphabetical and is 1 of the 4 valid moves and the valid move will not go out of the map
    while not direction.isalpha() or direction.upper() not in ['W', 'A', 'S', 'D'] or direction.upper() in move_wall_validation():
        print('Invalid move.') #displays invalid message
        if direction.upper() in move_wall_validation(): #checks if goes out of the map: to display a out of map message
            print('Cannot move out of map.')
        direction = input('Your move: ')

    direction = direction.upper()
    return direct_dict[direction] #returns plain english direction form the dictionary

#moves character on world_map
def move():
    view_map() #displays map before move
    direction = move_direction() #gets validated move direction
    hero_coordinates = get_char_pos('H') #gets character current location

    current_cell_old = hero_coordinates[2] #gets contents of the current character location i.e. 'H', 'H/T'...
    if current_cell_old != 'H': #checks if in non outdoor space i.e. 'H/T', 'H/K'...
        current_cell_new = current_cell_old[-1] #makes new cell the last item i.e. 'T', 'K'...
    else: #otherwise makes the new cell blank/open/' '
        current_cell_new = ' '
    world_map[hero_coordinates[0]][hero_coordinates[1]] = current_cell_new #changes the contents of current cell to the new cell contents

    #changes the coordinates based on the direction
    if direction == 'up':
        hero_coordinates[0] -= 1
    if direction == 'down':
        hero_coordinates[0] += 1
    if direction == 'left':
        hero_coordinates[1] -= 1
    if direction == 'right':
        hero_coordinates[1] += 1

    next_cell_old = world_map[hero_coordinates[0]][hero_coordinates[1]] #assigns the contents of the moved cell to the variable next_cell_old
    if next_cell_old != ' ': #checks for non empty cell i.e. 'T', 'K'...
        next_cell_new = 'H/' + next_cell_old #adds H/ to the front of the cell
    else:
        next_cell_new = 'H' #makes new cell 'H' otherwise
    world_map[hero_coordinates[0]][hero_coordinates[1]] = next_cell_new #change contents of moved cell in the world_map to the contents of the variable next_cell_new
    view_map() #displays map after move

#saves game; rewrites the current game stats into the specified save file: save_name
def save_game(save_name):
    file = open(save_name,'w')
    for stat in character_stats: #rewrites character stats into save file
        file.write(str(stat)+'\n')

    for line in world_map: #rewrites world map into save file
        file.write(str(line)+'\n')

    for line in enemy_state: #rewrites enemy states into save file
        file.write(str(line)+'\n')

    file.write('orb of power\n' + str(orb_of_power) + '\n') #rewrites orb state, holding orb -> True ,not holding orb -> False
    file.close()

#initiates combat sequence; takes in enemy name and current health of the enemy
def combat(enemy, health):
    enemy_stats = {'Rat':[1,3,1,10], 'Mutant Rat':[2,4,1,18], 'Rat King':[6,10,5,25]} #dictionary of enemy stats

    #displays formatted enemy stats
    print('Encounter! - {}\nDamage: {}-{}\nDefence:  {}\nHP: {}'.format(enemy, enemy_stats[enemy][0], enemy_stats[enemy][1], enemy_stats[enemy][2], health))

    combat_choice = menu_choice(fight_text) #displays combat menu and gets validated combat choice

    if combat_choice == '2': #run
        print('You run and hide.')
        health = enemy_stats[enemy][3] #resets enemy health to max since player runs
        open_choice = menu_choice(open_text) #displays outdoor menu and gets validated choice

        if open_choice == '3': #move; returns a string 'move' to break out of the combat sequence and prompt for a move
            return 'move'
        elif open_choice == '5': #exit; returns a string 'break' to break out of the combat sequence and prompt for a break to exit to the main menu
            return 'break'
        else: #all other choices results in an attack
            combat_choice = '1' #thus changeing the combat_choice to 1 to initiate the attack

    if combat_choice == '1': #attack
        if enemy == 'Rat King' and not bool(int(orb_of_power)): #displays immunity message and sets character's attack to 0 if enemy is king and Character not holding orb
            print('You do not have the Orb of Power - the Rat King is immune!')
            character_attack = 0
        else: #otherwise gets a random int between the character's damage range and subtracts the enemy's defence
            character_attack = randint(character_stats[3][0], character_stats[3][1]) - enemy_stats[enemy][2]

        enemy_attack = randint(enemy_stats[enemy][0],enemy_stats[enemy][1]) - character_stats[5] #calculates enemy's attack-same as above

        if character_attack > 0 or enemy == 'Rat King': #displays player to enemy attack message and adjusts enemy health accordingly
            print('You deal {} damage to the {}'.format(character_attack, enemy))
            health -= character_attack
        else: #displays block message if enemy's attack was <= character's defence (would not happen in the case of the current stats of the game as specified in the brief)
            print('The {} blocks your attack!'.format(enemy))

        if health > 0: #enemy not dead; display fight texts
            if enemy_attack > 0: #enemy's attack not blocked; continue fight texts
                print('Ouch! The {} hit you for {} damage!'.format(enemy, enemy_attack))
                character_stats[7] -= enemy_attack #adjust character health accordingly

                if character_stats[7] <= 0: #character is dead i.e. character health is 0 or less; display game over message and exit to main menu
                    print('You have 0 HP left.')
                    print('You are dead.\nGame over.\n')
                    return 'break' #returns a string 'break' to end combat sequence and promt for to break out of main game loop to the main menu
                else: #character not dead; display remaining health message
                    print('You have {} HP left.'.format(character_stats[7]))
            else: #enemy's attack blocked; displays attack blocked message
                print('You block the attack!')
        else: #enemy dead; display victory message
            print('The {} is dead! You are victorious!'.format(enemy))
            if enemy == 'Rat King': #dead enemy is king; display winning message; change king state to dead: 'k'; output end game trigger
                print('Congratulations, you have defeated the Rat King!\nThe world is saved! You win!')
                enemy_state[get_char_pos('H')[0]][get_char_pos('H')[1]] = 'k'
                return 'win'
            else: #for dead non king enemies; change enemy state to dead:0
                enemy_state[get_char_pos('H')[0]][get_char_pos('H')[1]] = '0'

        return health #outputs enemy's new health

#prints the direction of the orb or power
def sense_orb(orb_of_power):
    character_position = get_char_pos('H') #gets character coordinates
    orb_position = get_char_pos('O') #gets orb coordinates
    if  bool(int(orb_of_power)): #already holding orb; display holding orb message
        print('You are holding the Orb of Power.\nEnergy wasted sensing the Orb of Power.')
    else: #not currently holding orb
        #picks up orb if orb and character coordinates same
        if character_position == orb_position:
            print('You found the orb of Power!') #displays orb found message
            print('Your attack increases by 5!')
            print('Your defence increases by 5!')
            character_stats[3][0] += 5 #increases damage range and defence by 5
            character_stats[3][1] += 5
            character_stats[5] += 5
            orb_of_power = 1 #change orb state to 1:True,holding orb

        else: #not in the same location; display orb direction form character
            print('You sense that the Orb of Power is to the ', end = '')

            if orb_position[0] < character_position[0]: #adds north to the display message if orb row is above character row
                print('north', end = '')
            if orb_position[0] > character_position[0]: #adds sount to the display message if orb row is below character row
                print('south', end = '')

            if orb_position[1] < character_position[1]: #adds west to the display message if orb column is to the right of character column
                print('west', end = '')
            if orb_position[1] > character_position[1]: #adds east to the display message if orb column is to the left of character column
                print('east', end = '')
            print('.')
    return orb_of_power

#updates the highscore list in the records file
def add_highscore(score, save_name):
    try:
        file = open('records_save_file.txt','r')
        lines = file.readlines() #gets current highscores from the records file
        highscores = lines[1].strip('\n')[12:-1].split(', ') #makes the current highscores into a list
        file.close()

        for index in range(len(highscores)): #converts the list of string highscores to a list of integers
            highscores[index] = int(highscores[index])

        if 0 in highscores: #if list contains 0s:blank highscores
            highscores = highscores[:highscores.index(0)] #removes all elements after the first instance of 0: all elements after 0 should always be 0s

        highscores.append(score) #adds new score to the list
        highscores.sort() #sorts the new list smallest to largest; puts the new score in the right position
        highscores.extend([0, 0, 0, 0, 0]) #adds 0s to the back to the list: for when there are less than 5 highscores; could be [0, 0, 0, 0] but eh redundancies right

        highscores = highscores[:5] #moves anything after the 5th element in the list

        file = open('records_save_file.txt','w')
        file.write(lines[0]) #writes save count(unchanged) back into the record file
        file.write('highscores:' + str(highscores)) #writes new highscores into the records file
        file.close()

    except FileNotFoundError: #in the unlikely occasion that the record file gets deleted mid game
        print('Error! Records save file removed.\nReinitialising records save file and updating highscores.')
        saves = save_name[10:-4] #gets save file number from the save file currently running
        file = open('records_save_file.txt','w')
        file.write('saves:{}\nhighscores:[0, 0, 0, 0, 0]'.format(saves)) #rewrites record file with the curent save file number and blank highscores
        file.close()
        add_highscore(score, save_name) #reruns the function to add the current highscore

#generates new map with towns and the orb of power
def gen_new_map():
    #initialises a blank map
    blank_world_map = [['H/T', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
                       [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'K']]

    #towns
    town_list = [[0, 0]] # initialise list of town coordinate lists with
    for i in range(4): #iterates 4 times for the 4 new towns
        row_index = randint(0,7) #generates random coordinates for a new town
        col_index = randint(0,7)
        near_town = False #initialise a flag
        for town_coordinates in town_list: #cycles through town coordinates list
            distance = abs(town_coordinates[0] - row_index) + abs(town_coordinates[1] - col_index) #calculates dist: number of steps
            if distance <= 2:
                near_town = True #raise flag when too close to another town

        #repeats if the the flag is raised or the coordinates is not on a blank i.e. on the king
        while blank_world_map[row_index][col_index] != ' ' or near_town == True:
            row_index = randint(0,7) #generates random coordinates for a new town
            col_index = randint(0,7)
            near_town = False
            for town_coordinates in town_list:
                distance = abs(town_coordinates[0] - row_index) + abs(town_coordinates[1] - col_index)
                if distance <= 2:
                    near_town = True

        blank_world_map[row_index][col_index] = 'T' #changes spot on world map to a town
        town_list.append([row_index, col_index]) #adds coordinates to the list of town coordinates


    #orb of power
    row_index = randint(0,7) #generates random coordinates of the orb
    col_index = randint(0,7)
    #keeps regenerating coordinates until they are in the 4 rightmost columns or bottommost rows and it is an empty spot
    while (row_index in [0, 1, 2, 3] and col_index in [0, 1, 2, 3]) or blank_world_map[row_index][col_index] != ' ':
        row_index = randint(0,7)
        col_index = randint(0,7)

    blank_world_map[row_index][col_index] = 'O' #inserts the orb into the map

    return blank_world_map #returns complete map with new towns and the orb

#generates a enemy state map based on the new generated town map
def gen_enemy(world_map):
    for row_index in range(len(world_map)): #cycles through every spot in the map
        for col_index in range(len(world_map[row_index])):
            if world_map[row_index][col_index] in [' ', 'O']: #and checks for blanks and the orb; spots that are not towns and not the king
                world_map[row_index][col_index] = str(randint(1, 2)) #makes those spots a '1' or a '2'; 1 is Rat and 2 is a Mutant Rat
    return world_map #returns the enemy state map





#initialising text file to keep track of highscores and number of save files
try: #checks if there is an existing record file
    file = open('records_save_file.txt','r')
    file.close()
except: #creates a new record file otherwise
    file = open('records_save_file.txt','w')
    file.write('saves:0\nhighscores:[0, 0, 0, 0, 0]')
    file.close()


# Code your main program here
while True: #main menu
    print("Welcome to Ratventure!") #displays welcome message
    print("----------------------") #yeah this line thing too

    main_choice = menu_choice(main_text) #display and get choice for main manu

    if main_choice == '1': #new game
        save_name = new_game_save_file_name() #makes new save file and assigns the save file name to the variable save_name
        file = open(save_name,'r')
        lines = file.readlines() #obtains all save file data as a list of lines into the variable lines

        #character stats
        character_stats = lines[:10] #extracts character stats from save file as a list character_stats
        for i in range(len(character_stats)): #removes next line character from every item
            character_stats[i] = character_stats[i].strip('\n')

        character_stats[3] = character_stats[3][1:-1].split(', ') #damage to a list
        character_stats[3][0], character_stats[3][1] = int(character_stats[3][0]), int(character_stats[3][1]) #type forcing the string elements of the damage to integers

        for stat_index in range(5,10,2): #force typing numeric stats form strings in the save file to integers
            character_stats[stat_index] = int(character_stats[stat_index])

        #world map
        world_map = lines[10:18] #extracts world map from save file as a list world_map
        for i in range(len(world_map)): #removes next line character from every item
            world_map[i] = world_map[i].strip('\n')[2:-2].split("', '") #changes the string into a list removing the '[ and ]' from the start and end

        #enemy state map
        enemy_state = lines[18:26] #extracts enemy state from save file as a list enemy_state
        for i in range(len(enemy_state)): #removes next line character from every item
            enemy_state[i] = enemy_state[i].strip('\n')[2:-2].split("', '") #changes the string into a list removing the '[ and ]' from the start and end

        #orb of power
        orb_of_power = lines[27].strip('\n')
        file.close()


    elif main_choice == '2': #resume game
        try:#in the odd case that the record file gets deleted midway through the game
            file = open('records_save_file.txt','r')
            recent_save_count = int(file.readline()[6:-1]) #obtains most recent save file number
            file.close()
        except FileNotFoundError: #in the odd case that the record file gets deleted midway through the game, creates a new record file
            print('Error! Records save file removed.\nReinitialising records save file and restarting game.\n') #displays error message
            file = open('records_save_file.txt','w')
            file.write('saves:0\nhighscores:[0, 0, 0, 0, 0]') #reinitialises records file start data
            file.close()
            continue #goes to main menu

        #does not allow game resumtion if there are no save files
        if recent_save_count == 0:
            print('Error! No save files found.\nPlease start a new game.\n') #displays error message
            continue #goes to main menu

        save_file_choice = input('Enter save file number or press enter to resume most recent game: ')
        #validates save_file_choice, check if its not null string and not a save file number within the range to promt for a re-entry
        while (save_file_choice != '' and not save_file_choice.isdigit()) or (save_file_choice.isdigit() and (int(save_file_choice)<1 or int(save_file_choice)>recent_save_count)):
            print('Invalid save file number.\nFiles 1-{} available.'.format(recent_save_count)) #displays error message and valid file number range
            save_file_choice = input('Enter save file number or press enter to resume most recent game: ')

        if save_file_choice == '': #changes null string to most recent save file number
            save_file_choice = recent_save_count
        print('Loading save file',save_file_choice,'\n')
        #extracting game data from save file
        save_name = 'save_file_' + str(save_file_choice) + '.txt'
        try:
            file = open(save_name,'r')
            lines = file.readlines()
            #obtains all save file data
            character_stats = lines[:10] #extracts character stats from save file as a list character_stats
            for i in range(len(character_stats)): #removes next line character from every item
                character_stats[i] = character_stats[i].strip('\n')

            character_stats[3] = character_stats[3][1:-1].split(', ')
            character_stats[3][0], character_stats[3][1] = int(character_stats[3][0]), int(character_stats[3][1])

            for stat_index in range(5,10,2): #force typing numeric stats form strings in the save file to integers
                character_stats[stat_index] = int(character_stats[stat_index])

            world_map = lines[10:18] #extracts world map from save file as a list world_map
            for i in range(len(world_map)): #removes next line character from every item
                world_map[i] = world_map[i].strip('\n')[2:-2].split("', '") #changes the string into a list removing the '[ and ]' from the start and end

            enemy_state = lines[18:26] #extracts enemy state from save file as a list enemy_state
            for i in range(len(enemy_state)): #removes next line character from every item
                enemy_state[i] = enemy_state[i].strip('\n')[2:-2].split("', '") #changes the string into a list removing the '[ and ]' from the start and end

            orb_of_power = lines[27].strip('\n')
            file.close()


            if enemy_state[-1][-1] == 'k': #dead rat king and resuming; displays meassage rat king is already dead
                print('Day {}: The Rat King is dead! You are victorious!\nStart a new game or resume another game.\n'.format(character_stats[9]))
                continue #goes to main menu

        except FileNotFoundError: #selected save file has been deleted and cannot be opened; displays error message and goes to main menu to resume a different game
            print('Error! Save file ' + str(save_file_choice) + ' removed.\nPlease start a new game or try a different save file.\n')
            continue #goes to mian menu

    elif main_choice == '3': #view leaderboard
        file = open('records_save_file.txt','r')
        highscores = file.readlines()[1].strip('\n')[12:-1].split(', ') #gets leaderboard list from record file and coverts to a list
        file.close()

        print('Ratventure Leaderboard')  #display leaderboard title
        print('{:<6}{}'.format('Rank:', 'Days:')) #display leaderboard header
        for i in range(len(highscores)):
            if highscores[i] == '0': #displays a '-' for blank leaderboard positions
                score = '-'
            else:
                score = highscores[i]
            print('{:>4}: {}'.format('#' + str(i + 1), score)) #displays position number and score
        print()
        continue #goes back to main menu

    else: #option 4 exit game
        break #exits entire program


    ##################################################
    ##################################################


    #for the different day states: town , outdoor and rat king
    while True:
        #display day count and location text
        print('Day {}: {}'.format(character_stats[9],day_location(world_map)))

        if day_location(world_map) == 'You are in a town.':
            #display town menu and get choice
            town_choice = menu_choice(town_text)

            if town_choice == '1': #view character
                view_character()

            elif town_choice == '2': #view map
                view_map()

            elif town_choice == '3': #move
                move()
                character_stats[9] += 1 #increases day count

            elif town_choice == '4': #rest
                character_stats[7] = 20 #resets character health to full
                character_stats[9] += 1 #increases day count
                print('You are fully healed.\n')

            elif town_choice == '5': #save game
                save_game(save_name)
                print('Game saved.\nSave file number: {}\n'.format(save_name[10:-4])) #displays save file number for future resumtion of the game *additional feature

            else: #option 6 exit game
                break #goes to main menu


        elif day_location(world_map) == 'You are out in the open.':
            rat_health = 10 #initialise base rat health
            #repeats combat until enemy is dead i.e. change in enemy state in enemy state map; or a speacial message is returned-'move', 'break'
            while enemy_state[get_char_pos('H')[0]][get_char_pos('H')[1]] == '1' and str(rat_health).isdigit(): #rat
                rat_health = combat('Rat', rat_health)

            mutant_rat_health = 18 #same as above but for mutant rat
            while enemy_state[get_char_pos('H')[0]][get_char_pos('H')[1]] == '2' and str(mutant_rat_health).isdigit(): #mutant rat
                mutant_rat_health = combat('Mutant Rat', mutant_rat_health)

            if rat_health == 'break' or mutant_rat_health == 'break': #in combat 'exit' choice
                break #goes to main menu
            if rat_health == 'move' or mutant_rat_health == 'move': #in combat 'move' choice
                move()
                character_stats[9] += 1 #increases day count
                continue #goes to next day

            open_choice = menu_choice(open_text)
            if open_choice == '1': #view character
                view_character()

            elif open_choice == '2': #view map
                view_map()

            elif open_choice == '3': #move
                move()
                character_stats[9] += 1 #increases day count

            elif open_choice == '4': #sense orb
                orb_of_power = sense_orb(orb_of_power) #changes orb state and Performs sense orb actions
                character_stats[9] += 1 #increases day count

            else: #option 5 exit game
                break #goes to main menu


        elif day_location(world_map) == 'You see the Rat King!':
            rat_king_health = 25 #same as rat and mutant rat combat in outdoor
            while enemy_state[get_char_pos('H')[0]][get_char_pos('H')[1]] == 'K' and str(rat_king_health).isdigit(): #rat king
                rat_king_health = combat('Rat King', rat_king_health)
            if rat_king_health == 'break':
                break #goes to main menu
            if rat_king_health == 'move':
                move()
                character_stats[9] += 1 #increases day count
                continue #goes to next day
            if rat_king_health == 'win': #when rat king is dead
                add_highscore(character_stats[9],save_name) #updates records file with new highscore
                save_game(save_name)
                sys.exit() #exits entire game program
