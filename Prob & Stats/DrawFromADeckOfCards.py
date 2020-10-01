# imports 
import random
import sys 

# heart, diamon,spade club
deck_of_cards = { 
0:['a', 'heart', 'red' ], 1:['2', 'heart', 'red' ], 2:['3', 'heart', 'red' ], 3:['4', 'heart', 'red' ], 4:['5', 'heart', 'red' ], 5:['6', 'heart', 'red' ],
6:['7', 'heart', 'red' ], 7:['8', 'heart', 'red' ], 8:['9', 'heart', 'red' ], 9:['10', 'heart', 'red' ], 10:['j', 'heart', 'red' ], 11:['q', 'heart', 'red' ],
12:['k', 'heart', 'red' ],
13:['a', 'diamond', 'red' ], 14:['2', 'diamond', 'red' ], 15:['3', 'diamond', 'red' ], 16:['4', 'diamond', 'red' ], 17:['5', 'diamond', 'red' ],
18:['6', 'diamond', 'red' ], 19:['7', 'diamond', 'red' ], 20:['8', 'diamond', 'red' ], 21:['9', 'diamond', 'red' ], 22:['10', 'diamond', 'red' ],
23:['j', 'diamond', 'red' ], 24:['q', 'diamond', 'red' ], 25:['k', 'diamond', 'red' ],
26:['a', 'spade', 'black' ], 27:['2', 'spade', 'black' ], 28:['3', 'spade', 'black' ], 29:['4', 'spade', 'black' ], 30:['5', 'spade', 'black' ],
31:['6', 'spade', 'black' ], 32:['7', 'spade', 'black' ], 33:['8', 'spade', 'black' ], 34:['9', 'spade', 'black' ], 35:['10', 'spade', 'black' ],
36:['j', 'spade', 'black' ], 37:['q', 'spade', 'black' ], 38:['k', 'spade', 'black' ],
39:['a', 'club', 'black' ], 40:['2', 'club', 'black' ], 41:['3', 'club', 'black' ], 42:['4', 'club', 'black' ], 43:['5', 'club', 'black' ],
44:['6', 'club', 'black' ], 45:['7', 'club', 'black' ], 46:['8', 'club', 'black' ], 47:['9', 'club', 'black' ], 48:['10', 'club', 'black' ],
49:['j', 'club', 'black' ], 50:['q', 'club', 'black' ], 51:['k', 'club', 'black' ]
}


# total arguments 
n = len(sys.argv) 

if n > 1:
    Input=sys.argv[1]
else:
    Input = input("Input: ")

number_of_trials = 10 ** 6
Face = Input.split(',')[0].lower()
Type = Input.split(',')[1].lower()
Colour = Input.split(',')[2].lower()
# #print(Face)
# #print(Type)
# #print(Colour)


if Type == 'h': Type = 'heart'
elif Type == 'd': Type = 'diamond'
elif Type == 's': Type = 'spade'
elif Type == 'c': Type = 'club'
elif Type == 'none': pass
else: print("Incorrect type, enter h/d/s/c")
# #print(Face)
# #print(Type)
# #print(Colour)

# exit()
deck_of_cards_outcomes = [0 for x in range(0,52)]
#print(deck_of_cards_outcomes)
count=0
while count < number_of_trials:
    # head - 0 ; tail - 1
    i = random.randint(0,51)
    deck_of_cards_outcomes[i] += 1
    count += 1
#print(deck_of_cards_outcomes)
#print([(x/number_of_trials)*100 for x in deck_of_cards_outcomes])

result = 0
if Face == "none" and Type == "none" and Colour == "none":
    #print("i am here 01")
    result=0
elif Face != "none" and Type == "none" and Colour == "none":
    #print("i am here 02")
    for x in deck_of_cards:
        if Face == deck_of_cards[x][0]:
            result += (deck_of_cards_outcomes[x]/number_of_trials)*100
elif Face == "none" and Type != "none" and Colour == "none":
    #print("i am here 03")
    for x in deck_of_cards:
        #print("{} - {}".format(Type,deck_of_cards[x][1]))
        if Type == deck_of_cards[x][1]:
            result += (deck_of_cards_outcomes[x]/number_of_trials)*100
elif Face == "none" and Type == "none" and Colour != "none":
    #print("i am here 04")
    for x in deck_of_cards:
        if Colour == deck_of_cards[x][2]:
            result += (deck_of_cards_outcomes[x]/number_of_trials)*100
elif Face != "none" and Type != "none" and Colour == "none":
    #print("i am here 05")
    for x in deck_of_cards:
        if Face == deck_of_cards[x][0] and Type == deck_of_cards[x][1]:
            result += (deck_of_cards_outcomes[x]/number_of_trials)*100
elif Face != "none" and Type == "none" and Colour != "none":
    #print("i am here 06")
    for x in deck_of_cards:
        if Face == deck_of_cards[x][0] and Colour == deck_of_cards[x][2]:
            #print("{} - {}, {} - {}".format(Face,deck_of_cards[x][0],Colour,deck_of_cards[x][2]))
            result += (deck_of_cards_outcomes[x]/number_of_trials)*100
elif Face == "none" and Type != "none" and Colour != "none":
    #print("i am here 07")
    for x in deck_of_cards:
        if Type == deck_of_cards[x][1] and Colour == deck_of_cards[x][2]:
            result += (deck_of_cards_outcomes[x]/number_of_trials)*100
elif Face != "none" and Type != "none" and Colour != "none":
    #print("i am here 08")
    for x in deck_of_cards:
        if Face == deck_of_cards[x][0] and Type == deck_of_cards[x][1] and Colour == deck_of_cards[x][2]:
            result += (deck_of_cards_outcomes[x]/number_of_trials)*100
            
            

print("probability to get Face={}, Type={}, Colour={} is {}".format(Face,Type,Colour,result))


    
    
