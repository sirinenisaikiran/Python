deck_of_cards = { 
0:['A', 'heart' ], 1:['2', 'heart' ], 2:['3', 'heart' ], 3:['4', 'heart' ], 4:['5', 'heart' ], 5:['6', 'heart' ],
6:['7', 'heart' ], 7:['8', 'heart' ], 8:['9', 'heart' ], 9:['10', 'heart' ], 10:['J', 'heart' ], 11:['Q', 'heart' ],
12:['K', 'heart' ],
13:['A', 'diamond' ], 14:['2', 'diamond' ], 15:['3', 'diamond' ], 16:['4', 'diamond' ], 17:['5', 'diamond' ],
18:['6', 'diamond' ], 19:['7', 'diamond' ], 20:['8', 'diamond' ], 21:['9', 'diamond' ], 22:['10', 'diamond' ],
23:['J', 'diamond' ], 24:['Q', 'diamond' ], 25:['K', 'diamond' ],
26:['A', 'spade' ], 27:['2', 'spade' ], 28:['3', 'spade' ], 29:['4', 'spade' ], 30:['5', 'spade' ],
31:['6', 'spade' ], 32:['7', 'spade' ], 33:['8', 'spade' ], 34:['9', 'spade' ], 35:['10', 'spade' ],
36:['J', 'spade' ], 37:['Q', 'spade' ], 38:['K', 'spade' ],
39:['A', 'club' ], 40:['2', 'club' ], 41:['3', 'club' ], 42:['4', 'club' ], 43:['5', 'club' ],
44:['6', 'club' ], 45:['7', 'club' ], 46:['8', 'club' ], 47:['9', 'club' ], 48:['10', 'club' ],
49:['J', 'club' ], 50:['Q', 'club' ], 51:['K', 'club' ]
}
cout = 0
for x in deck_of_cards:
    if deck_of_cards[x][1] == 'diamond':
        print(deck_of_cards[x])
        cout += 1
print(cout)