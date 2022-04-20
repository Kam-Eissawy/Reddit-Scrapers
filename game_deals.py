from slacker import Slacker
import praw
import time

# Slack API token
slack = Slacker('Your Slack API token')

# Reddit API token
reddit = praw.Reddit(
    client_id="Your Client ID",
    client_secret="Your Client Secret",
    user_agent="Your User Agent",
)

# Change this to True if you only want get free games
get_free_only = False

# If get_free_only is False, the script will get games with at least min_discount discount
min_discount = 90

# The subreddit to get game deals from
subreddit = reddit.subreddit('gamedeals')

# posts that were already checked
already_checked = []

for submission in subreddit.new(limit=10):
    
    # check if the post was already checked
    if submission.id not in already_checked:
        already_checked.append(submission.id)
    else:
        continue

    # convert the post's title to lowercase
    title = submission.title.lower()
    
    # check if the game is free and post it to slack
    if '100%' in title or 'free' in title:
        slack.chat.post_message('#free_games', submission.title)
        slack.chat.post_message('#free_games', submission.url)

    # check if the game has a discount and post it to slack
    elif not get_free_only:
        percentages = [str(i) + '%' for i in range(min_discount,101)]
        if any(perc in title for perc in percentages):
            slack.chat.post_message('#discounted_games', submission.title)
            slack.chat.post_message('#discounted_games', submission.url)
    
    # wait for 5 seconds before checking for new posts
    time.sleep(5)
