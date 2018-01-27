#!/usr/bin/env python
from bottle import route, run
import random

# Global games.
games = []

attack_total = 15
malus_total = 5
recover_value = 50

class Card:
    """Has attack points (attack_total in sum) and a malus of one value.
    """
    attack_points = [
        {'name': 'cpu', 'value': 0},
        {'name': 'bandwidth', 'value': 0},
        {'name': 'route', 'value': 0}
    ]

    malus_points = [
        {'name': 'cpu', 'value': 0},
        {'name': 'bandwidth', 'value': 0},
        {'name': 'route', 'value': 0}
    ]

    def __init__(self):
        """Generates random values for the usages and which malus you get.
        """
        global attack_total
        random_values = []
        random_values.append(
            random.randint(0, attack_total)
        )
        random_values.append(
            random.randint(0, attack_total - random_values[0])
        )
        random_values.append(
            random.randint(
                0, attack_total - random_values[0] - random_values[1]
            )
        )

        random_values = random.shuffle(random_values)

        attack_points[0]['value'] = random_values[0]
        attack_points[1]['value'] = random_values[1]
        attack_points[2]['value'] = random_values[2]

        global malus_total
        index = randint(0, 2)
        malus_points[index]['value'] = malus_total

class Player:
    """Holds all information that belongs to a single player.
    """
    name = ''
    transmission = 0

    cpu_usage = 50
    bandwidth_usage = 50
    route_usage = 50

    cards = []

    current_action = None
    current_opponent = None
    current_card = None

    def __init__(self, username):
        self.name = username
        self.cards = [Card(), Card(), Card()]

    def select_action(self, action, opponent=None, card=None):
        if self.current_action is None:
            self.current_action = attack
            self.opponent = opponent
            self.current_card = card

    def incoming_attack(self, card):
        """If a player gets attacked with a card, add values to player stats.
        """
        self.cpu_usage = max(
            0, self.cpu_usage - card.attack_points[0]['value']
        )
        self.bandwidth_usage = max(
            0, self.bandwidth_usage - card.attack_points[1]['value']
        )
        self.route_usage = max(
            0, self.route_usage - card.attack_points[2]['value']
        )

    def outgoing_attack(self, card):
        """Substracts the malus points from an own attack.
        """
        self.cpu_usage = max(
            0, self.cpu_usage - card.malus_points[0]['value']
        )
        self.bandwidth_usage = max(
            0, self.bandwidth_usage - card.malus_points[1]['value']
        )
        self.route_usage = max(
            0, self.route_usage - card.malus_points[2]['value']
        )

    def recover(self, stat):
        """Add recover value to a stat.
        """
        global recover_value
        if stat == 'cpu':
            self.cpu_usage += recover_value
        else if stat == 'bandwidth':
            self.bandwidth += recover_value
        else if stat == 'route_usage':
            self.route_usage += recover_value

    def add_transmission(self):
        """Calculates the additional upload for the next round
        and add it to the total transmission.
        """
        transmission_delta = min(
            self.cpu_usage,
            self.bandwidth_usage,
            self.route_usage
        )
        self.transmission += transmission_delta

    def next_round(self):
        """Add transmission points, reset action and replace card, if one was
        used.
        """
        self.add_transmission()

        if self.current_action == 'attack':
            self.cards.remove(self.current_card)
            self.cards.append(Card())

        self.current_card = None
        self.opponent = None

        self.current_action = None

# For URL http://localhost:8080/join
@post('<group_name>/join')
def action_join(group_name):
    # Get username from request.
    username = request.json.username
    if join_possible:
        return { status: "OK" }
    else:
        return { status: "FAIL" }

# For URL http://localhost:8080/start_game
@post('<group_name>/start_game')
def action_start_game(group_name):
    # Disable possibility to join game
    global join_possible
    join_possible = False
    # Get stats for user from request.
    # TODO
    return { status: "OK" }

# Main function
if __name__ == '__main__':
    run(host='localhost', port=8080)
