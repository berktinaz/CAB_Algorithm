# CAB_Algorithm
Implemented the "Continuum Armbed Bandit" algorithm given in the publication "On Two Continuum Armed Bandit Problems in High Dimensions". For playing arms, it uses the UCB1 algorithm as described in the text "Finite-time Analysis of the Multiarmed Bandit Problem".

UCB1 algorithm selects the arm that maximizes the upper bound of a confidence interval. The maximized variable consists of two terms: Exploitation term (mean of previous rewards) and Exploration term (width of the confidence interval).

# TO DO:
Use matplotlib to display the "Regret vs Time".
