import requests
import os
import json
import time

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")

def get_tweet_list():
    old_ids = get_previous_data()
    with open(os.path.dirname(os.path.abspath(__file__)) + "/citations.json", "r") as f:
        x = f.read()
    tweet_dicts = json.loads(x)
    tweet_ids = []
    group_of_100 = []
    for d in tweet_dicts:
        resp_id = list(d.keys())[0]
        for dic in d[resp_id]:
            if dic['tweet_id'] not in old_ids:
                group_of_100.append(dic['tweet_id'])
            if len(group_of_100) == 100:
                tweet_ids.append(group_of_100)
                group_of_100 = []
    return tweet_ids

def create_url(tweet_id):
    tweet_fields = "tweet.fields=created_at,text,source"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = f"ids={tweet_id}"
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_previous_data():
    with open(os.path.dirname(os.path.abspath(__file__)) + "/tweet_text.json", "r") as f:
        y = f.read()
    return [item['id'] for item in json.loads(y)]


def main():
    bearer_token = auth()
    previous = get_previous_data()
    tweets = []
    counter = 0
    for group in get_tweet_list():
        if counter ==  179:
            with open(os.path.dirname(os.path.abspath(__file__)) + "/tweet_text.json", "r") as f:
                x = f.read()
            prev_tweets = json.loads(x) + tweets
            my_json = json.dumps(prev_tweets, indent = 4)
            with open(os.path.dirname(os.path.abspath(__file__)) + "/tweet_text.json", "w") as f:
                f.write(my_json)
            tweets = []
            counter = 0
            time.sleep(900)
        counter += 1
        url = create_url(','.join(group))
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        try:
            for tweet in json_response['data']:
                try:
                    text = tweet['text']
                    created = tweet['created_at']
                    tweet_id = tweet['id']
                    source = tweet['source']
                    tweets.append({'id': tweet_id, 'text': text, 'created_at': created, 'source': source})
                except:
                    continue
        except:
            continue
    with open(os.path.dirname(os.path.abspath(__file__)) + "/tweet_text.json", "r") as f:
        x = f.read()
    prev_tweets = json.loads(x) + tweets
    my_json = json.dumps(prev_tweets, indent = 4)
    with open(os.path.dirname(os.path.abspath(__file__)) + "/tweet_text.json", "w") as f:
        f.write(my_json)

if __name__ == "__main__":
    main()