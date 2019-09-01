#!/usr/bin/env python3


def convertLong2Digits(u64state):
    """
    Parse one long u64state to multiple fields.

    :param int u64state: input u64state.
    :return: remainingCards, stockNum, lastCard, binaryMask
    :rtype: int, int, int, int
    """
    return (u64state >> 48) & 0xFF, (u64state >> 40) & 0xFF, (u64state >> 32) & 0xF, u64state & 0x0FFFFFFF



def convertDigits2Long(remainingCards, stockNum, lastCard, binaryMask):
    """
    Build one long u64state from given digits.

    :param int remainingCards: How many cards remains (0-52)
    :param int stockNum: How many cards still in stock (0-24)
    :param int lastCard: The last card shown in this state. (1-13)
    :param int binaryMask: Binary mask show which place is present or not. (0x0FFFFFFF)
    :return: u64state
    :rtype: int
    """
    return (remainingCards << 48) | (stockNum << 40) | (lastCard << 32) | binaryMask

def convertArraypos2Layerpos(arrayidx):
    if arrayidx >= 18:
        return (4, arrayidx - 18)
    elif arrayidx >= 9:
        return (3, arrayidx - 9)
    elif arrayidx >= 3:
        return (2, arrayidx - 3)
    elif arrayidx >= 0:
        return (1, arrayidx)

def toString(binaryMask, flattenPeaks):
    ret = [0]*28
    maskStr = '{0:028b}'.format(binaryMask)
    for i in range(len(maskStr)):
        if maskStr[i] == '0':
            ret[i] = 0
        else:
            if flattenPeaks:
                ret[i] = flattenPeaks[i]
            else:
                ret[i] = 1
    
    return '\n'+'\n'.join([
        '        ,'.join(['{:3d}'.format(ret[i]) for i in range(3)]),
        '    ,'.join(['{:3d},{:3d}'.format(ret[i], ret[i+1]) for i in range(3,9,2)]),
        ','.join(['{:3d}'.format(ret[i]) for i in range(9,18)]),
        ','.join(['{:3d}'.format(ret[i]) for i in range(18,28)]),
        ])

# Load table 
def loadTripeaks(filename):
    import json
    with open(filename) as f:
        obj = json.load(f)

    flattenPeaks = [item for arr in obj["peaks"] for item in arr]

    return flattenPeaks, obj["stock"]


def getNextStates(curState, flattenPeaks, stock, history = None):
    """
    Get next u64state from current u64state-s.

    :param int curState: Current u64state of the game
    :param int[] flattenPeaks: tripeaks table
    :param int[] stock: stock cards array
    :param str[] history: history from first state
    :return: all next possible (u64state, history).
    :rtype: (int, str[])[]
    """
    # Return values
    ret = []
    # Unpack current u64state
    remainingCards, stockNum, lastCard, binaryMask = convertLong2Digits(curState)
    # Method 1: pop card from stock
    if stockNum < 24:
        new1U64State = convertDigits2Long(remainingCards - 1, stockNum + 1, stock[stockNum], binaryMask)
        ret.append((new1U64State, "Pop card from stock, get {}, \ttable = {}".format(stock[stockNum], toString(binaryMask, flattenPeaks))))
    # Method 2: find existing displayed card close to given lastCard.
    parent2Idx = [4, 6, 8, \
                10,11, 13,14, 16,17, \
                19,20,21, 22,23,24, 25,26,27, \
                -1,-1,-1, -1, -1,-1, -1, -1,-1,-1
                ]
    # loop over all possible index
    for idx in range(0, 28):
        checkBitIdx = 27 - idx
        # check if current place contains card
        if (binaryMask >> checkBitIdx) & 0x1:
            readyRemoveCard = flattenPeaks[idx]

            # Find parent bits
            parentCard2Idx = parent2Idx[idx]
            parentCards = (binaryMask >> (27-parentCard2Idx)) & 0x3

            # if exist any card that close to lastCard, and it's parents are removed
            if (abs(lastCard - readyRemoveCard) == 1 or abs(lastCard - readyRemoveCard) == 12) and parentCards == 0:
                # Unset current bit
                newMask = binaryMask ^ (1<<checkBitIdx)
                new2U64State = convertDigits2Long(remainingCards - 1, stockNum, readyRemoveCard, newMask)
                ret.append( (new2U64State, "Remove card {} from peaks, at {}, \ttable = {}".format(
                    readyRemoveCard, 
                    convertArraypos2Layerpos(idx), 
                    toString(newMask, flattenPeaks) )
                ) )
                
    return ret