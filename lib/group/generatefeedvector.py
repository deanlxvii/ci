import feedparser
import re


def getwords(html):
    # Remove all HTML tags
    txt = re.compile(r'<[^>]+>').sub('',html)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # Convert to lowercase
    return [word.lower() for word in words if word !='']

# Returns title and dictionary of word counts for an RSS feed
def getwordcounts(url):
    #parse the feed
    d = feedparser.parse(url)
    wc = dict()

    # Loop over all entries
    for e in d.entries:
        if 'summary' in e: summary=e.summary
        else: summary=e.description

        # Extract a list of words
        words = getwords(e.title+' '+summary)
        for word in words:
            wc.setdefault(word,0)
            wc[word]+=1
        return d.feed.title,wc


apcount = dict()
wordcounts = dict()
feedlist = list()
for feedurl in file('feedlist.txt'):
    try:
        title, wc = getwordcounts(feedurl)
        feedlist.append(feedurl)
        print 'processing >> ' + feedurl
        wordcounts[title]=wc
        for word,count in wc.items():
            apcount.setdefault(word,0)
            if count > 1:
                apcount[word]+=1
    except:
        print "skipped : "+feedurl


wordlist = list()
for w, bc in apcount.items():
    frac=float(bc)/len(feedlist)
    if frac>0.1 and frac<0.5: wordlist.append(w)


out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog, wc in wordcounts.items():
    try:
        print 'writing >> ' + blog
        out.write(blog)
        for word in wordlist:
            try:
                if word in wc: out.write('\t%d' % wc[word])
                else: out.write('\t0')
            except:
                'error >> ' + blog + ' >>> ' + word
        out.write('\n')
    except:
        print 'skipped write >>> ' + blog
