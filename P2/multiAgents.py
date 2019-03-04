# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
#import os 

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]
    
    def manhattanDistance( xy1, xy2 ):
       "Returns the Manhattan distance between points xy1 and xy2"
       return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )
	   
    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList() # asList() added
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"		
        gos = 	successorGameState.getGhostPosition(1)	#ghost position!!!!!!
        #print "newPos", newPos        
        #print "getGhostPositions=", gos
        #print "newScaredTimes",	newScaredTimes	
        #print successorGameState
        #print "--->" , newScaredTimes
        #print "food list",newFood

        
        gos_dist = manhattanDistance(gos, newPos) # distance between ghost and pacman

        score = 	successorGameState.getScore()	# initialize the score with current game score
        #print score		
        if (gos_dist < 4):	# [1,4]push pacman away from ghost
            score -= 20		

        h = 0
        values = []	
        for f in newFood: # f is the index of the newFood list (newFood returns [(1,2),...,(5,2)] )
           h_f = manhattanDistance(f, newPos)
           values.append(h_f)		  
        #Note: The evaluation function you're writing is evaluating state-action pairs.


        if (currentGameState.getNumFood() > successorGameState.getNumFood()):	# if next.state has less food than current
              score += 110 # [70,110]


        if values:
            h = min(values)	
        tmp = -5*h	 # weight/factor = [2,6]		
        score = score + tmp
        return score	

        
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""	
    """~ https://en.wikipedia.org/wiki/Minimax#Pseudocode  ~"""
    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""	
    def max_value(self, gameState, depth):	#agentIndex always zero, cause refers to Maximizer-pacman
        if (depth == 0) or (gameState.isLose() == True) or (gameState.isWin() == True): #terminal states or depth=0
            return self.evaluationFunction(gameState)
        v = float("-inf")		
		
        legal_actions = gameState.getLegalActions(0)		#refers to mr.Pacman Returns a list of legal actions(agentIndex=0)
        successors = []		
        for action in legal_actions:
            successors.append(gameState.generateSuccessor(0, action)) 
	
        for state in successors:       
                v = max(v, self.min_value(state, depth, 1))       #depth is -1 from min_value 

        return v

    def min_value(self, gameState, depth, agentIndex):
        if (depth == 0) or (gameState.isLose() == True) or (gameState.isWin() == True):	#terminal states or depth=0
            return self.evaluationFunction(gameState)
        v = float("inf")
        last_gos = ( gameState.getNumAgents() - 1 ) #

        legal_actions = gameState.getLegalActions(agentIndex) #agentIndex 1...n ghosts-minimizers
        succ = []
        for action in legal_actions:
            succ.append(gameState.generateSuccessor(agentIndex,action))
        for state in succ:        
            if agentIndex ==  last_gos:		
                v = min(v, self.max_value(state, depth-1))		#MAX VALUE with depth-1!!!,switch turn
				
            else:
                v = min(v, self.min_value(state, depth, agentIndex+1))	#MIN VALUE for next ghost 

        return v	
	
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

    =>  gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

    =>  gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

    =>  gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
       # print "getLegalActions",gameState.getLegalActions(1)
       # print "getLegalActions",gameState.getLegalActions(0)
       # print "getNumAgents",gameState.getNumAgents

        value = float("-inf")
        list_of_actions = gameState.getLegalActions(0)	# Pacman list_of_legal_actions
        #print list_of_actions
        #os.system("pause")
        for action in list_of_actions:
            #print "call Min_val"		##os.system("pause")
            v = self.min_value(gameState.generateSuccessor(0, action), self.depth, 1)   #min(state,depth,agentIndex)            
            if v > value:
                value = v
                best_move = action
        #print "========="
        return best_move
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
     Your minimax agent with alpha-beta pruning (question 3)
   """
   
    def max_value(self, gameState, depth, alpha, beta):
        if (depth == 0) or (gameState.isLose()==True ) or (gameState.isWin()==True ): #terminal states or depth=0
            return self.evaluationFunction(gameState)
        v = float("-inf")
		
        legal_actions = gameState.getLegalActions(0)
        succ = []
        for action in legal_actions:
            succ.append(gameState.generateSuccessor(0,action))
            for state in succ:
                v = max(v, self.min_value(state, depth, 1, alpha, beta))
                if v > beta: #You must not prune on equality
                    return v
                alpha = max(alpha,v)

        return v

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        if (depth == 0) or (gameState.isLose()==True ) or (gameState.isWin()==True ): #terminal states or depth=0
            return self.evaluationFunction(gameState)
        v = float("inf")
        last_gos = (gameState.getNumAgents()-1)
		
        legal_actions = gameState.getLegalActions(agentIndex)
        succ = []
        for action in legal_actions:
            succ.append(gameState.generateSuccessor(agentIndex,action))
            for state in succ:
                if agentIndex == last_gos:
                    v = min(v, self.max_value(state, depth-1, alpha, beta))
                else:
                    v = min(v, self.min_value(state, depth, agentIndex+1, alpha, beta))
                if v < alpha: #You must not prune on equality
                    return v
                beta = min(beta,v)
        return v
 
    def getAction(self, gameState):
        """
         Returns the minimax action using self.depth and self.evaluationFunction
       """

        "*** YOUR CODE HERE ***"
        alpha,beta,value = float("-inf"), float("inf"),float("-inf")

		
        list_of_actions = gameState.getLegalActions(0)
        #os.system("pause")
        for action in list_of_actions:
            v = self.min_value(gameState.generateSuccessor(0, action), self.depth, 1, alpha, beta)            
            alpha = max(alpha,v)
            if v > value:
                value = v
                best_move = action
        return best_move	

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


	
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
	#pacman.py -l smallClassic -p MinimaxAgent -a evalFn=better
    """

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    score = currentGameState.getScore()
    '''~~~Extra~~~  # untested
    for capsule in currentGameState.getCapsules():       	
        cap_dist = util.manhattanDistance(capsule,newPos)
        if cap_dist < 2:
           for g in newGhostStates:
               g_dist = newGhostStates[0].getPosition()
               if g_dist<3:
                  score +=10			   
           score +=2
    ~~~~~~'''		   
    #distance to ghosts
    for ghost in newGhostStates:
        gos_dist = newGhostStates[0].getPosition() 
        if gos_dist < 4 and newScaredTimes==0:   
            score -= 20
        elif newScaredTimes	!= 0 and gos_dist < 4:
            score += 20		
    Food = newFood.asList() 

    values = [] 
    for f in Food:
        h_f = util.manhattanDistance(f,newPos)
        values.append(h_f)		
    h =0 
    if values:
       h=min(values)
    tmp = 6*h	
    score = score - tmp	
    if len(Food): # oso uparxei fagito sto plegma afairese pontous!
       score -=2
	   
		
	   
    return score
		


# Abbreviation
better = betterEvaluationFunction

