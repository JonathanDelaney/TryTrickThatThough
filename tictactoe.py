
partial_runsP1 = []
partial_runsP2 = []


def GameResult(prev_coords, new_coords, player, dimensions, width):
    global partial_runsP1, partial_runsP2
    diff = [] # Displacement
    diff2 = [] # Displacement as a multiple or fraction of the first
    ref = [] # Reference coordinate to check that the coordinates can exist in a run
    if (player == "player1"):
        # Check if a run is completed.
        if partial_runsP1:
            for run in partial_runsP1:
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
                                    or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-2])
                                        or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-3]):
                        run.insert(-3, new_coords)
                # If its length is the width of the board plus the two displacement values
                # then it is a win scenario.
                    if len(run) == (width*2 - 1):
                        print("Player One wins!!! with : ", run)
                        partial_runsP1 = []
                        partial_runsP2 = []
                        return "victory for player one"
                    else:
                        pass
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
            """Add the new point to the partial run with the two displacement values
            for that line at the end for referencing against new points"""
            if (set([1, 2]).issubset(diff)
                or set([1, 3]).issubset(diff)
                    or set([2, 3]).issubset(diff)):
                pass
            elif (2 in diff and width == 3):
                diff2 = [(abs(c1-c2))/2 for c1, c2 in zip(coords, new_coords)]
                partial_runsP1.append([coords, new_coords, diff, diff2])
            elif (3 in diff and width == 4):
                diff2 = [((abs(c1-c2))/3)*2 for c1, c2 in zip(coords, new_coords)]
                diff3 = [(abs(c1-c2))/3 for c1, c2 in zip(coords, new_coords)]
                partial_runsP1.append([coords, new_coords, diff, diff2, diff3])
            # Create the multiple/factor diff list for reference
            elif ((1 in diff and width == 3) or
                ((1 in diff or 2 in diff) and width == 4)):
                if 2 in diff:
                    diff2 = [(abs(c1-c2))/2 for c1, c2 in zip(coords, new_coords)]
                    diff3 = [((abs(c1-c2))/2)*3 for c1, c2 in zip(coords, new_coords)]
                else:
                    diff2 = [(abs(c1-c2))*2 for c1, c2 in zip(coords, new_coords)]
                    diff3 = [(abs(c1-c2))*3 for c1, c2 in zip(coords, new_coords)]
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
                        or set([1, 3]).issubset(ref) or set([2, 3]).issubset(ref)) and width == 4)):
                    print("ineligable: ", ref, ", and relavent diff: ", diff,
                    ", and new_coords: ", new_coords, ", and other coords: ", coords)
                    ref = []
                elif width == 3:
                    partial_runsP1.append([coords, new_coords, diff, diff2])
                elif width == 4:
                    partial_runsP1.append([coords, new_coords, diff, diff2, diff3])
    else:
        # Check if a run is completed.
        if partial_runsP2:
            for run in partial_runsP2:
                # Check if the new point has the same displacement
                # as two other points with qualifying displacements.
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
                                    or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-2])
                                        or [abs(c1-c2) for c1, c2 in zip(run[1], new_coords)] == run[-3]):
                # If it does, add it to that partial run.
                        run.insert(-3, new_coords)
                # If its length is the width of the board plus the two displacement values
                # then it is a win scenario.
                    if len(run) == (width*2 - 1):
                        print("Player Two wins!!! with : ", run)
                        partial_runsP1 = []
                        partial_runsP2 = []
                        return "victory for player two"
                    else:
                        pass
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
            """Add the new point to the partial run with the two displacement values
            for that line at the end for referencing against new points"""
            if (set([1, 2]).issubset(diff)
                or set([1, 3]).issubset(diff)
                    or set([2, 3]).issubset(diff)):
                print("ineligable: ", ref, ", and relavent diff: ", diff,
                ", and new_coords: ", new_coords, ", and other coords: ", coords)
                pass
            elif (2 in diff and width == 3):
                diff2 = [(abs(c1-c2))/2 for c1, c2 in zip(coords, new_coords)]
                partial_runsP2.append([coords, new_coords, diff, diff2])
            elif (3 in diff and width == 4):
                diff2 = [((abs(c1-c2))/3)*2 for c1, c2 in zip(coords, new_coords)]
                diff3 = [(abs(c1-c2))/3 for c1, c2 in zip(coords, new_coords)]
                partial_runsP2.append([coords, new_coords, diff, diff2, diff3])
            # Create the multiple/factor diff list for reference
            elif ((1 in diff and width == 3) or
                ((1 in diff or 2 in diff) and width == 4)):
                if 2 in diff:
                    diff2 = [(abs(c1-c2))/2 for c1, c2 in zip(coords, new_coords)]
                    diff3 = [((abs(c1-c2))/2)*3 for c1, c2 in zip(coords, new_coords)]
                else:
                    diff2 = [(abs(c1-c2))*2 for c1, c2 in zip(coords, new_coords)]
                    diff3 = [(abs(c1-c2))*3 for c1, c2 in zip(coords, new_coords)]
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
                        or set([1, 3]).issubset(ref) or set([2, 3]).issubset(ref)) and width == 4)):
                    print("ineligable: ", ref, ", and relavent diff: ", diff,
                    ", and new_coords: ", new_coords, ", and other coords: ", coords)
                    ref = []
                elif width == 3:
                    partial_runsP2.append([coords, new_coords, diff, diff2])
                elif width == 4:
                    partial_runsP2.append([coords, new_coords, diff, diff2, diff3])
