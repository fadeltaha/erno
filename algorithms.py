#   Here, use the Kociemba notation on the side where PLL is being solved and compare it with this dictionary
PLL_algorithms = {

}
#   Here, use the Kociemba notation on the side where OLL is being solved and compare it with this dictionary
OLL_algorithms = {

}

def recognize_OLL_algorithm(algorithm):
    if algorithm in OLL_algorithms:
        return OLL_algorithms[algorithm]
    else:
        return "Unknown or inefficient OLL algorithm used"
    
def recognize_PLL_algorithm(algorithm):
    if algorithm in PLL_algorithms:
        return PLL_algorithms[algorithm]
    else:
        return "Unknown or inefficient PLL algorithm used"