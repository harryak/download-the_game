#!/usr/bin/env python
from bottle import app, get, post, route, run, request, response, redirect, static_file, view
import random

app().catchall = False

# Global games.
games = {}

attack_total = 15
malus_total = 5
recover_value = 50

class Game:
    players = {}
    current_round = 0
    game_running = False

    def __init__(self):
        """Initializes a game.
        """
        pass

    def join_possible(self):
        return not self.game_running and len(self.players) < 8

    def add_player(self, new_player):
        """Adds a player, if possible.
        """
        for username, player in self.players.items():
            if username == new_player.name:
                return False

        self.players[new_player.name] = new_player
        return True

    def start_game(self):
        """Starts a game.
        """
        if len(self.players) < 2 or len(self.players) > 8:
            return False
        else:
            self.game_running = True
            return True

    def next_round(self):
        """Calculates all actions and the next round.
        """
        for username, player in self.players.items():
            if player.current_action == "attack":
                if player.current_opponent is not None \
                        and player.current_card is not None:
                    player.current_opponent.incoming_attack(
                        player.current_card
                    )
                    player.outgoing_attack(
                        player.current_card
                    )

        for username, player in self.players.items():
            if player.current_action == "recover":
                player.recover()

        for username, player in self.players.items():
            player.next_round()

        self.current_round += 1

    def stat(self):
        return {
            "players": len(self.players),
            "round": self.current_round,
            "running": self.game_running
        }

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
        random.seed()

        global attack_total
        random_values = []
        random_values.append(
            random.randint(0, attack_total)
        )
        random_values.append(
            random.randint(0, attack_total - random_values[0])
        )
        random_values.append(
            attack_total - random_values[0] - random_values[1]
        )

        random.shuffle(random_values)

        self.attack_points[0]['value'] = random_values[0]
        self.attack_points[1]['value'] = random_values[1]
        self.attack_points[2]['value'] = random_values[2]

        global malus_total
        index = random.randint(0, 2)
        self.malus_points[index]['value'] = malus_total

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
        random.seed(username)
        card1 = Card()
        card2 = Card()
        card3 = Card()
        self.cards = [card1, card2, card3]

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
        elif stat == 'bandwidth':
            self.bandwidth += recover_value
        elif stat == 'route_usage':
            self.route_usage += recover_value

    def add_transmission(self):
        """Calculates the additional download for the next round
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

# For URL http://localhost:12345/join
@post('/<group_name>/join')
def action_join(group_name):
    response.content_type = "application/json"

    global games
    if not group_name in games:
        games[group_name] = Game()

    this_game = games[group_name]

    # Get username from request.
    if this_game.join_possible():
        username = request.json["username"]
        new_player = Player(username)

        if this_game.add_player(new_player):
            return { "status": "OK" }
        else:
            return { "status": "FAIL", "message": "Player already exists." }
    else:
        return { "status": "FAIL", "message": "Game is already running, it's not possible to join now." }

# For URL http://localhost:12345/start_game
@post('/<group_name>/start_game')
def action_start_game(group_name):
    response.content_type = "application/json"

    global games
    if not group_name in games:
        return { "status": "FAIL", "message": "Game was not found." }

    this_game = games[group_name]

    if this_game.start_game():
        return { "status": "OK" }
    else:
        return { "status": "FAIL", "message": "Game is not ready yet." }

@get('/<group_name>/status')
def action_stat(group_name):
    response.content_type = "application/json"

    global games
    if not group_name in games:
        return { "status": "FAIL", "message": "Game was not found." }

    this_game = games[group_name]

    return this_game.stat()

@get('/<group_name>')
def action_redirect(group_name):
    redirect("/")

@get('/<group_name>/game')
@view('index')
def overview(group_name):
    username = request.query["username"]

    global games
    if not group_name in games:
        redirect("/")

    if not games[group_name].game_running:
        redirect("/")

    this_game = games[group_name]
    return {
        "username": username,
        "players": this_game.players
    }

@route('/css/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root="./views/css")
@route('/img/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root="./views/img")
@route('/js/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root="./views/js")

@route('/<group_name>/css/<filepath:path>')
def server_static(group_name, filepath):
    return static_file(filepath, root="./views/css")
@route('/<group_name>/img/<filepath:path>')
def server_static(group_name, filepath):
    return static_file(filepath, root="./views/img")
@route('/<group_name>/js/<filepath:path>')
def server_static(group_name, filepath):
    return static_file(filepath, root="./views/js")

# The main page
@route('/')
@view('new_game')
def index():
    return dict()

# waiting page
@get('/<group_name>/wait')
@view('wait')
def action_wait(group_name):
    global games
    if not group_name in games:
        redirect("/")
    
    username = request.query["username"]
    return { "username": username }

# Main function
if __name__ == '__main__':
    run(host='0.0.0.0', port=80)
