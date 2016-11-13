import requests
r = requests.post('http://localhost:80/api/games/practice', data={'devkey': "58268225b642e9d038e35c52", 'username': 'charlieyou'}) # search for new game
json = r.json()
print(json)
gameID = json['gameID']
playerID = json['playerID']
print(gameID)
print(playerID)
input = ' '
while input != '':
	input = raw_input('input move: ')
        r = requests.post('http://localhost:80/api/games/submit/' + gameID, data={'playerID': playerID, 'move': input, 'devkey': "58268225b642e9d038e35c52"}); # submit sample move
	json = r.json()
	print(json)
