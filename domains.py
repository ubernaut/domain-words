import os
import whois
import sys

def load_words():
    with open('words.txt', 'r') as f:
        words = [line.strip() for line in f.readlines()]
    print(str(len(words))+" words loaded")
    return words

def load_tlds():
    with open('tlds.txt', 'r') as f:
        tlds = [line.strip() for line in f.readlines()]
    print(str(len(tlds))+" tlds loaded")
    return tlds

def find_domains(words, tlds):
    matches = []
    for word in words:
        for tld in tlds:
            if (word.lower().endswith(tld.lower()) and word != "" and word != tld):
                match = word[:-len(tld)] + "." + tld.lower()
                if(match.startswith(".") == False):
                    matches.append(match)
    return matches

def write_matches_to_file(matches, filename='matches.txt'):
    with open(filename, 'w') as f:
        for match in matches:
            f.write(match + '\n')

def check_domain(domain):
    try:
        # Get the WHOIS information for the domain
        w = whois.whois(domain)
        if w.status == "free":
            return True
        else:
            return False
    except Exception as e:
        print("Error: ", e)
        print(domain+" had an issue")
        return False

def check_available(matches):
    print('checking availability')
    available=[]
    for match in matches:
        if(check_domain(match)):
            print("found "+match+" available!")
            available.append(match)
    return available

if __name__ == '__main__':
    words = load_words()
    tlds = load_tlds()
    matches = find_domains(words, tlds)
    matches = sorted(matches, key=len, reverse=False)  # Sort the matches list by length in descending order
    write_matches_to_file(matches)
    available = check_available(matches)
    write_matches_to_file(available, filename="available.txt")
