

def get_house_text():

    file_path = "features_for_quiz/houses/houses.txt"

    result_dict = {}
    current_key = ""
    current_value = ""

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line == "":
                # Empty line, start a new key
                if current_key:
                    result_dict[current_key] = current_value
                    current_key = ""
                    current_value = ""
            elif "|" in line:
                # Line with a key
                key, value = map(str.strip, line.split("|", 1))
                current_key = key
                current_value = value
            else:
                # Lines with additional details
                current_value += " " + line

    # Add the last entry
    if current_key:
        result_dict[current_key] = current_value

    return result_dict
