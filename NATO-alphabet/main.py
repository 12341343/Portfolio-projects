student_dict = {
    "student": ["Angela", "James", "Lily"], 
    "score": [56, 76, 98]
}

import pandas
student_data_frame = pandas.DataFrame(student_dict)


nato_alphabet = "nato_phonetic_alphabet.csv"
nato_alphabet = pandas.read_csv(nato_alphabet)


#TODO 1. Create a dictionary in this format:
letters = {row.letter: row.code for (index, row) in nato_alphabet.iterrows()}

print("Welcome to NATO alphabet")
user_input = input("Type your word: ").upper()
result = [letters[letter] for letter in user_input]
print(result)

