# UoM COMP90054 Contest Project

# Youtube presentation
Presentation Video

![Video Link](https://www.youtube.com/embed/dpgpLCZLNX8)
<figure class="video_container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/dpgpLCZLNX8" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</figure>



### Design Decision Made
   * ##### Attribute Extraction 
      The below are the identified attributes used for 5-Step and Monte Carlo approach  
       * "eatfood": stores the count of leftover opponent food points
       * "eatCapsule": stores the count of capsules which are not consumed yet 
       * "distanceTOFood": stores the maze distance to the closest opponent food 
       * "successorScore": stores the current game score
       * "eatPacman": stores the maze distance from current position to closest enemy position
       * "deadend": If the next possible legal action is only one then this attribute is used.
       * "retreat": if there are capsules then runbacks towards the capsule otherwise runbacks the pacman attacker to the home territory
       *  "ghostBehind": checks if there is a ghost just two step away from the attacker
       * "isPowered": if any of the agents have eaten the power capsule this attribute is used for reward calculation.

      The below are the identified features used for Q-Function approach  
       * "capsules": stores the count of power capsules left
       * "numFoodLeft": stores the count of opponent food points 
       * "foodDistance": stores the maze distance to the closest opponent food 
       * "closestDefenderDistance": stores the maze distance to the closest opponent ghost 




   * Weight given for each attribute



### Techniques Tried
   * 5-Step (Final Approach)
   * Q-Function
   * Monte Carlo

#### 5-Step (Final Approach) 
The implementation could be found in the branch MCTS (https://gitlab.eng.unimelb.edu.au/sukritis/comp90054-pacman/tree/MCTS), we have used n-step Temporal Difference to decide the move for the agent. For each possible legal actions from a state, the q-value is taken from the max of the q-values returned from the simulation of each step. The simulation is done for the next 5 steps to calculate the best move possible.

Attacker:
N-steps: 
Each action has a corresponding child state. Among all possible child states, the one with highest simulation rewards means the best action for the current state. If there are tie rewards, we just randomly choose one from them. 

###### The simulation reward is determined by: 
   * The evaluation value of current child state + gamma * (the sum of the evaluation value for its further five child states.) That is to say, for each child state, we evaluate all its possible actions, among which, we pick the best action and add this action’s rewards to the current state. Then, for the corresponding state of this action, we repeat what we did- choosing its best action and adding the rewards. Repeat this for the next five states. Then, we multiply the sum rewards with gamma. Gamma is a discount factor that is less than one. So that the sum rewards of next five steps have a lesser weight than the reward of current child state. Finally, we compare all child states with the sum simulation rewards of the next five steps, among which, we chose the highest one as the best child state. Which means that the corresponding action is the best action for the current state. 

   * The evaluation value is determined by the sum value of the product of the features and the corresponding weight. From all legal actions, we pick the one with the highest value. As same, if there is a tie, we just randomly choose one from them.

###### Evaluation:
For each action, there is a basic value called successor score, whose weight is 4000. This won’t change in any situation. 
When we come out from the start, the value is mainly determined by the distance to food and the length of the food list. Therefore, it will go to the nearest location of the food. 

###### When we are in the home territory as a ghost:
If an enemy Pac man is approaching and we are not scared, the retreat value is changed to 0 and the eat Pac man value is changed to the minimum distance to this enemy. So, we will go toward to the invaders and eat it. If we are scared and will get eaten in 2 steps, the retreat value will be changed to the minimum distance towards the boundary, guarding the boundary. 

###### When we are in the opponent territory as a Pac man:
If an enemy is close to us, our first priority is not to be eaten. If they still have a capsule, the retreat value is changed to the minimum distance towards the capsule. So, we will go to the capsule location and eat it. If no capsule is left, the retreat value is changed to the minimum distance to the boundary between the red and blue team. At this point, we find that it is important to focus on safely returning the food agent is carrying to our side in order to recoup the points, instead of continuing chasing after the food. Also, the upper bound we set to the maximum number that a Pac man can carry is 4. Therefore, when a Pac man has collected 4 points of food, it will retreat to our home territory.

The value of being powerful is 100000 and is decreased as time goes by. When we ate the capsule, or we are powerful, the first priority is changed to collecting food. We will ignore the ghost behind us and the value of ghost is changed to 0. The value of retreat is also changed to 0. And, the value of eating food is 10 times than before. If the time left after consuming a power capsule is less than half distance towards food, the value of eating food is reverted back as normal and the retreat value is changed to the minimum distance towards tthe home territory.

If the agent would get eaten up in 2 steps and it is not powerful as well as none of the capsules are left, the retreat value will be set to the minimum distance to the boundary and the ghost behind value will be set to -100.

###### Defensive Status:

Only when the score is 4 or more and an invader is observed, the attacker will shift to defender status. The defensive value is only determined by the ghost, the number of invaders and the distance towards to the invaders. If we will get eaten in 2 steps, the value of ghost behind changed to -100. 

###### Perfect Defender:

The defender acts in two modes- attacker and defender. The working characteristics of the attacker mode is same as that of the normal attacker. The agent switches to defender mode when the enemy comes to its territory and becomes a Pac man.  When it switches to defender mode, it tries to locate the attacker by checking the location of the last food dot eaten. The agent gets the location of the last food dot eaten by taking a difference of the set of food dots from the previous observation and the set of the food dots from the current observation. The agent then sets that as its target location.
Out of all the possible legal actions from the agents current location, the best action is chosen that gives the least distance to the target set. In case of a tie between actions, an action is chosen randomly.
The reason why this is a perfect defender is because it not only defends but also acts as an attacker.

###### CRITICAL ANALYSIS
   1. Primary: 
     * The agent ignores the STOP action, which would be important when it gets blocked in order to not waste move or to get itself killed voluntarily.

   2. Secondary: 
     * As the number of goals is more than 1, we couldn’t apply monte-carlo and resorted to using Temporal Difference for 5 steps. The simulation could have improved a lot if the agent could simulate the next 20 steps but that could take a lot of time(more than 1 second) and get our agent disqualified.
     * The defender keeps switching its mode from attacker to defender depending on the opponent’s state. In case of a bad opponent, that keeps switching as pacman and ghost the perfect defender would also continue to switch between its modes.

###### OBSERVATIONS
1. The agent performed well, as it was able to win the matches against agents that used q learning.
2. Since the defender acts as both attacker and defender, that helped the agent’s team to accumulate more food dots.
3. The weakness of the system could be clearly observed by the matches against the top teams during the pre-competition. The attacker gets blocked in an alley that has only one entry/exit point, by the opponent. Since in our implementation we have removed the stop action, the blocked agent continues to find a path out and ends up wasting the steps.
4. In the pre-competition, the agent was able to defeat all the three agents of staff for one kind of maze, however, lost matches from the basic and top agents in the RANDOM6664 mazes. That was because for that particular match because of the maze structure, the agent was working both as attacker and defender and although, initially captured a lot of points got stuck in the end by one of the opponent’s pacman who tried to enter our region, while the other opponent agent already in our region was able to collect more food dots and win the match by a margin of just 3 or 4 points.

#### Q Function Approximation:
The implementation for Q function approximation can be found in the branch qLearning (https://gitlab.eng.unimelb.edu.au/sukritis/comp90054-pacman/tree/qLearning) in the GitLab repository.
Q function approximation is a linear approach to the reinforcement learning methodology of Q learning. The qValue for a particular state is calculated by multiplying the features obtained for that state with their corresponding weights. After the qValue calculation the weights are updated.
For Pacman contest, the features chosen along with their corresponding starting weights (weights were assigned after some trial matches and a justification for not starting with 0 weights is also mentioned below) were as listed below:
[NOTE: In the ideal scenario, the weights are initially assigned as zero and the agent is trained on the maze using the updated weights for each corresponding match).

###### a. Attacker

|Features|Weights|
| :------------------------------------: |  :------: | 
|Capsules in opponent’s side	Capsules|100|
|Number of food dots in opponent’s side	numFoodLeft|5|
|Distance from the nearest food dot	foodDistance|100|
|Distance from closest opponent	closestDefenderDistance|-10|

###### b. Defender

|Features|Weights|
| :------------------------------------: |  :------: |
|Number of invaders numInvaders|-10|
|Distance from closest invader invaderDistance|10|
|Food dots left that you are defending foodLeft|-1000|


###### Justification for the chosen initial weights: 
The features were assigned in such a way that if 

   1. An agent wants to attack then it’s primary focus would be on
     * Capsules: As capturing a capsule, scares the opponent’s defenders, more weightage is given to capturing the capsules.
     * Capturing the food dots: Since the score is based on number of food dots safely returned to our region, positive weightage is given to capturing the food dots and the closer a food dot is to agent, agent must focus on capturing it.
     * escaping from the opponent’s defender: If the opponent’s defender is not scared, then our attacker should try to run away from the defender as far as possible. Thus, the negative weightage for that.

   2. An agent which is defending would focus on 
    * The food dot count of the food it is defending:  if it decreases then that implies that the attacker of the opponent is in our region. 
    * The least the distance to the attacker is: more weightage should be given to it in order to make the defender attack it.
    * The number of attackers in its region of the maze.

###### CRITICAL ANALYSIS FOR Q FUNCTION APPROXIMATION
The reason why this approach was not chosen over n-step is because

   1. Primary: The maze is not fixed and it would take a painfully long time to train the agents. As the time limit for each match is 1200 steps the agents would end up losing the initial few matches to get a clear understanding of the maze.
   2. Secondary:  The features selected for the agents also play a major role during the approximation process. The features that were selected for this approach were not sufficient to train the pacman agent.

###### OBSERVATIONS MADE:
   1. MATCH AGAINST n-STEP AGENTS
     * Defender: The defender was stuck in the starting corner of the maze as it was trying to update its weights. It ended up wasting a lot of initial steps and towards the end of the game tried to leave the starting corner.
     * Attacker: With the given set of initial weights the attacker was able to attack and even eat a food dot. However, the opponent’s defender was strong and able to detect the attacker and kill it. The attacker after getting killed gets stuck in the starting position due to the weights that were updated for each action for the attacker.

   2. Key takeaway: 
     * Feature extraction/ selection and corresponding weight assignment play a critical role for q function approximation. 
     * Q function approximation could outperform the other agents if only there was no restriction on the time limit (i.e. they had time to train the agents) and the maze was fixed.



#### Monte Carlo Tree Search
The implementation for Monte Carlo Tree Search can be found in the branch qLearning (https://gitlab.eng.unimelb.edu.au/sukritis/comp90054-pacman/tree/Monte_Carlo) in the GitLab repository.
Monte Carlo Tree Search is heuristic search algorithm used in game playing to determine the best moves based on the current game state. Monte Carlo Tree Search starts by simulating the gameplay either till the end or till the specified steps, each simulation will have a result and these results can be evaluated based on winning or by using a heuristic by giving scores to each simulation. Based on the outcome of these simulations the next best move can be picked. In this project due to the time limit, each simulation is done for 20 steps from the current state and for each step the state is evaluated based on the feature values and weight. Monte Carlo Tree Search is used for attacker agent to eat the opponent food points and comes back to the home territory. Simulation is done for all the legal actions leaving out stop from the current state. For each legal action, the simulation is done 5 times and the results are summed. In each simulation process, the next action is simulated, these actions are chosen carefully by checking, it should be at least two steps away from the opponent ghosts and also should be near to the opponent food point. A temporary copy of game state and a local copy of food list and capsules are maintained while simulating the steps in order to be persistent. For each legal action, 5 simulations are run and the results are summed. While evaluating the result of each simulation step, these local copies are used to calculate the feature values. In the end, the max result action is chosen.

###### CRITICAL ANALYSIS FOR MONTE CARLO
The reason why this approach was not chosen over n-step is because

   1. Primary: Due to the time limit imposed for computation between each move, the simulation is limited to 20 steps as of this attacker agent is wasting steps when deciding the nearest action to food because in the simulation of the least important action is consuming more food point and is being allocated more weight, hence the least important action is being chosen.                         
   2. Secondary:  When an opponent ghost is near the boundary, the attacker agent just moves back and forth, it fails to consume food points.


###### OBSERVATIONS MADE:
   1. MATCH AGAINST n-STEP AGENTS
     * Defender: The defender effectively follows and eats the packman when in range of 5 distance. Guards along the boundary when opponent pacman not in range. 
     * Attacker: Eats two food points and comes back, if the opponent ghost is in distance of 5 then immediately returns home. It is wasting a few steps while going towards food point(i.e., not choosing shortest path). While returning home doesn't waste steps and chooses the shortest possible path.

### Comparison of Approaches Used
##### Reviewed as per performance

|5-Step|Q-Function|Monte Carlo|
| :-----------: |  :------: |  :------: |
|Returns next action quickly, quickest among the three|Initially takes time, after few steps works fast|Takes longer time to select the next action. Slowest among the three|
|Does not waste steps while attacking to consume opponent food dots. Best among the three|Steps are wasted while attacking|Few steps are wasted while attacking, compared to q-function waste less steps|


### Challenges Faced
   * Efficient attribute/feature extraction
   * Obtaining weight for each attribute/feature
   * For Q-Function approximation training pacman to obtain weights
   * For 5-Step and Monte Carlo approach identifying optimal weights for all scenarios

### Possible Improvements
1. If given some more time, we would have improvised the agent by adding some more features to get a better result with more suitable weights obtained from qlearning by training the agent in the maze first.
2. Instead of wasting moves when it gets blocked, we would have worked on making the pacman stop and observe for how long was it stopped and get itself killed in order to continue the game.
3. When the attacker is in opponents range, the attacker in our current implementation looks for the shortest path back home, this strategy could be updated to consider a path back home that contains food dots on its way such that our attacker is not eaten by the opponent and reach home safely.


## Team Members

* Ailin Zhang - ailinz1@student.unimelb.edu.au - 874810
* Sukriti Srivastava - sukritis@student.unimelb.edu.au - 932352
* Tarun Dev Thalakunte Rajappa - tthalakunte@student.unimelb.edu.au - 934175
