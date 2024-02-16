import json


VERSION = 'v1.1'
AUTHOR = 'Monti'
NAME = 'Snassist'


def print_info() -> None:
    print(f'{NAME} {VERSION} by {AUTHOR}\n')


def get_names() -> list:
    amount = input('2/[3] players: ')
    if amount == '2':
        amount = 2
    else:
        amount = 3

    players = []
    for i in range(amount):
        player = input(f'Name of [player{i+1}]: ')
        # default name for players
        if player == '':
            player = f'player{i+1}'
        players.append(player)
    return players


def ask_autosave() -> bool:
    inp = input('Autosave progress? [y]/n: ')
    if inp.lower() in ['n', 'no']:
        return False
    return True


def get_points(nam: list, his: list) -> dict:
    pts = {n: 0 for n in nam}

    # adding points together
    for result in his:
        for n, pt in result.items():
            pts[n] += pt

    return pts


# global variables
print_info()
names = get_names()
autosave = ask_autosave()
savable = False
history = []
inform = True
winners = {}
won = False

print('\uf45b'*54)

# main loop
while True:
    round_ = len(history)
    caller = round_ % len(names)
    points = get_points(names, history)
    savable = False

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
        print(f'Round {round_ + 1}!')
        print(f'Caller is {names[caller]}!')
        inform = False

    # taking user input
    cmd = input(f'\n@> ')
    print('\uf45b'*54)
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
        savable = True

    # managing commands
    elif cmd in ['quit', 'q', 'exit']:
        exit()

    if cmd == 'save' or (autosave and savable):
        save_data = json.dumps({
            'names': names,
            'history': history,
        })
        # writing data to json file
        with open('game.json', 'w') as f:
            f.write(save_data)

    if cmd == 'load':
        inform = True
        # reading data from json file
        with open('game.json', 'r') as f:
            save_data = json.loads(f.read())
        # loading the data
        names = save_data['names']
        history = save_data['history']
        print('Loaded from latest save!\n')

    elif cmd in ['points', 'pp', 'standings']:
        print('Standings:')
        # displaying points
        sort = sorted(points.items(), key=lambda x: x[1], reverse=True)
        for i, e in enumerate(sort):
            n, p = e
            print(f'  {"I"*(i+1)}. {n}: {p} pts')

    elif cmd == 'history':
        if len(history) < 1:
            print('No history...')
            continue
        print('History:')
        # displaying game history
        for r in history:
            n = ', '.join(list(r.keys()))
            p = list(r.values())[0]
            print(f'  {p} pts -> {n}')

    elif cmd in ['undo', 'back']:
        if len(history) < 1:
            print('Nothing to undo...')
            continue
        history.pop()
        print('Undo successful!')

    elif cmd == 'new':
        # resets everything
        names = get_names()
        autosave = ask_autosave()
        savable = False
        history = []
        inform = True
        winners = {}
        won = False
        print('\uf45b'*54)
