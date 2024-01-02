import json


def get_names() -> list:
    names = input('Please enter names: \
        [name1, name2, name3]\n... ')

    # turns it into a list of names
    return names.split(', ')


def get_points(nam: list, his: list) -> dict:
    pts = {n: 0 for n in nam}

    # adding points together
    for result in his:
        for n, pt in result.items():
            pts[n] += pt

    return pts


# global variables
names = get_names()
history = []
inform = True
winners = {}
won = False

# main loop
while True:
    round_ = len(history)
    caller = round_ % len(names)
    points = get_points(names, history)

    # checking for winners
    if not won:
        for n, p in points.items():
            if p >= 21:
                won = True
                if p not in list(winners.keys()):
                    winners[p] = []
                winners[p].append(n)

    if won:
        i = max(list(winners.keys()))
        winner = ' and '.join(winners[i])
        print(f'\nWinner is {winner}!\n')

    # info prompt
    if inform and not won:
        print(f'\nRound {round_ + 1}!')
        print(f'Caller is {names[caller]}!\n')
        inform = False

    # taking user input
    cmd = input('... ')
    # skipping empty command
    if cmd == '':
        inform = True
        continue

    # managing round results
    if cmd[-1] in ['1', '2', '3', '6']:
        # a single player gets points
        if cmd[0] == 'w' and not won:
            inform = True
            history.append({
                names[caller]: int(cmd[-1])
            })

        # multiple players get points
        elif cmd[0] == 'l' and not won:
            inform = True
            result = {}
            for i, n in enumerate(names):
                if i != caller:
                    result[n] = int(cmd[-1])
            history.append(result)

    # managing commands
    elif cmd in ['quit', 'q', 'exit']:
        exit()

    elif cmd == 'save':
        save_data = json.dumps({
            'names': names,
            'history': history,
        })
        # writing data to json file
        with open('game.json', 'w') as f:
            f.write(save_data)
        print('Game data saved!\n')

    elif cmd == 'load':
        inform = True
        # reading data from json file
        with open('game.json', 'r') as f:
            save_data = json.loads(f.read())
        # loading the data
        names = save_data['names']
        history = save_data['history']
        print('Game data loaded!')

    elif cmd in ['points', 'pp', 'standings']:
        print('\nCurrent standings:')
        # displaying points
        sort = sorted(points.items(), key=lambda x: x[1], reverse=True)
        for i, e in enumerate(sort):
            n, p = e
            print(f'{"I"*(i+1)}. {n}: {p} pts')
        print()

    elif cmd == 'history':
        print('\nGame history:')
        # displaying game history
        for r in history:
            n = ', '.join(list(r.keys()))
            p = list(r.values())[0]
            print(f'* {p} pts -> {n}')
        print()

    elif cmd in ['undo', 'back']:
        history.pop()
        print('Undo successful!\n')

    elif cmd == 'new':
        # resets everything
        names = get_names()
        history = []
        inform = True
        winners = {}
        won = False
