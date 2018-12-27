from captureAgents import CaptureAgent, AgentFactory
import random, time, util
from game import Directions, Agent

from util import nearestPoint



#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveAgent', second='PerfectDefender', numTraining=0):
    # The following line is an example only; feel free to change it.
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########

class OffensiveAgent(CaptureAgent):
    def __init__(self, index, depth=5, alpha=0.9):
        self.depth = depth
        self.alpha = float(alpha)
        self.powerfulTimer = 0
        CaptureAgent.__init__(self, index, timeForComputing=.1)

    def registerInitialState(self, gameState):

        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

    def isPowerful(self):
        if self.powerfulTimer > 0:
            return True
        else:
            return False

    def getSuccessor(self, gameState, action):
        """
    Finds the next successor which is a grid position (location tuple).
    """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def chooseAction(self, gameState):
        if self.powerfulTimer > 0:
            self.powerfulTimer -= 1

        actionList = gameState.getLegalActions(self.index)
        actionList.remove("Stop")

        values = []
        for action in actionList:
            values.append(self.simulation(gameState, action))
        bestValue = max(values)

        bestActions = filter(lambda x: x[1] == bestValue, zip(actionList, values))
        return random.choice(bestActions)[0]

    def simulation(self, state, action):
        nextStateValue = self.evaluate(state, action)

        simulationValue = 0
        depth = self.depth

        while depth > 0:
            simulatedActionList = state.getLegalActions(self.index)
            simulatedActionList.remove('Stop')
            valueList = []
            for simulatedAction in simulatedActionList:
                # valueList.append(self.getSimulationValue(state, simulatedAction) * self.alpha)
                valueList.append(self.evaluate(state, simulatedAction) * self.alpha)
            maxValue = max(valueList)
            bestActions = filter(lambda x: x[1] == maxValue, zip(simulatedActionList, valueList))
            nextAction = random.choice(bestActions)[0]
            state = state.generateSuccessor(self.index, nextAction)
            simulationValue = simulationValue + maxValue
            depth = depth - 1

        nextStateValue = nextStateValue + simulationValue
        return nextStateValue

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPosition = myState.getPosition()
        enemyList = self.getOpponents(successor)
        enemies = []
        for enemyIndex in enemyList:
            enemies.append(successor.getAgentState(enemyIndex))
        invaders = []
        for enemy in enemies:
            if enemy.isPacman is True and enemy.getPosition() is not None:
                invaders.append(enemy)
        foodList = self.getFood(successor).asList()
        if len(invaders) > 0 and self.getScore(gameState) > 3:
            features = self.getDefensiveFeatures(gameState, action)
            weights = self.getDefensiveWeight(gameState, action)
        else:
            features = self.getFeatures(gameState, action, foodList)
            weights = self.getWeights(gameState, action)
        # return features * weights
        evaluationValue = 0
        if features:
            for feature in features:
                evaluationValue = evaluationValue + features[feature] * weights[feature]
        return evaluationValue

    def getFeatures(self, gameState, action, foodList):
        """
        Returns a counter of features for the state
        """

        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        actionList = successor.getLegalActions(self.index)
        actionList.remove("Stop")

        myState = successor.getAgentState(self.index)
        numOfCarrying = myState.numCarrying
        myPosition = myState.getPosition()
        team = self.getTeam(gameState)
        teammate = team[1]
        teammatePosition = gameState.getAgentState(teammate).getPosition()

        features['successorScore'] = self.getScore(successor)
        features['numOfCarrying'] = successor.getAgentState(self.index).numCarrying
        features['deadEnd'] = 0

        # food feature:
        # foodList = self.getFood(successor).asList()
        foodDistance = []
        if foodList:
            [foodDistance.append(self.getMazeDistance(myPosition, food)) for food in foodList]
            minFoodDist = min(foodDistance)
            features['minFoodDistance'] = minFoodDist
            features['eatFood'] = len(foodList)
        else:
            minFoodDist = 0
            features['minFoodDistance'] = 0
            features['eatFood'] = 0

        # capsule feature:
        capsuleList = self.getCapsules(successor)
        for capsule in capsuleList:
            if myPosition == capsule or capsule in teammatePosition:
                self.powerfulTimer = 40
        capsuleDistance = []
        if capsuleList:
            [capsuleDistance.append(self.getMazeDistance(myPosition, capsule)) for capsule in capsuleList]
            features['minCapsuleDistance'] = min(capsuleDistance)
            features['eatCapsule'] = len(capsuleList)
        else:
            features['minCapsuleDistance'] = 0
        if myPosition in capsuleList:
            features['eatCapsule'] = 0

        #  get the boundary of red and blue territory
        width = gameState.data.layout.width
        height = gameState.data.layout.height
        if self.red:
            boundary = (width - 2) / 2
        else:
            boundary = ((width - 2) / 2) + 1
        homeBoundary = []
        for i in range(1, height - 1):
            if not gameState.hasWall(boundary, i):
                homeBoundary.append((boundary, i))
        # get the min distance to home territory
        disToHome = []
        for i in range(len(homeBoundary)):
            disToHome.append(self.getMazeDistance(myPosition, homeBoundary[i]))
        minDisToHome = min(disToHome)
        features['retreat'] = 0


        # I am at enemy territory and enemy is a ghost
        enemyList = self.getOpponents(successor)
        ghostList = []
        for enemyIndex in enemyList:
            enemy = successor.getAgentState(enemyIndex)
            enemyPosition = enemy.getPosition()
            if enemyPosition is not None and enemy.isPacman is False:
                ghostList.append(enemy)
        if len(ghostList) > 0:
            disToGhost = []
            for ghost in ghostList:
                ghostPosition = ghost.getPosition()
                disToGhost.append(self.getMazeDistance(myPosition, ghostPosition))
            minDisToGhost = min(disToGhost)
            if minDisToGhost < 5:
                features['minGhostDistance'] = minDisToGhost
        else:
            noisyDist = []
            [noisyDist.append(successor.getAgentDistances()[enemyIndex]) for enemyIndex in enemyList]
            # for i in self.getOpponents(successor):
            #     noisyDist.append(successor.getAgentDistances()[i])
            features['minGhostDistance'] = min(noisyDist)

        # I am at home territory and enemy is a pacman
        pacmanList = []
        for enemyIndex in enemyList:
            enemy = successor.getAgentState(enemyIndex)
            enemyPosition = enemy.getPosition()
            if enemyPosition is not None and enemy.isPacman is True:
                pacmanList.append(enemy)
        if len(pacmanList) > 0:
            disToPacman = []
            for pacman in pacmanList:
                pacmanPosition = pacman.getPosition()
                disToPacman.append(self.getMazeDistance(myPosition, pacmanPosition))
            minDisToPacman = min(disToPacman)
            if minDisToPacman < 4:
                features['minPacmanDistance'] = minDisToPacman
        else:
            features['minPacmanDistance'] = 0

        enemy1 = gameState.getAgentState(enemyList[0])
        enemy2 = gameState.getAgentState(enemyList[1])
        enemy1_Position = enemy1.getPosition()
        enemy2_Position = enemy2.getPosition()

        for enemyIndex in enemyList:
            enemy = gameState.getAgentState(enemyIndex)
            enemyPosition = enemy.getPosition()
            if enemyPosition is not None:
                myDisToEnemy = self.getMazeDistance(myPosition, enemyPosition)
                teammateDisToEnemy = self.getMazeDistance(teammatePosition, enemyPosition)
                enemyActionList = gameState.getLegalActions(enemyIndex)
                enemyPossiblePosition = []
                [enemyPossiblePosition.append(
                    gameState.generateSuccessor(enemyIndex, eneAction).getAgentState(enemyIndex).
                        getPosition()) for eneAction in enemyActionList]

                if (myPosition == self.start) or (myPosition in enemyPossiblePosition):
                    if gameState.getAgentState(self.index).isPacman and self.isPowerful():
                        features['retreat'] = 100
                        features['eatGhost'] = myDisToEnemy
                        features['ghostBehind'] = 0
                        features['eatFood'] = 10*len(foodList)
                    else:
                        features['retreat'] = minDisToHome
                        features['minFoodDistance'] = 0
                        features['ghostBehind'] = -100

                # I am home territory as a ghost and enemy is pac man
                if not gameState.getAgentState(self.index).isPacman and enemy.isPacman:
                    # I will get eaten in 2 steps
                    if (myPosition == self.start) or (myPosition in enemyPossiblePosition):
                        features['retreat'] = minDisToHome
                    # if not gameState.getAgentState(self.index).isPacman and enemy.isPacman and not myState.scaredTimer>0:
                    elif myDisToEnemy < teammateDisToEnemy:
                        features['eatPacman'] = myDisToEnemy



                if gameState.getAgentState(self.index).isPacman and not self.isPowerful():
                    if myDisToEnemy < 3:  # time to retreat
                        features['minFoodDistance'] = 0
                        features['eatFood'] = 0
                        if capsuleList:
                            [capsuleDistance.append(self.getMazeDistance(myPosition, capsule)) for capsule in
                             capsuleList]
                            features['retreat'] = min(capsuleDistance)
                            # features['eatCapsule'] = len(capsuleList)
                        else:
                            features['retreat'] = minDisToHome
                        if len(actionList) == 1 or actionList is None:
                            features['deadEnd'] = 1
        # When it's time to retreat
        if successor.getAgentState(self.index).numCarrying > 3:
            features['minFoodDistance'] = 0
            features['eatFood'] = 0
            if capsuleList:
                [capsuleDistance.append(self.getMazeDistance(myPosition, capsule)) for capsule in capsuleList]
                features['retreat'] = min(capsuleDistance)
                # features['eatCapsule'] = len(capsuleList)
            else:
                features['retreat'] = minDisToHome
            if len(actionList)==1 or actionList is None:
                features['deadEnd'] = 1

        # ate capsule
        if self.isPowerful():
            features['powerfull'] = float(self.powerfulTimer / 40)
            features['eatFood'] = 10 * len(foodList)
            if foodList:
                [foodDistance.append(self.getMazeDistance(myPosition, food)) for food in foodList]
                minFoodDist = min(foodDistance)
                features['minFoodDistance'] = minFoodDist


            features['ghostBehind'] = 0
            # features['eatPacman'] = 100
            features['retreat'] = 0
            if numOfCarrying>0 and self.powerfulTimer < minFoodDist * 2:
                features['retreat'] = minDisToHome
                features['minFoodDistance'] = 0
        else:
            features['powerfull'] = 0.0

        return features

    def getWeights(self, gameState, action):
        """
        Normally, weights do not depend on the gamestate.  They can be either
        a counter or a dictionary.
        """
        return {'successorScore': 4000, 'minFoodDistance': -4, 'minCapsuleDistance': 0, 'minGhostDistance': 0,
                'minPacmanDistance': 0, 'ghostBehind': 10, 'eatFood':-180, 'eatCapsule': -200, 'eatPacman': -4,
                'powerfull': 100000, 'retreat': -0.1, 'deadEnd': 0, 'numOfCarrying': 0, 'eatGhost': -20}

    def getSimulationValue(self, newstate, fakeaction):
        features = util.Counter()
        nextState = newstate.generateSuccessor(self.index, fakeaction)
        features['successorScore'] = self.getScore(nextState)

        weights = {'successorScore': 0.0001}
        value = 0

        for feature in features:
            value += features[feature] * weights[feature]

        return value

    def getDefensiveFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPosition = myState.getPosition()
        enemyList = self.getOpponents(gameState)
        invaders = []  # visible invaders
        for enemyIndex in enemyList:
            enemy = successor.getAgentState(enemyIndex)
            if enemy.getPosition() is not None:
                if enemy.isPacman is True:
                    invaders.append(enemy)
                else:  # enemy is a ghost
                    enemyActionList = gameState.getLegalActions(enemyIndex)
                    enemyPossiblePosition = []
                    [enemyPossiblePosition.append(
                        gameState.generateSuccessor(enemyIndex, eneAction).getAgentState(enemyIndex).
                            getPosition()) for eneAction in enemyActionList]
                    # I will get eaten in 2 steps
                    if (myPosition == self.start) or (myPosition in enemyPossiblePosition):
                        features['ghostBehind'] = -100
        features['numOfInvaders'] = len(invaders)
        if len(invaders) > 0:
            disToInvader = []
            for invader in invaders:
                disToInvader.append(self.getMazeDistance(myPosition, invader.getPosition()))
            features['disToInvader'] = min(disToInvader)
        return

    def getDefensiveWeight(self, gameState, action):
        return {'ghostBehind': 10, 'numOfInvaders': -4, 'disToInvader': -10}



class DefensiveAgent(OffensiveAgent):
    def __init__(self, index):
        CaptureAgent.__init__(self, index)
        self.lastFoodList = None
        self.borderTarget = {}
        self.target = None

    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.distancer.getMazeDistances()

        borderX = ((gameState.data.layout.width - 2) / 2) + 1
        if self.red:
          borderX = (gameState.data.layout.width - 2) / 2

        self.freeWay = [ ]
        for i in range(1, gameState.data.layout.height - 1):
            if not gameState.hasWall(borderX, i):
                self.freeWay.append((borderX, i))
        while len(self.freeWay) > (gameState.data.layout.height - 2) / 2:
            self.freeWay.pop(0)
            self.freeWay.pop(len(self.freeWay) - 1)
        self.borderToFoodDistance(gameState)

    def borderToFoodDistance(self, gameState):
        foodList = self.getFoodYouAreDefending(gameState).asList()
        total = 0

        for position in self.freeWay:
            if foodList:
                closestFood = min([self.getMazeDistance(position, food) for food in foodList])
                # We can't divide by 0!
                if closestFood == 0:
                    closestFood = 1
                self.borderTarget[position] = float(closestFood)
                total += self.borderTarget[position]

        if total == 0:
            total = 1
        for x in self.borderTarget.keys():
            self.borderTarget[ x ] = float(self.borderTarget[ x ]) / float(total)

    def selectGuardTarget(self):
        rand = random.random()
        sum = 0.0
        for x in self.borderTarget.keys():
            sum += self.borderTarget[ x ]
            if rand < sum:
                return x

    def chooseAction(self, gameState):
        if self.lastFoodList and len(self.lastFoodList) != len(self.getFoodYouAreDefending(gameState).asList()):
            self.borderToFoodDistance(gameState)

        mypos = gameState.getAgentPosition(self.index)
        if mypos == self.target:
            self.target = None

        opponents = self.getOpponents(gameState)
        enemies = [ gameState.getAgentState(i) for i in opponents ]
        invaders = filter(lambda x: x.isPacman and x.getPosition() != None, enemies)
        if len(invaders) > 0:
            positions = [ agent.getPosition() for agent in invaders ]
            self.target = min(positions, key=lambda x: self.getMazeDistance(mypos, x))

        elif self.lastFoodList != None:
            eaten = set(self.lastFoodList) - set(self.getFoodYouAreDefending(gameState).asList())
            if len(eaten) > 0:
                self.target = eaten.pop()

        self.lastFoodList = self.getFoodYouAreDefending(gameState).asList()

        if self.target == None and len(self.getFoodYouAreDefending(gameState).asList()) <= 4:
            foodList = self.getFoodYouAreDefending(gameState).asList() \
                   + self.getCapsulesYouAreDefending(gameState)
            self.target = random.choice(foodList)

        elif self.target == None:
            self.target = self.selectGuardTarget()

        actions = gameState.getLegalActions(self.index)
        actions.remove(Directions.STOP)
        goodActions = [ ]
        qvalues = [ ]
        for a in actions:
            successor = gameState.generateSuccessor(self.index, a)
            successorState=successor.getAgentState(self.index)

            if not successorState.isPacman :
                newpos = successor.getAgentPosition(self.index)
                goodActions.append(a)
                qvalues.append((self.getMazeDistance(self.target,newpos),a))
            else:
                qvalues.append((99999, a))

        # Randomly chooses between ties.
        best,action = min(qvalues)
        action = [a for q,a in qvalues if q==best ]

        return random.choice(action)

class BottomAgent(OffensiveAgent):
    def getFeatures(self, gameState, action, foodList):
        bottomFoodList = self.bottom(foodList)
        OffensiveAgent.getFeatures(self, gameState, action, bottomFoodList)

    def bottom(self, foodList):
        # return the  food list that locate at the bottom of map
        if foodList:
            minimum = foodList[0][1]
            bottomList = []
            for i in range(len(foodList)):
                # for each food in food list, find the ones with minimal coordinate
                if foodList[i][1] < minimum:
                    minimum = foodList[i][1]
                    bottomList[:] = []
                    bottomList.append(foodList[i])
                elif foodList[i][1] == minimum:
                    bottomList.append(foodList[i])
            return bottomList


class PerfectDefender(DefensiveAgent, BottomAgent):
    def __init__(self, index):
        OffensiveAgent.__init__(self, index)
        DefensiveAgent.__init__(self, index)
        self.start = self.index

    def chooseAction(self, gameState):
        opponents = self.getOpponents(gameState)
        enemies = [gameState.getAgentState(i) for i in opponents]
        invaders = filter(lambda x: x.isPacman, enemies)
        score = self.getScore(gameState)
        if len(invaders) > 0 :
            return DefensiveAgent.chooseAction(self, gameState)
        else:
            return BottomAgent.chooseAction(self, gameState)