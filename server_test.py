import time
import requests
import random


devkey = '582651d63c0cc0ed06f9da1d'
username = 'charlieyou'

r = requests.post('http://aicomp.io/api/games/practice',
        data={'devkey': devkey, 'username': username})
json = r.json()

gameID = json['gameID']
playerID = json['playerID']

possibleMoves = ['mu', 'ml', 'mr', 'md', 'tu', 'tl', 'tr', 'td', 'b', '', 'op',
        'bp', 'buy_count', 'buy_range', 'buy_pierce', 'buy_block']

output = {'state': 'in progress'}
times = []
while output['state'] != 'complete':
    randomInt = random.randint(0, len(possibleMoves) - 1)
    start = time.time()
    r = requests.post('http://aicomp.io/api/games/submit/' + gameID,
            data={'playerID': playerID, 'move': possibleMoves[randomInt],
            'devkey': devkey})

    end = time.time()
    times.append(end - start)

    json = r.json()
    output = json
    try:
        print output['state']
    except:
        print output
        break

print str(float(sum(times)) / len(times))
