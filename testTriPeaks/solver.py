#!/usr/bin/env python3

import time
from utility import getNextStates, convertDigits2Long, convertLong2Digits, loadTripeaks

def goOverTableWithMask(peaksArray, stock):
    # Timer
    statPrevEndTime = time.time()
    statStartTime = time.time()
    statPrevCnt = 0
    statCounter = 0

    import queue
    # Queue for relaxing
    pqueue = queue.PriorityQueue()
    # add viewed states to prevent revisit
    checkedStates = []
    u64state = convertDigits2Long(51, 1, stock[0], 0x0FFFFFFF)
    pqueue.put((51, (u64state, ["Start"])))
    finalHistory = []

    while pqueue:
        # Change counter
        statCounter += 1
        # Get first element
        _, (curState, history) = pqueue.get()
        # Unpack state
        remainingCards, stockNum, lastCard, binaryMask = convertLong2Digits(curState)
        # Exit if we solved.
        if binaryMask == 0:
            print("Success!")
            finalHistory = history
            break
        
        # Only check if state not in history
        if curState not in checkedStates:
            checkedStates.append(curState)
            # Get its children
            state_steps = getNextStates(curState, peaksArray, stock)

            for state, step in state_steps:
                remainingCards, stockNum, lastCard, binaryMask = convertLong2Digits(state)
                newHistory = [i for i in history]
                newHistory.append(step)
                pqueue.put((remainingCards, (state, newHistory)))

        # Print debug info.   
        if statCounter%12345 == 4:
            print("mask:{:28b} {} lastCard={}".format(binaryMask, "curTable", lastCard))
            #break
            print("statCounter {}, pqueue remains {}, transcation rate {:.1f}/s, eta {:.1f}s, total {:.1f}s".format(
                statCounter,
                pqueue.qsize(),
                (statCounter - statPrevCnt)/(time.time()-statPrevEndTime),
                (50000 - statCounter)*(time.time()-statPrevEndTime) / (statCounter - statPrevCnt),
                time.time() - statStartTime))
            #print(pqueue[0])
            statPrevEndTime = time.time()
            statPrevCnt = statCounter
    
    print("Queue finished. {} steps.".format(statCounter))
    return finalHistory



# Step 1: load peaks and stock
flattenPeaks, stock = loadTripeaks("sampleTripeaksTable.json")
# Step 2: solve with: peaks, stock
    # Step 2.1: init state into queue
    # Step 2.2: while queue is not empty, find next states and enqueue.
finalHistory = goOverTableWithMask(flattenPeaks, stock)

for h in finalHistory:
    print(h)
