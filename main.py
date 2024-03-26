
from models.round import Round
from service.dbService import DBService
import miscUtility as mu
from models.quest import Quest
from models.player import Player
import pyfiglet
import random
from log4python.Log4python import log as Logger
from service.configService import ConfigService

#for plotting
import matplotlib.pyplot as plt
# import scikitplot as skplt
# from sklearn.ensemble import RandomForestClassifier
#from sklearn import linear_model
from sklearn.linear_model import LinearRegression
import pandas as pd

import os.path
from csv import writer
import datetime 
import colorsys

log = Logger("main")

def createBarPlot(title, fignum, X, Y, X_label, Y_label, X__tick_labels):
    fig = plt.figure(fignum, figsize=(8, 6))
    # ax = plt.subplots()
    ax = fig.add_subplot(111)
    ax.bar(X, Y, color ='maroon',
        width = .4)
    ax.set_title(title)
    ax.set_xlabel(X_label)
    ax.set_ylabel(Y_label)
    ax.set_yticks(Y)
    ax.set_xticks(X)
    ax.set_xticklabels(X__tick_labels, rotation=90)


# def createFeatureImportancePlot(title, fignum, X, Y, X_label, Y_label, X__tick_labels):
#     # rf = RandomForestClassifier()
#     # rf.fit(X, X__tick_labels)
#     # skplt.estimators.plot_feature_importances(rf, feature_names=X)
#     fig = plt.figure(fignum, figsize=(8, 6))
    
#     ax = plt.subplots()
#     ax = fig.add_subplot(111)
    
#     # ax.bar(X, Y, color ='maroon',
#     #     width = 0.4)

#     ax.set_title(title)
#     ax.set_xlabel(X_label)
#     ax.set_ylabel(Y_label)
#     # ax.set_xticklabels(X__tick_labels, rotation=90)
#     plt.ion()     # turns on interactive mode
#     plt.show()    # now this should be non-blocking


header1 = pyfiglet.figlet_format("\nContent Generation Simulation \n- Josh Boyd")
log.info(header1)
log.info("Developed on Windows and Visual Studio Code")

config = ConfigService()
PLAYER_COUNT = config.playerCount
QUEST_COUNT = config.questCount
PERSONALITIES = config.personalities
DB = DBService()
players = []
quests = []
fignum = 0

now = datetime.datetime.now()
dateForFn = now.strftime('%Y%m%dT%H%M%S')
outputDirectory = "output"
if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

#***************************************************************************
#generate data

#randomly pick PLAYER_COUNT personalities to assign to players
#create players
for idx, p in enumerate(random.choices(PERSONALITIES, k=PLAYER_COUNT)):
    players.append(Player(idx, p))
    
#Random sample of 10% of quests for story quests.
storyIndexes = random.sample(range(QUEST_COUNT), k=int(QUEST_COUNT * .10))
#Random sample of 25% of quests for two player quests.
twoPlayerIndexes = random.sample(range(QUEST_COUNT), int(QUEST_COUNT * .25))
#Random sample of 5% of quests for three player quests. Overlap of threePlayerIndexes takes precedence over twoPlayerIndexes.
threePlayerIndexes = random.sample(range(QUEST_COUNT), k=int(QUEST_COUNT * .05))
 
#randomly pick QUEST_COUNT personalities to assign to Quests
for idx in range(QUEST_COUNT):
    isStory = idx in storyIndexes
    #Overlap of threePlayerIndexes takes precedence over twoPlayerIndexes. default is 1.
    requiredPlayers = 3 if idx in threePlayerIndexes else 2 if idx in twoPlayerIndexes else 1
    #pick a random sample of 1-3 personalities to assign to the quest.
    questPersonalities = random.sample(PERSONALITIES, k=random.randrange(1,4))
    quests.append(Quest(idx, isStory, requiredPlayers, questPersonalities))

#log.info(quests)

#***************************************************************************
#run sim

validPlayers = []
validQuests = []
currPlayerPool = []
currQuestPool = []
keepRunning = True
rounds = []
round = -1
while keepRunning:
    round += 1
    validPlayers = [x for x in players]
    validQuests = [x for x in quests if (x.isStory == True and x.totalCompletionsCount == 0) or (len(x.players) < x.requiredPlayerCount)]
    validStoryQuests = [x for x in quests if (x.isStory == True and x.totalCompletionsCount == 0)]
    startedQuestsWaitingOnMorePlayers = [x for x in quests if len(x.players) > 0 and (len(x.players) < x.requiredPlayerCount)]
    currPlayerPool =  random.choices(validPlayers, k=random.randrange(3,len(players)))
    currQuestPool = random.choices(validQuests, k=random.randrange(1,len(validPlayers)))

    log.info(f"round={round}, players={len(currPlayerPool)}, quests={len(currQuestPool)}, startedQuestsRequiringMorePlayers={len(startedQuestsWaitingOnMorePlayers)}")
    #loop through the players that are taking a turn
    for p in currPlayerPool:

        if len(p.quests) == 0:
            choice = random.choices(['wait', 'accept'], [.69, 1.31], k=1)[0]
        else:
            choice = random.choices(['wait', 'accept', 'submit'], [.69, 1.0, 1.31], k=1)[0]
        p.choice = choice

        if choice == "wait":
            p.idle()
        elif choice == "accept" and len(p.quests) <= 10:
            #try to get a quest
            matchedQuestsToAccept = [x for x in currQuestPool if p.personality in x.personalities]
            if len(matchedQuestsToAccept) > 0:
                questToAccept = random.choice(matchedQuestsToAccept)
                p.accept(questToAccept)
                p.choice += ": accepted"
            else:
                if p.idleCount >= 5:
                    unmatchedQuestToAccept = None
                    if(len(startedQuestsWaitingOnMorePlayers) > 0):
                        unmatchedQuestToAccept = random.choice(startedQuestsWaitingOnMorePlayers)
                    elif (len(validStoryQuests) > 0):
                        unmatchedQuestToAccept = random.choice(validStoryQuests)

                    if unmatchedQuestToAccept is not None:
                        p.accept(unmatchedQuestToAccept)
                        p.choice += ": non personality forced match"
                    else:
                        p.choice += ": no quest to accept"
                else:
                    p.idle()
                    p.choice += ": none available"
        elif choice == "submit" and len(p.quests) > 0:
            #turn in the quest
            submittedCount = 0
            for q in p.quests:
                if q.canComplete():
                    q.submitForAllPlayers()
                    submittedCount += 1
            p.choice += f": submitted ({submittedCount})"
        else:
            p.choice += ": forced idle"
            p.idle()
            
        log.info(f"p={p.id}, choice={p.choice}, idle={p.idleCount}")


    rounds.append(Round(round, currPlayerPool, currQuestPool))
    keepRunning = not (round >= 1000)
    if keepRunning:
        keepRunning = (not (len(storyIndexes) == len([x for x in quests if x.isStory == True and x.totalCompletionsCount > 0])))
        if not keepRunning:
           log.info("All story quests completed!")
    else:
        log.info("Max rounds reached!")


#***************************************************************************
# final results output

log.info(f"Final Results Output **********************")

log.info(f"PLAYER_COUNT:{PLAYER_COUNT}")
log.info(f"QUEST_COUNT:{QUEST_COUNT}")
log.info(f"PERSONALITIES:{PERSONALITIES}")
log.info(f"players:{players}")
log.info(f"quests:{quests}")  #too much
log.info(f"rounds:{rounds}")  #too much

#quests metrics
questsData = [
    ["Story", mu.count(q for q in quests if q.isStory == True) ],
    ["1 Plyr", mu.count(q for q in quests if q.requiredPlayerCount == 1)],
    ["2 Plyr", mu.count(q for q in quests if q.requiredPlayerCount == 2)],
    ["3 Plyr", mu.count(q for q in quests if q.requiredPlayerCount == 3)],
    ["1 Pers", mu.count(q for q in quests if len(q.personalities) == 1)],
    ["2 Pers", mu.count(q for q in quests if len(q.personalities) == 2)],
    ["3 Pers", mu.count(q for q in quests if len(q.personalities) == 3)],
    ["S Compl", mu.count(q for q in quests if q.totalCompletionsCount > 0 and q.isStory)],
    ["T Compl", mu.count(q for q in quests if q.totalCompletionsCount > 0)],
]

log.info(f"questsData:{questsData}")

#plot personalities *****
fignum += 1

playerPersonalities = [x.personality.id for  x in players]
personalityCounts = []
for p in PERSONALITIES:
    personalityCounts.append([p.id, p.name, playerPersonalities.count(p.id)])

X = [x[0] for x in personalityCounts]
Y = [x[2] for x in personalityCounts]
X__tick_labels = [x[1] for x in personalityCounts]


createBarPlot(f"Player Personalities ({len(players)})", fignum, X, Y, "Personality Type", "Player Count", X__tick_labels)
plt.savefig(f'{outputDirectory}\{dateForFn}_personalities_plot.png')

#plot quests metrics *****
fignum += 1
X = [ x[0] for x in questsData]
Y = [ x[1] for x in questsData]

createBarPlot(f"Quests ({len(quests)}), Rounds ({len(rounds)})", fignum, X, Y, "Field Type", "Count", X)
plt.savefig(f'{outputDirectory}\{dateForFn}_quests_plot.png')

#output run summary line to csv file *****

csvSummaryCols = [x[1] for x in personalityCounts] + [ x[0] for x in questsData]
csvSummaryOutput = [x[2] for x in personalityCounts] + [ x[1] for x in questsData]

fname_runSummary = f"{outputDirectory}\RunSummaries.csv"
if not os.path.isfile(fname_runSummary):
    with open(fname_runSummary, 'w', newline='') as f_object: 
        writer_object = writer(f_object)
        writer_object.writerow(csvSummaryCols)  
        f_object.close()

with open(fname_runSummary, 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
    writer_object = writer(f_object)
    # Result - a writer object
    # Pass the data in the list as an argument into the writerow() function
    writer_object.writerow(csvSummaryOutput)  
    # Close the file object
    f_object.close()

#output round details to csv file *****
fname_roundDetails = f"{outputDirectory}\{dateForFn}_Round.csv"
with open(fname_roundDetails, 'w', newline='') as f_object:  
    writer_object = writer(f_object)
    roundHeaders = ['id', 'players', 'quests']
    writer_object.writerow(roundHeaders) 
    for r in rounds:
        roundOutput = [r.id, r.players, r.quests]
        writer_object.writerow(roundOutput)  
    f_object.close()



#crazy linear regression
fignum += 1
#https://heartbeat.fritz.ai/implementing-multiple-linear-regression-using-sklearn-43b3d3f2fe8b

fig = plt.figure(fignum, figsize=(8, 6))
df_runSummaries = pd.read_csv(f"{outputDirectory}\RunSummaries.csv")

xCols = [col for col in df_runSummaries.columns if col != "T Compl"]
x = df_runSummaries[xCols]
y = df_runSummaries["T Compl"]

linear_regression = LinearRegression()
linear_regression.fit(x,y)
LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)

y_pred = linear_regression.predict(x)
# for v in x.values:
#     plt.scatter(v, y, color='red')

plt.plot(x, y, color='g', linewidth=3)
plt.plot(x, y_pred, color='blue', linewidth=1)
#plt.xticks(())
#plt.yticks(())
plt.savefig(f'{outputDirectory}\{dateForFn}_linearRegression_plot1.png')



#create linear regression with run summaries?
fignum += 1
fig = plt.figure(fignum, figsize=(8, 6))
#https://heartbeat.fritz.ai/implementing-multiple-linear-regression-using-sklearn-43b3d3f2fe8b

df_runSummaries = pd.read_csv(f"{outputDirectory}\RunSummaries.csv")

xCols = [col for col in df_runSummaries.columns if col != "T Compl"]
y = df_runSummaries["T Compl"]
rowIndex = 0
for col in xCols:
    x = df_runSummaries[[col]]

    linear_regression = LinearRegression()
    linear_regression.fit(x,y)
    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)

    y_pred = linear_regression.predict(x)
    # for v in x.values:
    #     plt.scatter(v, y, color='red')
    plt.scatter(x, y, color=mu.color(rowIndex))
    #plt.plot(x, y, color='g', linewidth=3)
    plt.plot(x, y_pred, color=mu.color(rowIndex), linewidth=3)
    rowIndex += 1
#plt.xticks(())
#plt.yticks(())
plt.savefig(f'{outputDirectory}\{dateForFn}_linearRegression_plot2.png')

#scatter
fignum += 1
fig = plt.figure(fignum, figsize=(8, 6))
ax = fig.add_subplot(111)
ax.set_xticklabels(df_runSummaries.columns, rotation = 90)


rowIndex = 0
for row in df_runSummaries.values:
    plt.plot(df_runSummaries.columns, row, color=mu.color(rowIndex))
    rowIndex += 1

#show plots *****
plt.ion()     # turns on interactive mode
plt.show()    # now this should be non-blocking

input("Press Enter to continue...")