import random
import time
import math
import copy

from bot import Bot


class MCTSBot(Bot):
    def __init__(self, state, player_id, sim_time=10):
        self.player_id = player_id
        self.sim_time = sim_time

        self.state_node = {}

    def get_move(self, state):
        print repr(state)
        state = copy.deepcopy(state)
        move = self.mcts(state)

        return move

    def mcts(self, state):
        results = {}

        root = None
        if state in self.state_node:
            root = self.state_node[state]
        else:
            n_children = len(state.legal_moves())
            if not state.completed and not n_children:
                n_children = 1

            root = Node(state, None, n_children)

        root.parent = None

        n_simulations = 0
        start = time.time()
        while time.time() - start < self.sim_time and root.moves_unfinished:
            node = self.tree_policy(root)
            result = self.simulate(node.state)
            self.back_prop(node, result)
            n_simulations += 1

        for child in root.children:
            wins, plays = child.get_wins_plays()
            position = child.move
            results[position] = (wins, plays)

        for position in sorted(results, key=lambda x: results[x][1]):
            print '{}: ({}/{})'.format(
                    position, results[position][0], results[position][1])
        print '{} simulations performed.'.format(n_simulations)

        return self.best_action(root)

    def tree_policy(self, root):
        current_node = root

        while root.moves_unfinished:
            legal_moves = current_node.state.legal_moves()
            if not legal_moves:
                if current_node.state.completed:
                    current_node.propogate_completion()
                    return current_node
                else:
                    next_state = current_node.state.next_state('')
                    next_node = Node(next_state, None, 1)
                    current_node.add_child(next_node)
                    self.state_node[next_state] = next_node
                    current_node = next_node
                    continue
            elif len(current_node.children) < len(legal_moves):
                unexpanded = [
                        move for move in legal_moves
                        if move not in current_node.moves_expanded]

                move = random.choice(unexpanded)
                state = current_node.state.next_state(move)
                child = Node(state, move, len(legal_moves))
                current_node.add_child(child)
                self.state_node[state] = child
                return child
            else:
                current_node = self.best_child(current_node)
        return current_node

    def best_child(self, node):
        enemy_turn = (node.state.move_iterator != self.player_id)
        C = 0   # exploration value
        values = {}
        for child in node.children:
            wins, plays = child.get_wins_plays()
            if enemy_turn:
                wins = plays - wins
            _, parent_plays = node.get_wins_plays()
            values[child] = (float(wins) / plays)\
                + C * math.sqrt(2 * math.log(parent_plays) / plays)

        best_choice = max(values, key=values.get)
        return best_choice

    def simulate(self, state):
        REWARD = 1
        LOSS = 0
        # print self.player_id
        while not state.completed:
            # print repr(state)
            # print state.bomb_map
            # print state.player.id
            moves = state.legal_moves()
            move = random.choice(moves)
            # print move
            state = state.next_state(move)

        if state.winner() == self.player_id:
            # print 'win!'
            return REWARD
        else:
            # print 'loss!'
            return LOSS

    @staticmethod
    def best_action(node):
        max_plays = -float('inf')
        max_wins = -float('inf')
        best_actions = []
        for child in node.children:
            wins, plays = child.get_wins_plays()
            if plays > max_plays:
                max_plays = plays
                best_actions = [child.move]
                max_wins = wins
            elif plays == max_plays:
                if wins > max_wins:
                    max_wins = wins
                    best_actions = [child.move]
                elif wins == max_wins:
                    best_actions.append(child.move)

        return random.choice(best_actions)

    @staticmethod
    def back_prop(node, delta):
        while node.parent:
            node.plays += 1
            node.wins += delta
            node = node.parent

        node.plays += 1
        node.wins += delta


class Node:
    def __init__(self, state, move, n_children):
        self.state = state
        self.plays = 0
        self.wins = 0
        self.children = []
        self.parent = None
        self.moves_expanded = set()
        self.moves_unfinished = n_children

        self.move = move

    def propogate_completion(self):
        if not self.parent:
            return

        if self.moves_unfinished:
            self.moves_unfinished -= 1

        self.parent.propogate_completion()

    def add_child(self, node):
        self.children.append(node)
        self.moves_expanded.add(node.move)
        node.parent = self

    def has_children(self):
        return len(self.children) > 0

    def get_wins_plays(self):
        return self.wins, self.plays

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return 'move: {} wins: {} plays: {}'.format(
                self.move, self.wins, self.plays)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.state == other.state
