import requests
import os
import json
import time

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")

def get_tweet_list():
    with open(os.path.dirname(os.path.abspath(__file__)) + "/citations.json", "r") as f:
        x = f.read()
    tweet_dicts = json.loads(x)
    tweet_ids = []
    for d in tweet_dicts:
        resp_id = list(d.keys())[0]
        for dic in d[resp_id]:
            tweet_ids.append(dic['tweet_id'])
    return tweet_ids

def create_url(tweet_id):
    tweet_fields = "tweet.fields=created_at,text"
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


def main():
    bearer_token = auth()
    tweets = []
    for tweet_id in get_tweet_list():
        url = create_url(tweet_id)
        headers = create_headers(bearer_token)
        json_response = connect_to_endpoint(url, headers)
        try:
            text = json_response['data'][0]['text']
            created = json_response['data'][0]['created_at']
            tweets.append({'id': tweet_id, 'text': text, 'created_at': created})
        except:
            continue
    json_object = json.dumps(tweets, indent = 4)
    with open(os.path.dirname(os.path.abspath(__file__)) + "/tweet_text.json", "w") as f:
        f.write(json_object)

if __name__ == "__main__":
    main()