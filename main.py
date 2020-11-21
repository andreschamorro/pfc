import sys
from deck import Deck
from UI.ui import Application

if __name__ == '__main__':
    source = sys.argv[1]
    table = sys.argv[2]

    flash_cards = []

    # Create deck
    deck = Deck(source, table)
    # Fetch
    deck.fetch()
    # Start quizzing
    deck.shuffle()

    app = Application()
    app.deck = deck
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)

    print("""
    Type \"exit\" or \"quit\" to exit,
    type \"hint\" for a hint, or
    type \"skip\" to skip a question.\n""")

    while len(deck) > 0:
        print("Remaining flash cards:", len(deck), "\n")

        card = deck.draw()
        print(card.question())
        answer = input("Answer: ")

        # Check if the answer is a command or actually an answer
        if answer.lower() == "exit" or answer.lower() == "quit":
            sys.exit()
        elif answer.lower() == "hint":
            print(card.hint())
            deck.add(card)
        elif answer.lower() == "skip":
            print()
        else:
            if card.check(answer):
                print("Correct!")
                for ans in card.answer():
                    print(ans)
            else:
                print("Incorrect!")
                for ans in card.answer():
                    print(ans)
                deck.add(card)

    print("Finished!")
