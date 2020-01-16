"""
Automated Realtime Conlanging HIErarchy creator
ARCHIE

Author: @solmann; 2019
"""
from models import *


def main():
    print("Welcome to Archie!")
    a = input("Select an option:\n"
              "1. You want to create a new phonology system for your conlang\n"
              "2. You want to setup morphemes for your language")
    if a == "1":
        print("OK, let's get started. ")
        print()


if __name__ == '__main__':
    main()
