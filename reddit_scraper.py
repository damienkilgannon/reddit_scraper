#!/usr/bin/env python3

import praw
import csv
import uuid
import os

from praw.models import MoreComments


def scrape_comments(path, id, submission_comments, query):
    fields = ['subreddit', 'parent_post', 'created', 'created_utc', 'title', 'text', 'url', 'type']

    comments = []

    for comment in submission_comments:
        if isinstance(comment, MoreComments):
            continue
        if query not in comment.body:
            continue
        comments.append([comment.subreddit, comment.submission, comment.author, comment.created_utc, '', comment.body, comment.permalink, 'comment'])

    print("Number of comments: " + str(len(comments)))

    if not os.path.exists(path):
        os.makedirs(path)

    filename = subreddit + '_' + query + '_' + id + "_comments.csv"

    with open(os.path.join(path, filename), 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(comments)

    return


def scrape(reddit, subreddit, query):
    path = 'data/' + str(uuid.uuid1().int)[:6]

    fields = ['subreddit', 'created', 'created_utc', 'title', 'text', 'url', 'type']

    submissions = []

    for submission in reddit.subreddit(subreddit).search(query, sort='relevance', time_filter='all', limit=None):
        submissions.append([submission.subreddit, submission.author, submission.created_utc, submission.title, submission.selftext, submission.url, 'post'])
        if submission.num_comments > 0:
            scrape_comments(path, submission.id, submission.comments, query)

    print("Number of posts: " + str(len(submissions)))

    if not os.path.exists(path):
        os.makedirs(path)

    filename = subreddit + '_' + query + "_posts.csv"

    with open(os.path.join(path, filename), 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(submissions)

    return

if __name__ == '__main__':
    reddit = praw.Reddit(
        client_id = "j1oQvtLhIBbPkg",
        client_secret = "nsw3AAYc0dOPOZ4h1jsatvJODAmAJA",
        user_agent = "android:com.example.myredditapp:v1.2.3 (by u/kemitche)"
    )

    print('Enter subreddit >>> ', end='')
    subreddit = input()
    print('Enter query >>> ', end='')
    query = input()
    scrape(reddit, subreddit, query)
