import random
import time


def GameResult(prev_coords, new_coords, player, dimensions, width, part_runs):
    diff = []  # Displacement
    diff2 = []  # Displacement as a multiple or fraction of the first
    diff3 = []  # Displacement as a multiple or fraction of the first
    diff4 = []  # Displacement as a multiple or fraction of the first
    ref = []  # Reference coordinate to check that the coordinates
    # can exist in a run.
    # First let's check if a run is completed.
    if part_runs:
        for run in part_runs:
            # Check if the new point has the same displacement
            # as two ot more other points with qualifying displacements.
            if width == 3:
                if (([abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-1]
                    or [abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-2])
                        and ([abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-1]
                            or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-2])):
            # If it does, add it to that partial run.
                    run.insert(-2, new_coords)
            elif width == 4:
                if (([abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-1]
                    or [abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-2]
                        or [abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-3])
                            and ([abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-1]
                                or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-2]
                                    or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-3])):
                    run.insert(-3, new_coords)
            elif width == 5:
                if (([abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-1]
                    or [abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-2]
                        or [abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-3]
                            or [abs(c1-c2) for c1, c2 in zip(run[0], new_coords)] == run[-4])
                                and ([abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-1]
                                    or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-2]
                                        or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-3]
                                            or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-4])):
                    run.insert(-4, new_coords)
            # If its length is the width of the board plus the
            # displacement values
            # then it is a win scenario.
            if len(run) == (width*2 - 1):
                print(player, " wins!!! with : ", run)
                part_runs = []
                prev_coords = []
                return player
    # Get the displacement values between the new point and all other previous points
    for coords in prev_coords:
        diff = [abs(c1-c2) for c1, c2 in zip(coords, new_coords)]
        """
        Ignore a pairing of points that have an uneven
        displacement as they can't exist in a run. If any
        two or more axis values have not expereienced
        equal displacement then it can't be a line with an
        angle of 0, 45, or 90 degrees, required to exist in a run.
        """
        # """Take the displacement values and create a diff which will be a
        # multiple or factor of the first, for referencing
        # closer or more distant points in a potential run."""
        """Add the new point to the partial run with the two/three/four displacement values
        ,for that run, at the end for referencing new points against"""
        if (set([1, 2]).issubset(diff)
            or set([1, 3]).issubset(diff)
                or set([1, 4]).issubset(diff)
                    or set([2, 3]).issubset(diff)
                        or set([2, 4]).issubset(diff)
                            or set([3, 4]).issubset(diff)):
            continue
        elif 1 in diff:
            diff2 = [c*2 for c in diff]
            diff3 = [c*3 for c in diff]
            diff4 = [c*4 for c in diff]
        elif 2 in diff:
            diff2 = [c/2 for c in diff]
            diff3 = [(c/2)*3 for c in diff]
            diff4 = [(c/2)*4 for c in diff]
        elif 3 in diff:
            diff2 = [c/3 for c in diff]
            diff3 = [(c/3)*2 for c in diff]
            diff4 = [(c/3)*4 for c in diff]
        elif 4 in diff:
            diff2 = [c/4 for c in diff]
            diff3 = [(c/4)*2 for c in diff]
            diff4 = [(c/4)*3 for c in diff]
        """Create a reference list with the coordinate values of the axis,
        of the new point, which have experienced displacement. If there
        are value pairings which can't exist in a run, ignore that point"""
        for i in range(dimensions):
            if diff[i] == 0:
                pass
            else:
                ref.append(new_coords[i])
        # If There are the following pairs of values in the
        # axis experiencing displacement ignore that point.
        if (((set([0, 1]).issubset(ref) or set([1, 2]).issubset(ref)) and width == 3)
            or ((set([0, 2]).issubset(ref) or set([0, 1]).issubset(ref)
                or set([1, 3]).issubset(ref) or set([2, 3]).issubset(ref)) and width == 4)
                        or ((set([0, 1]).issubset(ref) or set([0, 2]).issubset(ref)
                            or set([0, 3]).issubset(ref) or set([1, 2]).issubset(ref)
                                or set([1, 4]).issubset(ref) or set([2, 3]).issubset(ref)
                                    or set([2, 4]).issubset(ref) or set([3, 4]).issubset(ref)) and width == 5)):
            print("ineligable: ", ref, ", and relavent diff: ", diff,
            ", and new_coords: ", new_coords, ", and other coords: ", coords)
            pass
        elif width == 3:
            part_runs.append([coords, new_coords, diff, diff2])
        elif width == 4:
            part_runs.append([coords, new_coords, diff, diff2, diff3])
        elif width == 5:
            part_runs.append([coords, new_coords, diff, diff2, diff3, diff4])
        ref = []
    print("Partial runs for ", player, ": ", part_runs)
    ref = []


def CompPlay(player_part_runs,
                spent_runs,
                human_coords,
                computer_coords,
                width,
                dimensions):
    number_list = [0, 1, 2, 3, 4][:width]
    ref_list = []
    comp_coords = []
    # time.sleep(0.5)
    if player_part_runs:
        for run in reversed(player_part_runs):
            comp_coords = []
            if (len(run) == ((width*2)-2) and run not in spent_runs):
                for i in range(dimensions):
                    if run[width-1][i] == 0:
                        comp_coords.append(run[0][i])
                    else:
                        for j in range(width-1):
                            ref_list.append(run[j][i])
                        comp_coords.append(list(set(
                            number_list) - set(ref_list))[0])
                        ref_list = []
                if (comp_coords in computer_coords
                        or comp_coords in human_coords):
                    spent_runs.append(run)
                    comp_coords = []
                    if len(computer_coords) == 1:
                        for i in range(dimensions):
                            n = random.randint(0, width-1)
                            comp_coords.append(n)
                        return comp_coords[:dimensions]
                else:
                    return comp_coords[:dimensions]
        while True:
            for i in range(dimensions):
                n = random.randint(0, width-1)
                comp_coords.append(n)
            if (comp_coords in computer_coords
                    or comp_coords in human_coords):
                comp_coords = []
            else:
                return comp_coords[:dimensions]
    else:
        while True:
            for i in range(dimensions):
                n = random.randint(0, width-1)
                comp_coords.append(n)
            if (comp_coords in computer_coords
                    or comp_coords in human_coords):
                comp_coords = []
            else:
                return comp_coords[:dimensions]
    return comp_coords[:dimensions]
