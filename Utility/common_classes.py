class Common:
    def remove_until_first_space(input_string):
        # Find the index of the first space in the input string
        first_space_index = input_string.find(' ')

        # If no space is found, return the original string
        if first_space_index == -1:
            return input_string

        # Remove characters up to (including) the first space
        result_string = input_string[first_space_index + 1:]

        return result_string

class MyCustomException(Exception):
    pass