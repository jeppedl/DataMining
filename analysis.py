"""
This file is part of the Subreddit Comments Analysis bot library.

Copyright 2014 Jeppe de Lange and Niclas Bach Nielsen

It is intended to be used in conjunction with datafile_plotting.py and
analysis.py for the best result.

License:

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

The Reddit Subreddit Comments Analysis is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY; without even
the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the Reddit Subreddit Comments Analysis library.
If not, see <http://www.gnu.org/licenses/>.
"""
import re
import string

AFINN_FILE = 'word_lists/AFINN-111.txt'
PROFANITY_LIST_FILE = 'word_lists/profanity-list-google.txt'


def reddit_anal(subreddit_com, word1, word2, word3, word4, word5, word6):
    """
    Returns subreddit comments and word count, average sentiment score,
    counted profane words, the average of counted profane words and the
    occurences of the specified words. All based on the comments list.

    Example usage:

    >>> reddit_anal(subreddit_com = 'comments.csv',
                    'money', 'cats', 'dogs', 'love', 'hate', 'kiss')
    """
    # Run through all comments and store them in a list.
    subreddit_comments_list = []
    for comment in subreddit_com:
        subreddit_comments_list.append(comment.body)

    # Clears the list for special characters, for later analysis.
    subreddit_comments_list = map(lambda foo: foo.replace(".", ""), subreddit_comments_list)
    subreddit_comments_list = map(lambda foo: foo.replace(",", ""), subreddit_comments_list)
    subreddit_comments_list = map(lambda foo: foo.replace("!", ""), subreddit_comments_list)
    subreddit_comments_list = map(lambda foo: foo.replace("?", ""), subreddit_comments_list)
    subreddit_comments_list = map(lambda foo: foo.replace("*", ""), subreddit_comments_list)
    subreddit_comments_list = map(lambda foo: foo.replace("'", ""), subreddit_comments_list)
    subreddit_comments_list = map(lambda foo: foo.replace("/", ""), subreddit_comments_list)
    subreddit_comments_list = map(lambda foo: foo.replace("(", ""), subreddit_comments_list)
    subreddit_comments_list = map(lambda foo: foo.replace(")", ""), subreddit_comments_list)

    # Run through the list of profanity and store them in a list.
    profanity_list = []
    with open(PROFANITY_LIST_FILE) as swearword:
        for someword in swearword:
            someword = someword.strip()
            profanity_list.append(someword)

    # Run through the commentlist and count profanity.
    word_count = 0
    profanity_count = 0

    for redcomment in subreddit_comments_list:
        redcomment = redcomment.encode('utf-8')
        for word in redcomment.lower().split():
            word_count += 1
            if word in profanity_list:
                profanity_count += 1

    prof_score = (float(profanity_count)/word_count)*100
    prof_score_list = [prof_score]

    # Use AFINN-111.txt and make a dictionary with words and
    # their coresponding sentiment values.
    afinn = dict(map(lambda (w, s): (w, int(s)), [
        ws.strip().split('\t') for ws in open(AFINN_FILE)]))

    # Convert the list of comments to a string,
    # get sentiment value for each word
    # and calculate an estimated sentimen average.
    afinn_score = 0
    string_comments = ''.join(subreddit_comments_list)
    afinn_score = map(lambda word: afinn.get(word, 0),
                      string_comments.lower().split())

    if afinn_score:
        sentiment_score = float(sum(afinn_score))/len(afinn_score)
    else:
        sentiment_score = 0

    # Convert list to string in order to count the word frequencies.
    stringMyList = ''.join(subreddit_comments_list).encode('utf-8').lower()
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    finalList = regex.sub(' ', stringMyList)
    # del myList, stringMyList
    words = [word1, word2, word3, word4, word5, word6]
    comments = finalList
    prof_wordcount = dict((x, 0) for x in words)
    for w in re.findall(r"\w+", comments):
        if w in prof_wordcount:
            prof_wordcount[w] += 1

    # Change values in dict to percentage:
    # (word frequency/total nr of words)*100
    for key, value in prof_wordcount.items():
        prof_wordcount[key] = (float(value)/word_count)*100

    print "profanity count: " + str(profanity_count)
    print "total words: " + str(word_count)
    print "profscore: " + str(prof_score)
    print "Afinn sentiment avg: " + str(sentiment_score)
    return subreddit_comments_list, word_count, sentiment_score, \
        prof_score_list, profanity_count, prof_score, prof_wordcount
