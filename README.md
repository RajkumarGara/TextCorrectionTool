# TextCorrectionTool
It cleans and extracts words to form dictionary from a given text file (warofworlds file is used as dataset). Using this dictionary to spell check the input text and suggestions are given for the misspelled words using the minimum edit distance.

## Execution steps
1. call process_regex(path_to_text_file); input file will be any text file (warofworlds.txt is choosen)
2. call normalize_text(path_to_text_file); input file will be the output file from step1 (regex.txt)
3. call spell_checker(input_file); input file will be the output file from step2 (dictionary.txt)
