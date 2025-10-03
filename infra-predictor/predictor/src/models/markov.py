from functools import lru_cache

def game_win_prob(p_server: float) -> float:
    @lru_cache(None)
    def P(a,b):
        if a>=4 and a-b>=2: return 1.0
        if b>=4 and b-a>=2: return 0.0
        return p_server*P(a+1,b) + (1-p_server)*P(a,b+1)
    return P(0,0)

def set_win_prob(p_hold_a: float, p_hold_b: float, starting_server: str="A") -> float:
    @lru_cache(None)
    def P(ga, gb, srv):
        if ga>=6 and ga-gb>=2: return 1.0
        if gb>=6 and gb-ga>=2: return 0.0
        if ga==6 and gb==6:
            tb = 0.5 + 0.25*(p_hold_a - p_hold_b)
            return max(0.0, min(1.0, tb))
        if srv=="A":
            pa = p_hold_a
            return pa*P(ga+1, gb, "B") + (1-pa)*P(ga, gb+1, "B")
        else:
            pb = p_hold_b
            return (1-pb)*P(ga+1, gb, "A") + pb*P(ga, gb+1, "A")
    return P(0,0, starting_server)

def match_win_prob(p_hold_a: float, p_hold_b: float, best_of: int=3) -> float:
    from math import comb
    ps = 0.5*(set_win_prob(p_hold_a,p_hold_b,"A")+set_win_prob(p_hold_a,p_hold_b,"B"))
    if best_of==3:
        return ps*ps + 2*ps*(1-ps)*ps
    p=0.0
    for k in range(3,6): p += comb(5,k)*(ps**k)*((1-ps)**(5-k))
    return p
