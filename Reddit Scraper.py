import praw
import sqlite3 as sql
import string
import re
import itertools
from fractions import Fraction
r = praw.Reddit('A script to gather vendor reviews from /r/DarkNetMarkets for a university project. User: MrJBlack')
scraperdb = sql.connect('Darkmarkets1.db')
c = scraperdb.cursor()

markets = ['agora', 'hydra', 'tpm', 'pirate', 'the pirate market', '1776', 'andromeda', 'topix', 'outlaw', 'bazaar', 'cloud', 'cloud9', 'c9', 'cannabis road', 'cr', 'blue sky', 'bsm', 'tom', 'evolution', 'evo', 'alpaca', 'dream', 'silk street', 'silk', 'pandora', 'middle earth', 'ramp', 'majestic garden', 'tmg', 'silk road', 'sr2', 'private']
drugs = {'cocaine':['coke', 'cocaine'], 'cannabis':['cannabis', 'marijuana', 'weed', 'hash', 'brownies', 'brownie','wax', 'white widow', 'bruce banner', 'og', 'kush', 'bubble gum', 'tickle', 'ak-47', 'green', 'diesel', 'skunk', 'girl scout cookies', 'sour', 'haze', 'purple', 'blueberry', 'bubba', 'bud'], 'lsd': ['lsd', 'blotter', 'blotter', 'acid', 'dots', 'tabs', 'tab', 'stamp', 'stamps'], 'mdma':['mdma', 'molly', 'e', 'mandy'], 'crack':['crack'], 'meth':['meth'], 'mushrooms':['mushrooms', 'shrooms'], 'dmt':['dmt'], 'amphetamin':['amphetamin', 'speed', 'paste'], 'heroin':['heroin', 'smack'], 'ketamine':['ket', 'ketamine', 'mxe'], 'misc':['etizolam', 'ghb', 'gbl', 'diazepam']}
drugs2 = list(itertools.chain(*drugs.values()))

def marketCheck(s):
    ns = ''.join(ch for ch in s if ch not in string.punctuation)
    ns = ns.lower().split(' ')
    ls = []
    for w in ns:
        if w in markets:
            ls.append(w)
    return ', '.join(set(ls))
    

def whichDrug(s):
    s = ''.join(ch for ch in s if ch not in string.punctuation)
    s = s.lower().split(' ')
    ls = []
    for w in s:
        if w in drugs2:
            for key in drugs.keys():
                if w in drugs[key]:
                    ls.append(key)
    return ', '.join(set(ls))
    
def nameCheck(s):
    ns = set(re.split('\W+', s.lower()))
    ns = [x for x in ns if not re.match(r'(\d+\w+)|(\d)', x)]
    misc = ['gram', 'mg', 'g', 'ug', 'ml', 's', 'l', 'oz', 'and', 'scam', 'scammer', 'scammed', 'waiting', 'exit', 'an', 'a', 'shipping', 'reviews', 'review', 'vendor', 'on', 'still', 'free', 'sample', 'the', 'market', 'marketplace', 'from', 'finalize', 'early', 'fe', 'pics', 'delays', 'delay', 'order', 'dose']
    stp = [markets, drugs2, misc]
    for i in stp:
        for j in i:
            if j in ns:
                ns.remove(j)
    return ', '.join([i for i in ns if i != ''])
    
def qSearch(s, q):
    for j in re.split(r'\n', s):
        if q in j and re.findall(r'\d+/\d+', j) != []:
            return re.findall(r'\d/\d', j)[0]

def textget(x, s):
    '''
    x is the limit on how many submissions it should check, None for first time and lower subsiquently.
    s is the subreddit we wish to scrape.
    This fuction checks submissons to a subreddit against our detection rules. If one fits out criteria
    and has not been logged prevously it saves the text to a document.
    To Do:
        Adapt for rules fuctions.
    '''
    submissions = r.get_subreddit(s)
    resultsDoc = open(('/home/john/Dropbox/cryptomarkets/data/'+ s +'Results.TXT'), 'a')
    count = 0
    try:
        c.execute('select id from Darknetmarkets_sub')
        done = c.fechall()
    except:
        done = []
    for i in submissions.get_new(limit= x):
        if i.permalink not in done:
            if 'vendor review' in i.title.lower() or 'Vendor Review' == i.link_flair_text:
                resultsDoc.write((i.title + '\n' + i.selftext + '\n' + '##########\n##########\n##########\n\n').encode('utf-8'))
                count += 1
                done.append(i.permalink)
            elif 'vendor complaint' in i.title.lower() or 'Vendor Complaint' == i.link_flair_text:
                resultsDoc.write((i.title + '\n' + i.selftext + '\n' + '##########\n##########\n##########\n\n').encode('utf-8'))
                count += 1
                done.append(i.permalink)         
    resultsDoc.close()    
    return 'Added ' + str(count) +', for a total of ' + str(len(done))
    

        
def subScrape(limit=None, sub='darknetmarkets'):
    submissions = r.get_subreddit(sub)
    count = 0
    try:
        c.execute('select id from Darknetmarkets_sub')
        done = c.fechall()
    except:
        done = []
    for i in submissions.get_new(limit= limit):
        row = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if i.id not in done:
            if 'Vendor Review' == i.link_flair_text or 'Vendor Complaint' == i.link_flair_text:
                count += 1
                title = i.title.lower()
                things = ['vendor review', 'vendor complaint','[]', '()']
                for t in things:
                    title = title.replace(t, '')
                row[0] = i.url
                row[1] = i.id
                row[2] = i.link_flair_text
                row[3] = i.title
                row[4] = str(i.author)
                row[5] = i.score
                row[6] = i.num_comments
                row[7] = marketCheck(title)
                row[8] = nameCheck(title)
                row[9] = whichDrug(title)
                row[10] = i.selftext
                row[11] = qSearch(i.selftext.lower(), 'communication')
                row[12] = float(Fraction(qSearch(i.selftext.lower(), 'communication') or 0))
                row[13] = qSearch(i.selftext.lower(), 'shipping')
                row[14] = float(Fraction(qSearch(i.selftext.lower(), 'shipping') or 0))
                row[15] = qSearch(i.selftext.lower(), 'stealth')
                row[16] = float(Fraction(qSearch(i.selftext.lower(), 'stealth') or 0))
                row[17] = qSearch(i.selftext.lower(), 'quality')
                row[18] = float(Fraction(qSearch(i.selftext.lower(), 'quality') or 0))
                row[19] = qSearch(i.selftext.lower(), 'price')
                row[20] = float(Fraction(qSearch(i.selftext.lower(), 'price') or 0))
                c.execute('INSERT INTO Darknetmarkets_sub VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row)
    scraperdb.commit()
    return count
    
print subScrape()
                
            
