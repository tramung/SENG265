#Author: Tram Ung
#!/usr/bin/env python3
import re
class Kwic:
    def __init__(self, excluded, lines):
        self.excluded = excluded
        self.index_lines = lines
        self.formatted_list = []

#output() called by kwic3.py
    def output(self):
        keys, sentences = Kwic.capitalise_it(self)
        keys_sorted, values_sorted = Kwic.sort_it(self, keys, sentences)
        Kwic.format_it(self, keys_sorted, values_sorted)
        return self.formatted_list

#capitalise words
    def capitalise_it(self):
        capped_list = []
        key_list = []
        number_list = []
        for phrase in self.index_lines:
            result_sentence = ""
            word_list = phrase.strip().split()
            for word in word_list:
                if word.lower() not in self.excluded:
                    s = re.sub(word, word.upper(), word).strip() #sub word with capped word
                    result_sentence = " ".join(word_list[:word_list.index(word)]) + " " + s + " " + " ".join(word_list[word_list.index(word)+1:]) #contruct sentence
                    key_list.append(s)
                else:
                    continue
                capped_list.append(result_sentence.strip())
        return key_list, capped_list

#sort list using tuple
    def sort_it(self, key_list, capped_list):
        zipped_tuple = tuple(zip(key_list, capped_list)) #zip lists into tuple
        sorted_tuple = sorted(zipped_tuple, key=lambda tup: tup[0]) #sort tuple
        sorted_keys = [key[0] for key in sorted_tuple] #unzip into list of sorted capped words
        sorted_values = [phrase[1] for phrase in sorted_tuple] #unzip into list of sorted sentences
        return sorted_keys, sorted_values

#format it using regex
    def format_it(self, sorted_keys, sorted_values):
        counter = 0
        CONST_SPACE_AFTER = 30 #space after
        CONST_SPACE_BEFORE = 20 #space before
        for phrase in sorted_values:
             s = r'((^|\s).{0,'+ str(CONST_SPACE_BEFORE) + r'})' + sorted_keys[counter] + r'(($|\s)(.{0,' + str(CONST_SPACE_AFTER - len(sorted_keys[counter])) + '})($|\s))'
             matchobj = re.search(s, phrase)
             if matchobj:#if match is found
                 line = matchobj.group(0).strip()
                 space = CONST_SPACE_AFTER - line.find(sorted_keys[counter]) - 1
                 self.formatted_list.append(" "*space + line)
             else:#if match not found
                 print("None")
             counter += 1
