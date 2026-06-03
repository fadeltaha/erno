PLL_algorithms = {

}

OLL_algorithms = {
    "R U U R R F R F' U U R' F R F'" : "1"
    
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