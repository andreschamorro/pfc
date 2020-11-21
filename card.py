
class Card:
    """
    A card contains a definition and a list of answers that correspond with it.
    Cards can optionally contain hints.

    Attributes:
        __answer (list of str): A list of possible answers for the card.
        __question (str):      The question for the card.
        __hint (str, optional):  The hint associated with the definition.
    """

    def __init__(self, answer, question, hint=None):
        """
        Constructor.
        Args:
            answer (list of str): A list of possible answers for the card.
            question (str):      The question/definition for the card.
            hint (str, optional):  The hint associated with the definition.
        """
        self.__answer = answer
        self.__question = question
        self.__hint = hint

    def check(self, attempt):
        """
        Determines if the given answer is correct.
        Args:
            answer (str): The answer to check.
        Returns:
            (bool): True if the answer is correct and false otherwise.
        """
        for ans in self.__answer.split(','):
            if attempt.lower() == ans.lower():
                return True

    def answer(self):
        """
            Displays the answer(s) of the card.
        """
        return self.__answer

    def question(self):
        """
            Displays the card question.
        """
        return self.__question

    def hint(self):
        """
            Displays the card hint, if available.
        """
        return self.__hint
