import sys


def find_common_letters(box_ids):
    """Returns the common letters from the correct box ids.
    Two boxes form the correct combination, if the ids differ by exactly a single character. 
    
    Arguments:
        box_ids {list} -- Sequence of box ids
    
    Returns:
        [String]
    """
    common_letters = None

    for id1 in box_ids:
        for id2 in box_ids:
            # Enforcing the box ids are of same length.
            if (id1 != id2) and (len(id1) == len(id2)):
                common_letters = _get_common_letters(id1, id2)
                if (len(id1) - len(common_letters)) == 1:
                    print(f"Id1: {id1}, Id2: {id2}")
                    break
                else:
                    common_letters = None

        if common_letters:
            break

    return common_letters


def _get_common_letters(box_id1, box_id2):
    """Returns common letters in the box ids
  
    Arguments:
        box_id1 {String}
        box_id2 {String}

    Returns:
        [String]
    """
    # I can iterate through both the string and find out the diff in one iteration only.
    # below logic is still O(n), through n elements are traversed twice (zip and list comprehension)
    # remember len function is O(1)
    common_letters = [e[0] for e in zip(box_id1, box_id2) if (e[0] == e[1])]
    return "".join(common_letters)


def main(args):
    """
        This is the entry point.
    """
    box_ids = [id.strip() for id in sys.stdin]
    print(f"Checksum: {find_common_letters(box_ids)}")


if __name__ == "__main__":
    main(sys.argv)
