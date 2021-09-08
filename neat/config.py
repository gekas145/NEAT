from neat.Node import Node

# crossover parameters
CHOOSE_ANOTHER_GENE_PROBABILITY = 0.5  # default 0.5
DISABLE_GENE_PROBABILITY = 0.75  # default 0.75

# mutations parameters
MUTATE_WEIGHT_PROBABILITY = 0.8
RESET_WEIGHT_PROBABILITY = 0.1
ADD_NODE_PROBABILITY = 0.008
ADD_CONNECTION_PROBABILITY = 0.08
CROSSOVER_PROBABILITY = 0.75

# species division parameters
COMPATIBILITY_THRESHOLD = 3
EXCESS_GENE_COEFF = 1
DISJOINT_GENE_COEFF = 1
AVERAGE_WEIGHT_DIFF_COEFF = 0.5
MIN_GENOME_LENGTH = 20

# selection parameters
MAX_STALENESS = 2000

# pole balancing rewards and penalties
OUT_OF_FIELD_PENALTY = 70
OUT_OF_ANGLE_PENALTY = 40
CENTER_ACCEPTABLE_DEVIATION = 0.2  # float from (0, 1)
CENTER_REWARD = 10  # reward for not going off center more then CENTER_ACCEPTABLE_DEVIATION
USUAL_REWARD = 4

# network parameters(used for pole balancing)
ACTIVATION_FUNCTION = Node.sigmoid
INPUTS_NUM = 3
OUTPUTS_NUM = 2  # can have values 1 or 2 only
DECISION_THRESHOLD = 0.5  # used when OUTPUTS_NUM == 1
