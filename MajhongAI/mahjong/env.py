import json
import logging
import pickle
import os
import numpy as np
from copy import deepcopy
from mahjong.game import Game
from mahjong.snapshot import Snapshot

DEFAULT_CONFIG = {
    'player_num': 4,
    'seed': None
}
class Env(object):
    """
    Mahjong Environment
    """

    def __init__(self, config: dict = None):
        """init config

        Args:
            config (dict, optional): DEFAULT_CONFIG. Defaults to None.
        """
        self.config = config
        if not self.config:
            self.config = DEFAULT_CONFIG
        self.name = 'Mahjong'
        self.seed = config['seed']
        self.game = Game()
        
        self.agents = None
        self.snapshot = None

    def set_agents(self, agents):
        self.agents = agents

    def reset(self):
        self.game.init_game(self.config)
        self.snapshot = self.game.new_game()

    def next(self):
        self.snapshot = self.game.next(self.snapshot)

    def save(self):
        self.game.save()

    def decide(self):
        for agent in self.agents:
            agent.decide(self.snapshot, self.game.round.trace, self.game.dealer.deck) # self.game.round.trace to get the trace , self.game.dealer.deck to get deck

    def load(self, uuid:str, step:int):
        """
        加载历史对局
        Args:
            uuid (str): 局id
            step (int): 步骤
        """
        if not os.path.exists(f'logs/{uuid}_history.pickle') \
            or not os.path.exists(f'logs/{uuid}_trace.pickle') \
            or not os.path.exists(f'logs/{uuid}_seed.pickle'):
            print("wrong uuid")
        
        with open(f'logs/{uuid}_seed.pickle', 'rb') as handle:
            self.config = pickle.load(handle)
        self.game.init_game(self.config)
        self.snapshot = self.game.load_game(uuid, step)

    def step_back(self,step:int=1):
        self.snapshot = self.game.step_back(step)

    def run(self):
        # history = []
        if self.config["show_log"]:
            self.snapshot.print()
        while not self.snapshot.is_finish:

            self.decide()
            # if self.config["show_log"]:
            #     self.snapshot.print_decides()
            self.next()
        # if self.config["show_log"]:
        #     self.snapshot.print()
        if self.config["seed"]:
            self.save()
