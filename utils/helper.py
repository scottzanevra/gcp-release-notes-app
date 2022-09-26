

def get_keys_from_dict(some_dict):
    return list(some_dict.keys())


def left_join_lists(primary_list, second_list):
    result = []
    for x in primary_list:
        if x in second_list:
            result.append(x)
    return result


if __name__ == '__main__':
    primary_list = [1,2,3,4]
    second_list = [1,2,5,6,7]
    data = left_join_lists(primary_list, second_list)
    foo = "me"
