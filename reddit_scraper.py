#!/usr/bin/env python3

import praw
import csv
import uuid
import os

from praw.models import MoreComments


def scrape(path, iter, query, type, id=None):
    fields = ['subreddit', 'author', 'created_utc', 'title', 'text', 'url', 'type', 'parent_post']
    parent_post = None
    items = []

    for item in iter:
        if isinstance(item, MoreComments):
            continue
        try:
            body = item.body
            if query not in body:
                continue
        except AttributeError:
            body = ""
        try:
            title = item.title
        except AttributeError:
            title = ""

        items.append([item.subreddit, item.author, item.created_utc, title, body, item.permalink, type, id])

        try:
            if item.num_comments > 0:
                scrape(path, item.comments, query, "comment", id=item.id)
        except AttributeError:
            continue

    if not os.path.exists(path):
        os.makedirs(path)

    if id:
        filename = str(id) + "_" + type + ".csv"
    else:
        filename = type + ".csv"

    with open(os.path.join(path, filename), 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(items)


if __name__ == '__main__':
    reddit = praw.Reddit(
        client_id = os.getenv('CLIENT_ID'),
        client_secret = os.getenv('CLIENT_SECRET'),
        user_agent = os.getenv('USER_AGENT', "android:com.example.myredditapp:v1.2.3 (by u/kemitche)")
    )

    uuid = str(uuid.uuid1().int)[:6]
    print("Enter query term >>> ", end="")
    query = input()
    print("Enter space seperated list of subreddits >>> ", end="")
    subreddits = input().split()

    print("Scraping the follow subreddits for posts and comments matching the query term.")
    print("Subreddits: ", end="")
    print(subreddits)
    print("Query: ", end="")
    print(query)
    print("Scrape UUID: ", end="")
    print(uuid)
    print("Output path: ", end="")
    print("data/" + uuid + "/<subreddit>/<query>")

    for subreddit in subreddits:
        path = 'data/' + uuid + '/' + subreddit + '/' + query
        iter = reddit.subreddit(subreddit).search(query, sort='relevance', time_filter='all', limit=None)
        scrape(path, iter, query, "post")
