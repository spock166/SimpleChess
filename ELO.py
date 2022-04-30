def expected_score(player_score, opponent_score):
    difference = opponent_score-player_score
    exponent = difference/400.0

    return 1/(1+10**exponent)

def update_score(player_A_score, player_B_score, player_A_outcome):
    player_B_outcome = 1 - player_A_outcome
    E_A = expected_score(player_A_score,player_B_score)
    E_B = 1 - E_A

    K = 16

    return player_A_score + K * (player_A_outcome-E_A), player_B_score + K * (player_B_outcome-E_B)

