import random
import timeit


def counting_sort(digit_list, b, index, digit_len):
    """
    This function plots the frequency of each value of the list digit_list into a count array, then
    it marks the positions these numbers will appear in the sorted array and finally plots
    those values into the correct positions in the resulting array.

    Time complexity: O(N+K) where N is the size of digit_list and K is digit_len (the length of the largest
    number in digit_list)
    :param digit_list: the array which will be sorted in sorted_list
    :param b: the base the numbers in digit_list are in
    :param index: which digit of each number in digit_list will be sorted through this call of counting_sort
    :param digit_len: the number of elements in the list digit_list
    :return sorted_list: a list that is sorted relative to the digits of digit_list used in this call
    """
    try:
        # Creates arrays to store count tally and positions on where to insert
        count = [0] * b
        position = [0] * b
    except MemoryError:
        raise MemoryError("The base is too large, memory cannot handle array creation")

    sorted_list = [None] * digit_len

    # Tallies each digit into count
    for i in range(digit_len):
        value = digit_list[i] // (b**index)
        value = value % b
        count[value] += 1

    position[0] = 0

    # Calculates the position to insert each digit in
    for i in range(1, b):
        position[i] = position[i-1] + count[i-1]

    # Inserts each number into a new list using the positions
    for i in range(digit_len):
        value = digit_list[i] // (b**index)
        value = value % b
        sorted_list[position[value]] = digit_list[i]
        position[value] += 1

    return sorted_list


def radix_sort(num_list, b):
    """
    This function uses radix sort to sort num_list in ascending order. It iteratively calls
    counting_sort(result_list, b, digit_inc, digit_len) to sort each digit from left to right, as the digit
    to the most left has the highest influence on the order of the number. The sorted list is stored and returned
    in result_list.

    Time complexity: O(KN) where N is the size of num_list and K is the length of the highest number in
    num_list

    :param num_list: a list of integers to be sorted
    :param b: the base of the integers in num_list
    :return result_list: a sorted list of num_list, sorted in ascending order
    """

    result_list = num_list
    digit_len = len(num_list)
    try:
        max_num = max(num_list)

    except TypeError:
        print("List must only contain integers")
        return
    except ValueError:
        print("invalid value")
        return

    digit_num = 0

    # Calculates the highest digit number
    while max_num > 0:
        digit_num += 1
        max_num //= b

    digit_inc = 0

    # Count sorts each digit within each number of num_list amongst each other
    while digit_inc < digit_num:
        result_list = counting_sort(result_list, b, digit_inc, digit_len)
        digit_inc += 1

    return result_list


def time_radix_sort():
    """
    This function generates a random list 'test_data' of 100,000 integers, then uses the radix sort function
    to sort the list with various bases. The function times how long it takes (in seconds) until the radix sort
    function has completely sorted the list 'test_data' and stores the base and time respectively for each base
    used to sort the list.

    Time complexity: Assuming base_list remains a fixed size - O(KN) where N is the size of num_list and
    K is the length of the highest number in num_list

    :return result: a list of tuples with the base and time in seconds it took to sort the list with that base
    respectively
    """
    #base_list = [2, 5, 17, 88, 201, 500, 9999, 33823, 349384]
    # base_list = [5, 10, 15, 20, 25, 30, 35, 40, 45]

    base_list = [5, 17, 88, 201, 500, 9999, 33823, 349384, 700000, 1000000, 2000000]
    result = [0] * len(base_list)

    for index, base in enumerate(base_list):
        # Generates 100,000 elements from 1-2^64
        test_data = [random.randint(1, (2 ** 64) - 1) for _ in range(100000)]

        # Times radix sort calculation with the generated list
        startTimer = timeit.default_timer()
        radix_sort(test_data, base)
        endTimer = timeit.default_timer() - startTimer

        # For visual help
        print("Base ", base, ":", endTimer, "s")
        result[index] = base, endTimer
    return result


def find_max_len(string_list):
    """
    Finds the maximum string length in a list of strings string_list, stores the length of the maximum string
    in max

    Time complexity: O(NM) where N is the length of string_list and M is the length of the largest string in
    string_list
    :param num_list: a list of strings to check the largest string in the list
    :return max: the maximum string length in the list string_list
    """
    max = 0
    for stringval in string_list:
        if len(stringval) > max:
            max = len(stringval)

    return max


def string_counting_sort(string_list, index, stringlist_len):
    """
    This function plots the frequency of each letter of the list string_list into a count array by finding
    the values of the letters on the ascii table then subtracting it by 96 to give a relative digit for each
    letter. It then plots the frequency of these letters using their resulting digit and then it marks the
    positions the numbers will appear in the sorted array and finally plots those values into the correct
    positions in the resulting array.

    Time complexity: O(N+K) where N is the size of digit_list and K is digit_len (the length of the largest
    number in digit_list)
    :param string_list: a list of strings to be sorted
    :param index: which letter each string of string_list will be sorted
    :param stringlist_len: the number of strings in stringlist_len
    :return sorted_list: a list that is sorted relative to the digits of string_list used in this call
    """
    try:
        count = [0] * 27    # Set to 27 as this function assumes string (and includes no value as 0)
        position = [0] * 27
    except MemoryError:
        raise MemoryError("The base is too large, memory cannot handle array creation")

    sorted_list = [None] * stringlist_len

    for i in range(stringlist_len):
        if len(string_list[i]) > index:
            value = ord(string_list[i][-(index+1)])-96  # Using ASCII table to give each char a value
            count[value] += 1
        else:
            count[0] += 1

    position[0] = 0

    for i in range(1, 27):
        position[i] = position[i-1] + count[i-1]

    for i in range(stringlist_len):
        if len(string_list[i]) > index:
            value = ord(string_list[i][-(index+1)])-96
            sorted_list[position[value]] = string_list[i]
            position[value] += 1
        else:
            sorted_list[position[0]] = string_list[i]
            position[0] += 1

    return sorted_list


def radix_sort_string(string_list):
    """
    This function uses radix sort to sort string_list in ascending order. It iteratively calls
    string_counting_sort(result_list, string_inc, stringlist_len) to sort each digit from left to right, as the digit
    to the most left has the highest influence on the order of the number. The sorted list is stored and returned
    in result_list.

    Time complexity: O(KN) where N is the size of string_list, K is the length of the largest string in
    string_list
    :param string_list: a list of strings to be sorted
    :return result_list: a sorted list of string_list
    """
    result_list = string_list
    stringlist_len = len(string_list)
    try:
        letters = find_max_len(string_list)

    except TypeError:
        print("List must only contain strings")
        return
    except ValueError:
        print("invalid value")
        return

    string_inc = 0

    while string_inc < letters:
        result_list = string_counting_sort(result_list, string_inc, stringlist_len)
        string_inc += 1

    return result_list


def rotate_list(string_list, p):
    """
    This function rotates all strings by p to the left in the list string_list

    :Time complexity: O(NM) where N is the size of string_list and M is the max string size in string_list
    :param p: how many characters to the left each string in string_list will be rotated
    :return rotated_list: a list containing each string with a rotation of p from the original list string_list
    """
    rotated_list = [None] * len(string_list)
    resultstring = ""

    for list_element in range(len(string_list)):
        p_remainder = p % (len(string_list[list_element]))
        result = [None] * p_remainder

        for p_inc in range(p_remainder):

            result[p_inc] = string_list[list_element][p_inc]

        for first_values in range(p_remainder, len(string_list[list_element])):
            resultstring += string_list[list_element][first_values]

        for p_inc in range(p_remainder):
            resultstring += result[p_inc]

        rotated_list[list_element] = resultstring
        resultstring = ""

    return rotated_list

def intersect_array(rotated_list, original_list):

    """
    This function increments through rotated_list and original_list. Because both lists are in ascending order,
    we can check if rotated_list contains an element from original_list by traversing through the rotated_list until
    there is an element greater than the value it is trying to find in original_list, if the value is not found
    then we can assume it doesn't exist in rotated_list. Knowing this, we can increment through each element of
    original_list in ascending order, and every time we find an element in rotated_list that's greater than the
    current element in the original_list, we can increment the original_list until we find a unique value in
    original_list, while continuing the rotated_list incrementation upon each iteration. When we find a matching
    value, it is appended onto final_array and both rotated_list and original_list are incremented.

    :Time complexity: O(NM) where N is the size of original_list and M is the size of the largest string in
    original_list
    :param rotated_list: a list containing strings which have been rotated by p from original_lists elements
    :param original_list: a list of the original strings which we will compare to rotated_list
    :return final_array: contains the value of elements which appear both in original_list and rotated_list
    """
    final_list = []
    rotate_index = 0
    original_index = 0
    n = len(rotated_list)
    while original_index < n and rotate_index < n:

        # Checks bounds and duplicates
        while (rotate_index < n - 1) and rotated_list[rotate_index] == rotated_list[rotate_index + 1]:
            rotate_index += 1

        while(original_index < n - 1) and original_list[original_index] == original_list[original_index + 1]:
            original_index += 1

        # Assuming both lists sorted, can iterate through each simultaneously
        if original_list[original_index] > rotated_list[rotate_index]:
            rotate_index += 1

        elif original_list[original_index] < rotated_list[rotate_index]:
            original_index += 1

        # Found a match
        else:

            final_list.append(original_list[original_index])
            original_index += 1
            rotate_index += 1

    return final_list


def find_rotations(string_list, p):
    """
    Creates a list of strings which are rotated by p amount from string_list, then compares the strings in
    string_list to the rotated_list and returns all the elements which appear in both string_list and rotated_list

    :Time complexity: O(NM) where N is the length of string_list and M is the largest element in string_list
    :param string_list: a list of the original strings to be rotated
    :param p: will rotate string_list by its value and store the rotated strings in rotated_list
    :return rotate_list(result_list, -p) contains a list of sorted elements in rotated_list which also
    appear in string_list
    """
    rotated_list = rotate_list(string_list, p)                     # O(NM)  /
    sorted_rotation = radix_sort_string(rotated_list)              # O(NM)  /
    sorted_list = radix_sort_string(string_list)                   # O(NM)  /

    result_list = intersect_array(sorted_rotation, sorted_list)    # O(NM)  /
    return rotate_list(result_list, -p)                            # O(NM)  /

time_radix_sort()