import sys
from datetime import datetime
from deck import open_or_create_db


if __name__ == '__main__':

    source = input("Database source path:")
    db = open_or_create_db(source)
    table_name = input("Table name:")
    table = db.table('test')

    print("""
    Type \"exit\" or \"quit\" to exit
    type \"insert\" for a insert a new card, \n""")

    while True:

        command = input(":")

        # Check if the answer is a command or actually an answer
        if command.lower() == "exit" or command.lower() == "quit":
            sys.exit()
        elif command.lower() == "insert":
            question = input("Question: ")
            answer = input("Answer: ")
            hint = input("hint: ")
            card = {'next_time': datetime.now(),
                    'question': question, 'answer': answer, 'hint': hint}

            table.insert(card)
        else:
            print("Type a valid command")

    print("Finished!")
