#!/usr/bin/env python3
"""CrackPython: a simple terminal-based Python learning program."""

from __future__ import annotations

import json
from pathlib import Path

PROGRESS_FILE = Path.home() / ".crackpython_progress.json"

LESSONS = [
    {
        "title": "Getting started: print and comments",
        "topic": "Output and comments",
        "explanation": (
            "Python runs instructions from top to bottom. Use print() to show text "
            "or values. A comment starts with # and is ignored by Python."
        ),
        "example": 'print("Hello, Python!")\n# This is a comment\nprint(2 + 3)',
        "question": "Which function displays a message in the terminal?",
        "choices": ["show()", "print()", "write()"],
        "answer": 1,
        "practice": "Write a line of Python that prints your name.",
        "hint": 'Try: print("your name")',
        "solution": 'print("Ada Lovelace")',
    },
    {
        "title": "Variables and basic types",
        "topic": "Variables, strings, numbers, and booleans",
        "explanation": (
            "A variable is a name for a value. Use = to assign a value. Common "
            "types include str (text), int (whole numbers), float (decimals), "
            "and bool (True or False)."
        ),
        "example": 'name = "Sam"\nage = 12\nis_learning = True\nprint(name, age, is_learning)',
        "question": "Which value is a boolean?",
        "choices": ['"True"', "True", "1.0"],
        "answer": 1,
        "practice": "Create a variable called city containing the name of a city, then print it.",
        "hint": 'Assign text in quotes, for example: city = "Tokyo"',
        "solution": 'city = "Tokyo"\nprint(city)',
    },
    {
        "title": "Working with strings",
        "topic": "Text and string methods",
        "explanation": (
            "Strings are text wrapped in quotes. Join strings with +, or use an "
            "f-string to insert values: f\"Hello, {name}!\". Methods like .upper() "
            "create useful transformed strings."
        ),
        "example": 'name = "Riley"\nmessage = f"Hello, {name}!"\nprint(message.upper())',
        "question": "What prefix makes a string an f-string?",
        "choices": ["s", "f", "text"],
        "answer": 1,
        "practice": "Make an f-string that greets a person using a name variable.",
        "hint": 'Use a string like f"Hi, {name}!"',
        "solution": 'name = "Alex"\nprint(f"Hi, {name}!")',
    },
    {
        "title": "Lists and indexing",
        "topic": "Collections of values",
        "explanation": (
            "A list stores multiple values in order, using square brackets. Indexes start at 0, "
            "so items[0] is the first item. Use append() to add an item."
        ),
        "example": 'fruits = ["apple", "banana"]\nfruits.append("pear")\nprint(fruits[0])\nprint(len(fruits))',
        "question": "What is the index of the first item in a Python list?",
        "choices": ["0", "1", "-1"],
        "answer": 0,
        "practice": "Create a list of three favorite foods and print the second one.",
        "hint": "The second item has index 1.",
        "solution": 'foods = ["pasta", "tacos", "soup"]\nprint(foods[1])',
    },
    {
        "title": "Making decisions with if",
        "topic": "Conditions and comparisons",
        "explanation": (
            "Use if to run code only when a condition is true. Add elif for another condition "
            "and else for the fallback. Indentation defines which lines belong to each branch."
        ),
        "example": 'temperature = 18\nif temperature > 25:\n    print("It is warm")\nelse:\n    print("It is cool")',
        "question": "Which keyword provides a fallback when an if condition is false?",
        "choices": ["otherwise", "else", "default"],
        "answer": 1,
        "practice": "Check whether a number variable is positive and print a suitable message.",
        "hint": "Compare the number to 0 with > and use an else branch.",
        "solution": 'number = 7\nif number > 0:\n    print("Positive")\nelse:\n    print("Not positive")',
    },
    {
        "title": "Repeating work with loops",
        "topic": "For and while loops",
        "explanation": (
            "A for loop visits each item in a sequence. range(5) produces 0, 1, 2, 3, 4. "
            "A while loop repeats as long as its condition stays true."
        ),
        "example": 'for number in range(1, 4):\n    print(number)\n\nfor color in ["red", "blue"]:\n    print(color)',
        "question": "How many numbers does range(4) produce?",
        "choices": ["3", "4", "5"],
        "answer": 1,
        "practice": "Use a for loop to print the numbers 1 through 5.",
        "hint": "range(1, 6) includes 1 and stops before 6.",
        "solution": "for number in range(1, 6):\n    print(number)",
    },
    {
        "title": "Functions",
        "topic": "Reusable blocks of code",
        "explanation": (
            "Define a function with def, followed by its name and parentheses. Parameters let a function "
            "receive values. return sends a result back to the caller."
        ),
        "example": 'def greet(name):\n    return f"Hello, {name}!"\n\nmessage = greet("Jo")\nprint(message)',
        "question": "Which keyword sends a result back from a function?",
        "choices": ["yield", "return", "send"],
        "answer": 1,
        "practice": "Write a function named double that returns a number multiplied by 2.",
        "hint": "Start with def double(number): and return number * 2.",
        "solution": "def double(number):\n    return number * 2\n\nprint(double(4))",
    },
    {
        "title": "Dictionaries and a mini project",
        "topic": "Key-value data and putting it together",
        "explanation": (
            "A dictionary stores key-value pairs inside braces. Look up a value with its key, "
            "such as person['name']. You can combine variables, conditions, and collections to make a small program."
        ),
        "example": 'person = {"name": "Kai", "favorite_language": "Python"}\nprint(person["name"])\nperson["level"] = "beginner"\nprint(person)',
        "question": "How do you look up a dictionary value?",
        "choices": ["By its key", "By its position only", "With a list index"],
        "answer": 0,
        "practice": "Create a dictionary for a book with title and author, then print the title.",
        "hint": 'Use keys such as "title" and "author".',
        "solution": 'book = {"title": "The Hobbit", "author": "J.R.R. Tolkien"}\nprint(book["title"])',
    },
]


def load_progress():
    try:
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {
                "completed": [i for i in data.get("completed", []) if isinstance(i, int)],
                "best_scores": data.get("best_scores", {}) if isinstance(data.get("best_scores", {}), dict) else {},
            }
    except (OSError, json.JSONDecodeError):
        pass
    return {"completed": [], "best_scores": {}}


def save_progress(progress):
    try:
        PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"\nCouldn't save progress: {exc}")


def show_lesson(index):
    lesson = LESSONS[index]
    print(f"\nLesson {index + 1}: {lesson['title']}\n{'-' * (len(lesson['title']) + 11)}")
    print(f"\n{lesson['explanation']}\n\nExample:\n")
    for line in lesson["example"].splitlines():
        print(f"  {line}")
    print(f"\nPractice: {lesson['practice']}")
    choice = input("Show a hint, solution, or continue? [h/s/Enter]: ").strip().lower()
    if choice == "h":
        print(f"Hint: {lesson['hint']}")
    elif choice == "s":
        print("\nOne possible solution:\n")
        for line in lesson["solution"].splitlines():
            print(f"  {line}")
    print("\nMark this lesson complete? [y/N]: ", end="")
    return input().strip().lower() == "y"


def take_quiz(index, progress):
    lesson = LESSONS[index]
    print(f"\nQuick quiz — {lesson['topic']}\n")
    print(lesson["question"])
    for number, choice in enumerate(lesson["choices"], start=1):
        print(f"  {number}. {choice}")
    while True:
        response = input("Your answer (number): ").strip()
        if response.isdigit() and 1 <= int(response) <= len(lesson["choices"]):
            break
        print("Please enter one of the listed numbers.")
    correct = int(response) - 1 == lesson["answer"]
    if correct:
        print("Correct! Nice work.")
    else:
        correct_choice = lesson["choices"][lesson["answer"]]
        print(f"Not quite. The answer is {correct_choice!r}. Keep practicing!")
    previous = progress["best_scores"].get(str(index), 0)
    progress["best_scores"][str(index)] = max(previous, int(correct))
    return correct


def show_progress(progress):
    completed = set(progress["completed"])
    print("\nYour learning progress")
    print("-" * 23)
    for index, lesson in enumerate(LESSONS):
        mark = "✓" if index in completed else " "
        score = "quiz passed" if progress["best_scores"].get(str(index)) == 1 else "quiz not passed yet"
        print(f"[{mark}] {index + 1}. {lesson['title']} — {score}")
    print(f"\nCompleted: {len(completed & set(range(len(LESSONS))))}/{len(LESSONS)} lessons")
    input("\nPress Enter to continue...")


def main():
    progress = load_progress()
    print("=" * 45)
    print("  Welcome to CrackPython: Learn Python! 🐍")
    print("=" * 45)
    while True:
        completed = set(progress["completed"])
        next_lesson = next((i for i in range(len(LESSONS)) if i not in completed), 0)
        print("\nMenu")
        print(f"  1. Start / continue (Lesson {next_lesson + 1})")
        print("  2. Choose a lesson")
        print("  3. View progress")
        print("  4. Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            index = next_lesson
        elif choice == "2":
            print("\nLessons:")
            for i, lesson in enumerate(LESSONS, start=1):
                print(f"  {i}. {lesson['title']}")
            selected = input("Lesson number (or Enter to cancel): ").strip()
            if not selected:
                continue
            if not selected.isdigit() or not 1 <= int(selected) <= len(LESSONS):
                print("Please choose a valid lesson number.")
                continue
            index = int(selected) - 1
        elif choice == "3":
            show_progress(progress)
            continue
        elif choice == "4":
            print("\nGreat work today. Keep practicing Python — see you next time!")
            break
        else:
            print("Please choose 1, 2, 3, or 4.")
            continue

        if show_lesson(index):
            if index not in progress["completed"]:
                progress["completed"].append(index)
            save_progress(progress)
        take_quiz(index, progress)
        save_progress(progress)


if __name__ == "__main__":
    main()
