
def longest_walk_aux(x, y, x_len, y_len, M, output_M):
    """
    Recursively checks the surrounding cells to see their current max walking distance, will find the
    max walking distance of the cells surrounding it which have a lower int in the original grid. Adds the
    max by 1 and uses that in the current cells max walking distance.
    :Time complexity (worst case): O(NK) - where N is the length of the x axis of M and K is the length
    of the y axis of M
    :Auxiliary space (worst case): O(NK) - where N is the length of the x axis of M and K is the length
    of the y axis of M, as we are using a shallow copy
    :param x: current cells x coordinate
    :param y: current cells y coordinate
    :param x_len: The length of the x coordinate of the input 2D list
    :param y_len: The length of the y coordinate of the input 2D list
    :param M: The input 2D array containing integers
    :param output_M: A 2D array of the max walking distances for each cell
    :return output_M: the new updated list of max walking distances of each cell
    """
    if x < 0 or x >= x_len or y < 0 or y >= y_len or output_M[y][x] != -1:
        return output_M

    # vertical
    up, down = 0, 0

    # horizontal
    left, right = 0, 0

    # diagonal
    upright, upleft, downright, downleft = 0, 0, 0, 0

    # checking right tile
    if x < x_len-1 and M[y][x] < M[y][x+1]:
        right = 1 + longest_walk_aux(x + 1, y, x_len, y_len, M, output_M)[y][x+1]

    # checking top right tile
    if x < x_len-1 and y > 0 and M[y][x] < M[y-1][x+1]:
        upright = 1 + longest_walk_aux(x + 1, y - 1, x_len, y_len, M, output_M)[y-1][x+1]

    # checking bottom right tile
    if x < x_len-1 and y < y_len-1 and M[y][x] < M[y+1][x+1]:
        downright = 1 + longest_walk_aux(x+1, y+1, x_len, y_len, M, output_M)[y+1][x+1]

    # checking left tile
    if x > 0 and M[y][x] < M[y][x-1]:
        left = 1 + longest_walk_aux(x - 1, y, x_len, y_len, M, output_M)[y][x-1]

    # checking top left tile
    if x > 0 and y > 0 and M[y][x] < M[y-1][x-1]:
        upleft = 1 + longest_walk_aux(x-1, y-1, x_len, y_len, M, output_M)[y-1][x-1]

    # checking bottom left tile
    if x > 0 and y < y_len-1 and M[y][x] < M[y+1][x-1]:
        downleft = 1 + longest_walk_aux(x-1, y+1, x_len, y_len, M, output_M)[y+1][x-1]

    # checking bottom tile
    if y < y_len-1 and M[y][x] < M[y+1][x]:
        down = 1 + longest_walk_aux(x, y+1, x_len, y_len, M, output_M)[y+1][x]

    # checking top tile
    if y > 0 and M[y][x] < M[y-1][x]:
        up = 1 + longest_walk_aux(x, y-1, x_len, y_len, M, output_M)[y-1][x]

    output_M[y][x] = max(right, left, down, up, upright, downright, upleft, downleft)
    return output_M


def longest_walk_coord_aux(M, max_path, x, y, x_len, y_len):
    """
    Recursively checks for the longest walk given an input M containing a 2D list of max walks of all
    cells in the original input array of longest_walk(M).
    :Time complexity (worst case): O(NK) where N is the length of the x axis of M and K is the length
    of the y axis of M
    :Auxiliary space (worst case): O(NK) where N is the length of the x axis of M and K is the length
    of the y axis of M
    :param M: a 2D array containing the max walk of all cells
    :param max_path: a list containing the coordinates of the cells which make the longest walk
    :param x: The x coordinate of the cell with the longest walk value
    :param y: The y coordinate of the cell with the longest walk value
    :param x_len: The length of the x axis in the 2D list M
    :param y_len: The length of the y axis in the 2D list M
    :return max_path: a list containing the coordinates of the cells which make the longest walk
    """
    max_path.append((y, x))

    # reached end of walk, end tail recursion
    if M[y][x] == 0:
        return max_path

    # right
    elif x < x_len-1 and M[y][x] == M[y][x+1]+1:
        max_path = longest_walk_coord_aux(M, max_path, x+1, y, x_len, y_len)

    # top right
    elif x < x_len-1 and y > 0 and M[y][x] == M[y-1][x+1]+1:
        max_path = longest_walk_coord_aux(M, max_path, x + 1, y - 1, x_len, y_len)

    # bottom right
    elif x < x_len-1 and y < y_len-1 and M[y][x] == M[y+1][x+1]+1:
        max_path = longest_walk_coord_aux(M, max_path, x + 1, y + 1, x_len, y_len)

    # left
    elif x > 0 and M[y][x] == M[y][x-1]+1:
        max_path = longest_walk_coord_aux(M, max_path, x - 1, y, x_len, y_len)

    # top left
    elif x > 0 and y > 0 and M[y][x] == M[y-1][x-1]+1:
        max_path = longest_walk_coord_aux(M, max_path, x - 1, y - 1, x_len, y_len)

    # bottom left
    elif x > 0 and y < y_len - 1 and M[y][x] == M[y+1][x-1]+1:
        max_path = longest_walk_coord_aux(M, max_path, x - 1, y + 1, x_len, y_len)

    # bottom
    elif y < y_len-1 and M[y][x] == M[y+1][x]+1:
        max_path = longest_walk_coord_aux(M, max_path, x, y + 1, x_len, y_len)

    # top
    elif y > 0 and M[y][x] == M[y-1][x]+1:
        max_path = longest_walk_coord_aux(M, max_path, x, y - 1, x_len, y_len)

    return max_path


def longest_walk(M):
    """
    Calculates the longest walking distance of a 2D list of integers M, where a walk consists of an increasing
    sequence of numbers. This function will generate a list of those coordinates and the length of the walk.
    :Time complexity (worst case): O(NK) where N is the length of the x axis of M and K is the length of
    the y axis of M
    :Auxiliary space (worst case): O(NK) where N is the length of the x axis of M and K is the length of
    the y axis of M
    :param M: A 2D array of integers
    :return: a tuple containing the length of the max walk distance and the coordinates that the max
    walk distance consists of.
    """

    # saves time as it doesn't have to keep recalculating this
    x_len = len(M[0])
    y_len = len(M)

    # 2D list that will contain max walking distances
    output_M = [[-1] * x_len for i in range (y_len)]

    # calculate max walking distance of all cells
    for y in range(y_len):
        for x in range(x_len):
            output_M = longest_walk_aux(x, y, x_len, y_len, M, output_M)

    max = -1
    max_coord = [0, 0]

    # finds cell with maximum walk value
    for y in range(y_len):
        for x in range(x_len):
            if output_M[y][x] > max:
                max = output_M[y][x]
                max_coord = [x, y]

    # traverses through that walk to get the coordinates
    max_path = longest_walk_coord_aux(output_M, [], max_coord[0], max_coord[1], x_len, y_len)

    return max + 1, max_path

