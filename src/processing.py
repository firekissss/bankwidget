def filter_by_state(dictionary_input_list: list, state:str = 'EXECUTED') -> list:
    output_dictionary_list: list = []
    for item in dictionary_input_list:
        if item['state'] == state:
            output_dictionary_list.append(item)
    return output_dictionary_list
