def get_names() -> list:
    names = input('Please enter names: \
        [name1, name2, name3]\n... ')

    # turns it into a list of names
    return names.split(', ')


def game_loop() -> None:
    ...
