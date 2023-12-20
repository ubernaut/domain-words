import os
import sys
from multiprocessing import Pool

import pandas as pd
from tqdm import tqdm
from whois import whois

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
            print(match)
            if type(match) is tuple:
                f.write(str(match[0])+" "+str(match[1])+"\n")
            else:
                f.write(match + '\n')

# def check_domain(domain):
#     try:
#         # Get the WHOIS information for the domain
#         w = whois.whois(domain)
#         if w.status == "free":
#             return True
#         else:
#             return False
#     except Exception as e:
#         print("Error: ", e)
#         print(domain+" had an issue")
#         return False
def blockPrint():
    sys.stdout = open(os.devnull, "w")


def enablePrint():
    sys.stdout = sys.__stdout__


def check_domain(domain):
    try:
        blockPrint()
        result = whois(domain)
    except:
        return domain, None
    finally:
        enablePrint()
    return domain, result.status

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
    domains = matches

    results = []
    with Pool(processes=32) as pool:  # <-- select here how many processes do you want
        for domain, status in tqdm(
            pool.imap_unordered(check_domain, domains), total=len(domains)
        ):
            results.append((domain, not bool(status)))

    df = pd.DataFrame(results, columns=["domain", "is_free"])
    print(df.drop_duplicates())

    write_matches_to_file(results, filename="results.txt")
