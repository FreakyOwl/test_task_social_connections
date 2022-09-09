#!/usr/bin/env python3

import json
import networkx as nx
import matplotlib


class APIException(Exception):
    """
    Class for API errors
    """


class Server:
    """
    Class with server methods
    """

    def __init__(self, data_path="journal.json"):
        self.data_path = data_path

    def add_communication(self, time, pair):
        try:
            with open(self.data_path, 'r') as file:
                database = json.load(file)
            if pair[0] not in database["names"] or pair[1] not in database["names"]:
                raise APIException(f"Cannot add communication with an unregistered user")
            journal = database["journal"]
            journal.append({"time": time, "pair": pair})
            database["journal"] = journal
            with open(self.data_path, 'w') as file:
                json.dump(database, file)
        except Exception as exc:
            raise APIException(f"Cannot add communication: {exc}") from exc

    def add_user(self, name):
        try:
            with open(self.data_path, 'r') as file:
                database = json.load(file)
            names = database["names"]
            names.append(name)
            database["names"] = names
            with open(self.data_path, 'w') as file:
                json.dump(database, file)
        except Exception as exc:
            raise APIException(f"Cannot add user: {exc}") from exc

    def make_graph(self):
        try:
            with open(self.data_path, 'r+') as file:
                database = json.load(file)
            journal = database["journal"]
            counters = []
            g = nx.Graph([entry["pair"] for entry in journal])
            nx.draw_networkx(g)
            edges = [set(edge) for edge in nx.edges(g)]
            connections = [set(entry["pair"]) for entry in journal]
            for edge in edges:
                counters.append(connections.count(edge))
            min_inter = min(counters)
            max_inter = max(counters)
            mean_inter = round(sum(counters) / len(counters), 2)
            print(f"Minimal number of communications between two persons: {min_inter}")
            print(f"Maximal number of communications between two persons: {max_inter}")
            print(f"Mean number of communications between two persons: {mean_inter}")
            matplotlib.pyplot.savefig('graph.png')
            return [min_inter, max_inter, mean_inter]
        except Exception as exc:
            raise APIException(f"Cannot make graph: {exc}") from exc
