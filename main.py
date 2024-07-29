import copy
from queue import deque
from queue import PriorityQueue

def hash(puzzle):
    res = []
    for bottle in puzzle:
        if not bottle:
            res.append("-")
        else:
            res.append("".join(bottle))
    return ";".join(res)


def end(puzzle):
    for bottle in puzzle:
        if bottle:
            s = set(bottle)
            s.discard("-1")
            if len(s) != 1:
                return False
    return True


def moveable(bottle1, bottle2):
    # if empty or full bottle1, not possible
    if len(set(bottle1)) == 1:
        return False
    # if empty bottle2 then it is true
    if len(set(bottle2)) == 1 and bottle2[-1] == "-1":
        sb1 = set(bottle1)
        sb1.discard("-1")
        if len(sb1) == 1:
            return False
        return True
    last = 3
    while bottle1[last] == "-1":
        last -= 1
    end = last
    start = end
    while bottle1[end] == bottle1[start]:
        start -= 1
    start += 1
    color = bottle1[last]
    amount = last - start + 1

    last2 = 3
    empty_count = 0
    while bottle2[last2] == "-1" and last2 >= 0:
        last2 -= 1
        empty_count += 1
    color2 = bottle2[last2]
    # print(f"From {bottle1=} to {bottle2=}: {color=}, {color2=} and {amount=} {empty_count=}")
    return color == color2 and empty_count >= amount

    

visited = set()

def performMove(x, y, puzzle):
    res = copy.deepcopy(puzzle)
    bottle1, bottle2 = res[x], res[y]
    last = 3
    while bottle1[last] == "-1":
        last -= 1
    end = last
    start = end
    while bottle1[end] == bottle1[start]:
        start -= 1
    start += 1
    color = bottle1[last]
    amount = last - start + 1
    # print(start, end)
    for i in range(start, 4):
        bottle1[i] = "-1"

    last2 = 3
    while last2 >= 0 and bottle2[last2] == "-1":
        last2 -= 1
    start2 = last2 + 1
    for i in range(start2, start2 + amount):
        bottle2[i] = color
    

    # print(f"After {x=} -> {y=} we get to {res=}")
    return res


def get_moves(p):
    res = []
    for i in range(len(p)):
        for j in range(len(p)):
            if i != j and moveable(p[i], p[j]):
                # print(f"We can {i=}({p[i]=}) -> {j=}({p[j]=})")
                new_puzzle = performMove(i, j, p)
                h = hash(new_puzzle)
                if h not in visited:
                    visited.add(h)
                    res.append(((i, j), new_puzzle))
    return res

def evaluation(puzzle):
    ans = 0
    for bottle in puzzle:
        ans += len(set(bottle))
    return ans

def solve(puzzle):
    q = PriorityQueue()
    depth = 1
    q.put((0, (puzzle, [])))
    count = 1
    while q:
        n, (p, pre) = q.get()
        if (count % 10000 == 0):
            print(count, p)
        moves = get_moves(p)
        for (i, j), new_puzzle in moves:
            if end(new_puzzle):
                return pre + [(i, j)]
            q.put((evaluation(new_puzzle), (new_puzzle, copy.deepcopy(pre) + [(i, j)])))
        count += 1

def translate(p):
    for i in range(len(p)):
        p[i] = list(map(str, p[i]))
    return p


# t = solve(
#     [
#         ["3", "3", "2", "1"],
#         ["7", "6", "5", "4"],
#         ["10", "9", "4", "8"],
#         ["8", "9", "5", "8"],
#         ["1", "11", "9", "2"],
#         ["2", "10", "2", "11"],
#         ["12", "9", "4", "10"],
#         ["12", "5", "4", "12"],
#         ["1", "3", "7", "6"],
#         ["12", "7", "11", "10"],
#         ["1", "12", "11", "7"],
#         ["8", "5", "3", "6"],
#         ["-1", "-1", "-1", "-1"],
#         ["-1", "-1", "-1", "-1"]
#     ]
# )

yellow = "1"
orange = "2"
gray = "3"
lgreen = "4"
lblue = "5"
green = "6"
purple = "7"
red = "8"
pink = "9"
brown = "10"
dblue = "11"
dgreen = "12"
empty = "-1"


t = solve(translate([
    [yellow, orange, gray, lgreen],
    [lblue, green, purple, red],
    [purple, lgreen, pink, green],
    [brown, red, pink, yellow],
    [purple, brown, dblue, green],
    [yellow, purple, gray, green],
    [dgreen, lblue, gray, orange],
    [pink, lblue, dgreen, red],
    [lgreen, lblue, dblue, dblue],
    [orange, pink, brown, dgreen],
    [orange, yellow, lgreen, gray],
    [dblue, dgreen, brown, red],
    [empty, empty, empty, empty],
    [empty, empty, empty, empty]
]))

print(len(t))
count = 0
for x in t:
    if count % 6 == 0:
        print("    ")
    count += 1
    print(x)


# t = solve(translate([[1,2,3,4], [4,3,4,2], [4,1,1,3], [3,2,1,2], [-1,-1,-1,-1], [-1, -1,-1,-1]]))
# print(len(t), t)
