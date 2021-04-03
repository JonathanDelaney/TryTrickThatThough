
partial_runsP1 = []
partial_runsP2 = []


def GameResult(prev_coords, new_coords, player, dimensions, width):
    global partial_runsP1, partial_runsP2
    diff = []
    ref = []
    if player == "player1":
        for run in partial_runsP1:
            if ([abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[2] or
                    [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[2]):
                return print("Player One wins!!!")
        for coords in prev_coords:
            diff = [abs(c1-c2) for c1, c2 in zip(coords, new_coords)]
            if set([1, 2]).issubset(diff):
                pass
            elif 2 in diff:
                partial_runsP2.append([coords, new_coords])
            elif 1 in diff:
                for i in range(dimensions):
                    if diff[i] == 0:
                        pass
                    elif new_coords[i]:
                        ref.append(new_coords[i])
                if (set([0, 1]).issubset(ref) and set([2, 1]).issubset(ref)):
                    pass
                else:
                    partial_runsP1.append([coords, new_coords, diff])
    else:
        for run in partial_runsP2:
            if ([abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[2] or
                    [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[2]):
                return print("Player Two wins!!!")
        for coords in prev_coords:
            diff = [abs(c1-c2) for c1, c2 in zip(coords, new_coords)]
            if set([1, 2]).issubset(diff):
                pass
            elif 2 in diff:
                partial_runsP2.append([coords, new_coords])
            elif 1 in diff:
                for i in range(dimensions):
                    if diff[i] == 0:
                        pass
                    elif new_coords[i]:
                        ref.append(new_coords[i])
                if (set([1, 0]).issubset(ref) and set([1, 2]).issubset(ref)):
                    pass
                else:
                    partial_runsP2.append([coords, new_coords, diff])
    return print("Partial runs are for player1, player2:",
                partial_runsP1, partial_runsP2)
