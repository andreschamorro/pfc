from queue import Queue
import random
# import os

from card import Card
from datetime import datetime

from tinydb import TinyDB, Query
from tinydb_serialization import Serializer, SerializationMiddleware


class DateTimeSerializer(Serializer):
    OBJ_CLASS = datetime  # The class this serializer handles

    def encode(self, obj):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')

    def decode(self, s):
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')


def open_or_create_db(path):
    """Get a TinyDB database object for the recipy database.
        This opens the DB, creating it if it doesn't exist.
    """
    serialization = SerializationMiddleware()
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')
    # if not os.path.exists(os.path.dirname(path)):
    #     os.mkdir(os.path.dirname(path))
    db = TinyDB(path, storage=serialization)
    return db


def sm2(x: [int], a=6.0, b=-0.8, c=0.28, d=0.02,
        assumed_score=2.5, min_score=1.3, theta=1.0) -> float:
    """
    Returns the number of days until seeing a problem again based on the
    history of answers x to the problem, where the meaning of x is:
    x == 0: Incorrect, Hardest
    x == 1: Incorrect, Hard
    x == 2: Incorrect, Medium
    x == 3: Correct, Medium
    x == 4: Correct, Easy
    x == 5: Correct, Easiest
    @param x The history of answers in the above scoring.
    @param theta When larger, the delays for correct answers will increase.
    """
    assert all(0 <= x_i <= 5 for x_i in x)
    correct = [x_i >= 3 for x_i in x]
    # If you got the last question incorrect, just return 1
    if not correct[-1]:
        return 1.0

    # Calculate the latest consecutive answer streak
    r = 0
    for c_i in reversed(correct):
        if c_i:
            r += 1
        else:
            break

    return a*(max(min_score,
              assumed_score + sum(b+c*x_i+d*x_i*x_i for x_i in x)))**(theta*r)


class Deck:
    """
    A deck contains one or more cards.

    Attributes:
        __cards (list of Card): The cards in the deck.
    """

    def __init__(self, source, table):
        """
        Constructor.

        Args:
            source (str): The path to the deck source file.
        """
        # Create cards from source file
        self.__db = open_or_create_db(source)
        self.__table = self.__db.table(table)

    def __len__(self):
        return self.__cards.qsize()

    def fetch(self):
        db_query = Query()
        self.__cards = Queue()
        for cdict in self.__table.search(db_query.next_time <= datetime.now()):
            # Extract definitions, answers, and hints from the given line
            if cdict:
                self.__cards.put(Card(cdict['question'],
                                      cdict['answer'],
                                      cdict['hint']))
        return self.__cards

    def add(self, card):
        """
        Adds a card onto the bottom of the deck.

        Args:
            card (Card): The card to add to the deck.
        """
        self.__cards.put(card)

    def draw(self):
        """
        Draws a card from the deck.

        The card will be removed once drawn unless manually added back in

        Returns:
            (Card): The card from the top of the deck.
        """
        return self.__cards.get()

    def shuffle(self):
        """
        Shuffles the cards in the deck.
        """
        # Extract cards from queue
        card_list = []
        while not self.__cards.empty():
            card_list.append(self.__cards.get())

        # Shuffle extracted cards
        random.shuffle(card_list)

        # Reinsert cards into queue
        for card in card_list:
            self.__cards.put(card)
