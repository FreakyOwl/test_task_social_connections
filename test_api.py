#!/usr/bin/env python3

import os
import json
import datetime
import random
import pytest

import api

JOURNAL_PATH = "journal.json"


def generate_database():
    journal = []
    names = ["Антон Иванов", "Татьяна Петрова", "киса зая", "City Hunter 87", "Дашуня Волкова"]
    number_of_entries = 10

    for i in range(0, number_of_entries):
        new_entry = {"time": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"), "pair": random.sample(names, 2)}
        journal.append(new_entry)

    database = {"names": names, "journal": journal}
    with open(JOURNAL_PATH, 'w') as file:
        json.dump(database, file)


class TestApi:

    def test_add_user(self):
        generate_database()
        server = api.Server()
        server.add_user("Марат Борисов")
        with open(JOURNAL_PATH, 'r+') as file:
            database = json.load(file)
        names = database["names"]
        assert names == ["Антон Иванов", "Татьяна Петрова", "киса зая", "City Hunter 87", "Дашуня Волкова", "Марат Борисов"]

    def test_add_communication(self):
        generate_database()
        server = api.Server()
        new_communication = {"time": "09/09/2022 19:19:59", "pair": ["Антон Иванов", "Татьяна Петрова"]}
        server.add_communication(new_communication["time"], new_communication["pair"])
        with open(JOURNAL_PATH, 'r+') as file:
            database = json.load(file)
        journal = database["journal"]
        assert journal[len(journal)-1] == new_communication
        with pytest.raises(api.APIException):
            server.add_communication(new_communication["time"], ["Антон Иванов", "Марат Борисов"])

    def test_make_graph(self):
        generate_database()
        server = api.Server()
        server.make_graph()
        assert os.path.isfile("graph.png")

    def teardown(self):
        try:
            os.remove(JOURNAL_PATH)
        except Exception:
            pass
