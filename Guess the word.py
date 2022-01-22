import requests
import json

def findVowels(word):
    contains = []
    returning = ''
    for vowel in ['a','e','i','o','u']:
        if word.find(vowel) > 0:
            contains.append(vowel)
    if len(contains) == 0:
        returning = 'None'
    else:
        for i in contains:
            returning += i + ' '
    return returning.strip()

headers = requests.utils.default_headers()

headers.update(
    {
        'User-Agent': 'My User Agent 1.0',
    }
)


print("Welcome to the game!")
print("In this game, you will need to guess the word.")
print("You will get 5 hints: ")
print("1. Number of letters")
print("2. The meaning of the word")
print("3. The vowels in the word")
print("4. Letter that the word starts with")
print("5. Letter that the word ends with")
print()

answer = ""
noDefinition = {'title': 'No Definitions Found', 'message': "Sorry pal, we couldn't find definitions for the word you were looking for.", 'resolution': 'You can try the search again at later time or head to the web instead.'}
continueGame = True
while(continueGame):
    listOfWords = json.loads(requests.get("https://random-word-api.herokuapp.com/word?number=10", headers=headers).text)
    sameQuestion = True
    count = 0
    while(sameQuestion):
        word = listOfWords[count]
        responseDict = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+word, headers=headers)
        dic = json.loads(responseDict.text)
        if dic != noDefinition:
            
            meaning = dic[0]['meanings'][0]['definitions'][0]['definition']
            print("Hints:")
            print("1. The word has " + str(len(word)) + " letters.")
            print("2. The meaning of the word is: " + meaning)
            print("3. The word contain the vowels: " + findVowels(word))
            print("4. The word starts with: " + word[0])
            print("5. The word ends with: " + word[-1])
            print("This won't be printed : " + word)
            while(answer != word):
                answer = input("Please input your guess (type /q to quit, /s to skip): ")
                if answer == '/q':
                    continueGame = False
                    sameQuestion = False
                    print("The answer is " + word)
                    print()
                    break
                elif answer == '/s':
                    sameQuestion = False
                    print("The answer is " + word)
                    print()
                    break
                elif answer.lower() == word:
                    print("Congratulations! Let's move on to the next word!")
                    print()
                    sameQuestion = False
                    break
                else:
                    print("Please try again.")
        count += 1

print("The end.")
