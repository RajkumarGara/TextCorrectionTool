import re


def process_regex(path_to_text_file):
    print("Processing file...")
    # opens the warofworlds.txt file from the given path in read mode
    with open(path_to_text_file, 'r', encoding="UTF-8") as warofworlds:
        text = warofworlds.read()
        # British english words to American english words conversion (from 'ou' to 'o')
        text = re.sub(r'([a-zA-Z])([a-zA-Z])([a-su-zA-Z])our(ed|ing|.s|er.s)?(\s|\n)', r'\1\2\3or\4\5', text)

    # List of Titles to be converted
    titles = ["Dr.", "Mr.", "Ms.", "Mrs."]
    titles_expanded = ["Doctor", "Mister", "Miss", "Misses"]

    # checking each title from titles in text
    for index, title in enumerate(titles):
        if title in text:
            # Substitute abbreviate titles with the expanded title in the text
            text = re.sub(title, titles_expanded[index], text)

    # creates regex.txt in write mode
    with open("regex.txt", 'w', encoding="UTF-8") as regex_file:
        for line in text:
            # write content from text to regex_file
            regex_file.write(line)
    print('Output stored to “regex.txt”')


def normalize_text(path_to_text_file):
    print("Normalizing text...")
    # opens the regex text file from the given path in read mode
    with open(path_to_text_file, 'r', encoding="UTF-8") as regex_file:
        text = regex_file.read()

    # Converts all words to lower case
    text = text.lower()

    # insert space for hyphen"-"
    text = re.sub(r'([a-z]*)[—-]', r'\1 ', text)

    # remove some stop words
    # remove words with 'll, 't, 've such as I'll, aren't, you've...
    text = re.sub(r"[a-z]*['’](ll|t|ve|re|d)", r"", text)

    # remove 's from the words having 's such as there's, it's,...
    text = re.sub(r"([a-z]*)['’]s", r"\1", text)

    # adding letter g to words with movin', goin'...
    text = re.sub(r"([a-z]*n)['’]", r"\1g", text)

    # remove special characters, punctuations and numbers
    text = re.sub(r'[^a-z\n\s]', r'', text)

    # removing the single and double letters like "i, a, an, at,..."
    text = re.sub(r'\b\w{1,2}\b', r'', text)

    # remove websites that starts with www
    text = re.sub(r'www[a-z]+', r'', text)

    # remove roman numbers like iv, xii,...
    text = re.sub(r'\s[ivx]+\s', r'', text)

    # stemming (removing suffixes like ed, ing, s)
    # removing suffix 'ed', 'ing' from doing, cited,....
    # text = re.sub(r'([a-z]{3})(ed|ing)(\s)',r'\1\3', text) # skipped owed for not to do weed
    # replacing ed with '' results some meaning less words like "com" from "coming", "cit" from "cited"

    # split the text into words each in new line and sort it in alphabetical order
    text = sorted(text.split())

    # remove repeated words
    unique_text = []
    for word in text:
        if word not in unique_text:
            unique_text.append(word)

    # creates dictionary.txt in write mode
    with open("dictionary.txt", 'w', encoding="UTF-8") as dictionary_file:
        for word in unique_text:
            # write content from unique_text to 'dictionary.txt' file
            dictionary_file.write("%s \n" % word)
    print('Output stored to “dictionary.txt”')


def edit_distance(word1, word2):
    # initializing width, height and declaring distance table
    w, h = len(word1) + 1, len(word2) + 1
    dist_table = [[0 for i in range(h)] for j in range(w)]

    # initializing the edit_distance table
    for i in range(0, w):
        for j in range(0, h):
            dist_table[i][0] = i
            dist_table[0][j] = j

    # edit distance table algorithm
    for i in range(1, w):
        for j in range(1, h):
            if word1[i - 1] == word2[j - 1]:
                dist_table[i][j] = min(dist_table[i - 1][j] + 1, dist_table[i][j - 1] + 1, dist_table[i - 1][j - 1] + 0)
            else:
                dist_table[i][j] = min(dist_table[i - 1][j] + 1, dist_table[i][j - 1] + 1, dist_table[i - 1][j - 1] + 2)

    # print the edit distance table
    # print(dist_table)

    # edit distance value
    distance = dist_table[w - 1][h - 1]
    return distance


def spell_checker(input_file):
    print('Welcome to the spell checker!')
    print('Please enter a text to check spelling or enter quit to exit the program.')

    # waiting for the input text
    text = input('Enter text to be checked: ')

    # Converts all words to lower case
    text = text.lower()

    while (text != 'quit'):

        # insert space for hyphen"-"
        text = re.sub(r'([a-z]*)[-]', r'\1 ', text)

        # insert space for special characters, punctuations and numbers
        text = re.sub(r'[^a-z\n\s]', r' ', text)

        # split the text into words each in new line
        text = text.split()

        # remove repeated words
        unique_text = []
        for word in text:
            if word not in unique_text:
                unique_text.append(word)

        # opens the dictionary_file from the given path in read mode
        with open(input_file, 'r', encoding="UTF-8") as dictionary_file:
            # converts the dictionary_file to dictionary list
            dictionary = re.findall(r'([a-z]+)\s', dictionary_file.read())

        # collect misspelling words
        misspellings = []
        for word in unique_text:
            if word not in dictionary:
                misspellings.append(word)

        # if there are no misspellings
        if not misspellings:
            print("No misspellings detected!")

        # if there are some misspellings
        else:
            print("Misspelling - Suggestion")

            # going through each and every wrong_word in misspellings
            for wrong_word in misspellings:

                # initializing min_edit_distance_val with maximum value
                # to make sure edit_distance < min_value
                min_edit_distance_val = 100
                corrected_word = []

                # calculating edit_distance between wrong_word and each dictionary word
                for dictionary_word in dictionary:
                    edit_distance_val = edit_distance(wrong_word, dictionary_word)

                    # getting minimum edit_distance values
                    if (edit_distance_val < min_edit_distance_val):
                        min_edit_distance_val = edit_distance_val

                        # updating the corrected_word with the nearest dictionary_word
                        corrected_word = dictionary_word

                # print the wrong word and final corrected word
                print(wrong_word + " - " + corrected_word)

        # waiting for the input text
        text = input('Enter text to be checked: ')

        # Converts all words to lower case
        text = text.lower()

    print('Goodbye!')