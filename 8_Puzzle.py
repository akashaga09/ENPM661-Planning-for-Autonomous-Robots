import numpy as np
import pandas as pd

# take input from user and convert to list
def convert_list(text):
    state_list = list(map(int, text.split(' ')))
    return state_list

# convert list and store information in a matrix
def make_matrix(state):
    node_state = np.array([[state[0], state[3], state[6]],
                          [state[1], state[4], state[7]],
                          [state[2], state[5], state[8]]])
    
    return node_state

# convert state from matrix to list form
def matrix_to_list(matrix):
    change_matrix = matrix.ravel(order = "F")
    change_matrix = change_matrix.tolist()
    return change_matrix

# find the location of the blank tile
def blank_tile_location(current_node):
    for i in range(len(current_node)):
        for j in range(len(current_node[0])):
            if current_node[i][j] == 0:
                return [i,j]
            
# moves blank tile left, if possible
def action_move_left(current_node):
    [i,j] = blank_tile_location(current_node)
    if j > 0:
        temp = current_node[i,j-1]
        current_node[i,j-1] = 0
        current_node[i,j] = temp
        new_node = current_node
        return new_node
    else:
        return current_node


# moves blank tile right, if possible
def action_move_right(current_node):
    [i,j] = blank_tile_location(current_node)
    if j < 2:
        temp = current_node[i,j+1]
        current_node[i,j+1] = 0
        current_node[i,j] = temp
        new_node = current_node
        return new_node
    else:
        return current_node
    

# moves blank tile up, if possible
def action_move_up(current_node):
    [i,j] = blank_tile_location(current_node)
    if i > 0:
        temp = current_node[i-1,j]
        current_node[i-1,j] = 0
        current_node[i,j] = temp
        new_node = current_node
        return new_node
    else:
        return current_node


# moves blank tile down, if possible
def action_move_down(current_node):
    [i,j] = blank_tile_location(current_node)
    if i < 2:
        temp = current_node[i+1,j]
        current_node[i+1,j] = 0
        current_node[i,j] = temp
        new_node = current_node
        return new_node
    else:
        return current_node

# check if given node state is solvable
def check_solve(nodes):
    test = nodes.ravel()
    test = test.tolist()
    count = 0
    for i in range(0,8):
        for j in range(i+1,9):
            if test[j] and test[i] and test[i] > test[j]:
                count += 1
                
    if count%2 == 0:
        return 1
    else:
        return 0
    
# backtracking to find path between initial and goal nodes
def generate_path(index):
    path = []
    path.append(index[-1][0])
    parent = index[-1][1]
    for i in range(0,len(index)):
        for j in range(0,len(index)):
            if parent == index[j][0]:
                path.append(index[j][0])
                parent = index[j][1]
    return path
    
    
# taking input from user
input_text_string = input("Enter initial state (column wise):- ")
input_state = convert_list(input_text_string)

initial_node = make_matrix(input_state)
initial_node_state = input_state
goal_node_state = [1,4,7,2,5,8,3,6,0]

# initializing variables
node_index = 2
parent_node_index = 1
node_address = []
node_address.append([1,0])
node_set = []
node_set.append(initial_node)
node_state_set = []
node_state_set.append(initial_node_state)
store_node = np.empty([3,3])

if check_solve(initial_node) == 0:
    print("The puzzle is not solvable!!!")
else:
    while True:
        
        if initial_node_state == goal_node_state:
            print("Initial and Goal nodes are same!")
            break
        
        else:
            store_node = np.array(node_set[parent_node_index-1])
            new_node = action_move_down(store_node)
            new_node_state = matrix_to_list(new_node)
            flag = 0
            if new_node_state in node_state_set:
                flag = 1
            else:
                node_state_set.append(new_node_state)
                node_set.append(new_node)
                node_address.append([node_index, parent_node_index])
                node_index += 1
            
        
        if new_node_state == goal_node_state:
            break
        
        else:
            store_node = np.array(node_set[parent_node_index-1])
            new_node = action_move_left(store_node)
            new_node_state = matrix_to_list(new_node)
            flag = 0
            if new_node_state in node_state_set:
                flag = 1
            else:
                node_state_set.append(new_node_state)
                node_set.append(new_node)
                node_address.append([node_index, parent_node_index])
                node_index += 1
                
        
        if new_node_state == goal_node_state:
            break
        
        else:
            store_node = np.array(node_set[parent_node_index-1])
            new_node = action_move_right(store_node)
            new_node_state = matrix_to_list(new_node)
            flag = 0
            if new_node_state in node_state_set:
                flag = 1
            else:
                node_state_set.append(new_node_state)
                node_set.append(new_node)
                node_address.append([node_index, parent_node_index])
                node_index += 1
            
            
        if new_node_state == goal_node_state:
            break
        
        else:
            store_node = np.array(node_set[parent_node_index-1])
            new_node = action_move_up(store_node)
            new_node_state = matrix_to_list(new_node)
            flag = 0
            if new_node_state in node_state_set:
                flag = 1
            else:
                node_state_set.append(new_node_state)
                node_set.append(new_node)
                node_address.append([node_index, parent_node_index])
                node_index += 1
            
        if new_node_state == goal_node_state:
            break

        parent_node_index += 1
        
    # generating path
    path = generate_path(node_address)
    correct_path = path[::-1]
    
    temp_path = []
    for ele in range(0, len(correct_path)):
        temp_path.append(correct_path[ele]-1)

# writing to files
nodes_info = open("NodesInfo.txt", "w+")
df1 = pd.DataFrame(node_address)
dt1 = df1.to_string(index=False, columns=None)
nodes_info.write(dt1)
nodes_info.close()

nodes_all = open("Nodes.txt", "w+")
df2 = pd.DataFrame(node_state_set)
dt2 = df2.to_string(index=False, columns=None)
nodes_all.write(dt2)
nodes_all.close()

final_answer = []
for x in temp_path:
    final_answer.append(node_state_set[x])
    
nodes_path = open("nodePath.txt", "w+")
df3 = pd.DataFrame(final_answer)
dt3 = df3.to_string(index=False, columns=None)
nodes_path.write(dt3)
nodes_path.close()

print("Solution Found!!!")