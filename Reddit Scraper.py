import praw

r = praw.Reddit('A script to gather vendor reviews from /r/DarkNetMarkets for a university project. User: MrJBlack')
submissions = r.get_subreddit('darknetmarkets')
count = 0
done = []
resultsDoc = open(('C:\Users\JKiely\Google Drive\Reddit Scraper\Results.TXT'), 'a')
doneDoc = open(('C:\Users\JKiely\Google Drive\Reddit Scraper\Done.TXT'), 'a+')

for h in doneDoc.readlines():
    done.append(h)

for i in submissions.get_new(limit= None):
    if i.id not in done:
        if 'vendor review' in i.title.lower() or 'Vendor Review' == i.link_flair_text:
            resultsDoc.write((i.title + '\n' + i.selftext + '\n' + '##########\n##########\n##########\n\n').encode('utf-8'))
            count += 1
            done.append(i.id)
        elif 'vendor complaint' in i.title.lower() or 'Vendor Complaint' == i.link_flair_text:
            resultsDoc.write((i.title + '\n' + i.selftext + '\n' + '##########\n##########\n##########\n\n').encode('utf-8'))
            count += 1
            done.append(i.id)

for j in done:
    doneDoc.write(j + '\n')
    
resultsDoc.close()
doneDoc.close()
print 'Added ' + str(count) +', for a total of ' + str(len(done))
