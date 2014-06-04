#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
import trie_program
import database
import codecs
import operator
import time

BRITCH_DICT = []
DEATH_DICT = []

xmlTemplateStart = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE cesAna SYSTEM "xcesAnaIPI.dtd">
<chunkList xmlns:xlink="http://www.w3.org/1999/xlink"> <chunk>
  <sentence>"""
xmlTemplateEnd = """</sentence>
 </chunk>
</chunkList>"""
xmlTemplate = """<tok>
    <orth>%s</orth>
    <lex></lex>
</tok>"""


class Sentence:
    def __init__(self, sentence):
        self.tokens = self.tokenize(sentence)
        self.named_entities = self.ner()
        self.lemmas = self.lemmatize(sentence)
        print "Zdanie zostało rozpoznane."

    def tokenize(self, input):
        proc = subprocess.Popen("cd psi-toolkit/build; echo " + input + " | psi-pipe tokenize; cd ../..;", shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        return [line.decode("UTF-8").strip() for line in proc.stdout]

    def lemmatize(self, input):
        proc = subprocess.Popen("cd psi-toolkit/build; echo " + input + " | psi-pipe read-text ! tokenize ! lemmatize --lang pl ! write simple --tags lemma; cd ../..;", shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        return [line.decode("UTF-8").strip() for line in proc.stdout]
        # return [u'jaka|jaki', u'być', u'data', u'począć|poczęcie', u'Karol|Karola', u'Wojtyła']

    def ner(self):
        f = codecs.open('sentence.xml', "w", "utf-8")
        f.write(self.getXMLSentence())
        f.close()
        proc = subprocess.Popen("liner2.3/liner2.sh pipe -ini ./liner2-models-fat-pack/config-muc-fast.ini -i ccl -f sentence.xml -o tuples", shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        return [line.decode("UTF-8").split(",") for line in proc.stdout]
        # return [[u'(20', u'32', u'PER', u'"Karola Wojtyły")\n']]

    def getXMLSentence(self):
        result = xmlTemplateStart
        for t in self.tokens:
            result = result + xmlTemplate%t
        result = result + xmlTemplateEnd
        return result

    def __str__(self):
        return "Tokens: " + str(self.tokens) + "\nNamed Entities: " + str(self.named_entities) + "\nLemmas: " + str(self.lemmas) + "\n"

class Question:
    def __init__(self, name=None, birth=None, death=None):
        self.name = name
        self.birth = birth
        self.death = death
        print "Pytanie zostało rozpoznane."

def recognizeQuestion(sentence):
    global BRITCH_DICT, DEATH_DICT
    person = ""

    for ne in sentence.named_entities:
        if ne[2] == "PER":
            person = ne[3][1:-3]

    if not person:
        print("Brak nazwiska osoby w pytaniu!") 
        return Question()

    # print("Recognized person: " + person + "\n")

    lemmas = [lm for l in sentence.lemmas for lm in l.split("|")]
  
    birth = True if [val for val in lemmas if val in BRITCH_DICT] else False 
    death = True if [val for val in lemmas if val in DEATH_DICT] else False

    return Question(person, birth, death)

def answerQuestion(question):
    if not question.name:
        return

    print "Szukam odpowiedzi..."
    databaseMatches = trie_program.search(question.name, 10)
    databaseMatches.sort(key=operator.itemgetter(1))

    answers = []
    for db in database.getDatabaseDict():
        if db['name'] in databaseMatches[0]:
            answers.append(db)

    if len(answers) == 0:
        print "Nie znalazłem żadnej odpowiedzi.."
        return

    for answer in answers:
        print "Osoba: ", answer['name']
        if question.birth:
            print "Data urodzenia: ", answer['birth']
        if question.death:
            print "Data śmierci: ", answer['death']

def initDicts():
    global BRITCH_DICT, DEATH_DICT
    f = codecs.open("brith-dict.txt", encoding='utf-8')
    BRITCH_DICT = [l.strip() for l in f.readlines()]
    f.close()

    f = codecs.open("death-dict.txt", encoding='utf-8')
    DEATH_DICT = [l.strip() for l in f.readlines()]
    f.close()

    db = database.getDatabaseDict()
    trie_program.initDict(db)

def runQA(input):
    start = time.time()
    answerQuestion(recognizeQuestion(Sentence(input)))
    end = time.time()
    print "Czas odpowiedzi %g s" % (end - start)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", help="Input question which program should answer")
    parser.add_argument("--i", help="Run program in interactive mode", action="store_true")
    args = parser.parse_args()

    print "Wczytuje słowniki..."
    initDicts() 

    print "Program jest gotowy do działania..."
    if args.i:
        print "Wpisz exit() aby zatrzymać program."
        while True:
            print "Pytanie:"
            s = raw_input()
            if "exit()" in s:
                exit()
            runQA(s)
    else:
        runQA(args.q)