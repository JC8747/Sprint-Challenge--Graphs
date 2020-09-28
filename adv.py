from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = set()

def depth_direction():
    #Find available paths, then remove directions that lead back to a previous room
    paths = player.current_room.get_exits()
    new_paths = []
    for path in paths:
        if player.current_room.get_room_in_direction(path) not in visited:
            new_paths.append(path)

    #Keep searching until no new paths
    if len(new_paths) > 0:
        path = random.choice(new_paths)
        return path

    if len(new_paths) == 0:
        return False

def breadth_search():
    #Create queue and enqueue start room as a list
    global visited
    visited_paths = {}
    starting_room = player.current_room
    path_queue = []
    path_queue.append([starting_room])

    #Queue isn't empty, how to check?
    # Get the path, remove from q, set current TO LAST, track on visited_paths, check against list and return
    while len(path_queue) > 0:
        cur_path = path_queue[0]

        path_queue.pop(0)

        cur_room = cur_path[-1]

        visited_paths[cur_room] = cur_path

        if cur_room not in visited:
            cur_path.pop(0)
            backtrack_path = []

        #Track directions to find unknown rooms, must use cardinal
            for i in range(0, len(cur_path)):
                if starting_room.get_room_in_direction('n') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('n')
                elif starting_room.get_room_in_direction('e') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('e')
                elif starting_room.get_room_in_direction('s') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('s')
                elif starting_room.get_room_in_direction('w') == cur_path[i]:
                    starting_room = cur_path[i]
                    backtrack_path.append('w')

            return backtrack_path

        #Add to neighbors q if it HAS been visited, and make sure path is unchecked
        if cur_room in visited:
            for direction in cur_room.get_exits():
                new_path = list(cur_path)
                new_path.append(cur_room.get_room_in_direction(direction))

                if new_path[-1] not in visited_paths:
                    path_queue.append(new_path)

def adv():
    visited.add(player.current_room)

    playing = True
    dft = True
    bft = True
    #Run DFT first in a play loop, then check with BFT
    while playing:

        while dft:
            bft = True
            #Call depth direction to traverse until there is no new paths
            direction = depth_direction()
            if direction == False:
                dft = False
            else:
                traversal_path.append(direction)
                player.travel(direction)
                visited.add(player.current_room)

        while bft:
            #Call breadth search to path to nearest unknown. Once backtrack is done, resume DFT search
            backtrack_path = breadth_search()
            if backtrack_path == None:
                bft = False
                playing = False
            else:
                for direction in backtrack_path:
                    player.travel(direction)
                    visited.add(player.current_room)
                    traversal_path.append(direction)
                bft = False
                dft = True

adv()

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
#player.current_room.print_room_description(player)
#while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
