import time, random
def simulate_points():
    score={"set_a":0,"set_b":0,"game_a":0,"game_b":0,"server":"A"}
    while True:
        pt = random.choice(["A","B"])
        if pt=="A": score["game_a"]+=1
        else: score["game_b"]+=1
        yield {**score, "point_winner": pt}
        time.sleep(1)
