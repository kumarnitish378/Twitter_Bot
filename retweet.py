import tweepy
from time import sleep
from datetime import datetime
import sys
from termcolor import colored

cout = 0
def create_api():
    file_check = False
    file_name = "auth2.txt"
    global user, cout
    try:
        file = open(file_name, 'r')
        file_check = True
        data = file.readlines()
        file.close()
        if len(data) < 4:
            abc = open(file_name, 'w')
            abc.write("")
            abc.close()
            file_check = False
    except:
        file = open(file_name, 'w')
        file_check = False
        file.close()
    
    if file_check:
        file = open(file_name, 'r')
        cre = file.readlines()
        if len(cre) > 0:
            consumer_key = cre[0].replace("\n", '')
            consumer_secret = cre[1].replace("\n", '')
            access_token = cre[2].replace("\n", '')
            access_token_secret = cre[3].replace("\n", '')
            
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth, wait_on_rate_limit=True,
                             wait_on_rate_limit_notify=True)
            try:
                user = api.me()
                api.verify_credentials()
                b = auth.get_username()
                print(b)
                print("Account Verified")
            except tweepy.TweepError as error:
                print("Error creating API")
                abc = open(file_name, 'w')
                abc.write("")
                abc.close()
                print(error)
                cout = cout+1
                create_api()
            print("API created")
            return api
        else:
            print("Please Enter Vailed Credential")
    else:
        print("Please enter All Credential")
        consumer_key = input("consumer_key >> ")
        consumer_secret = input("consumer_secret >> ")
        access_token = input("access_token >> ")
        access_token_secret = input("access_token_secret >> ")
        file = open(file_name, 'w')
        file.write(consumer_key)
        file.write("\n")
        file.write(consumer_secret)
        file.write("\n")
        file.write(access_token)
        file.write("\n")
        file.write(access_token_secret)
        file.close()
        cout = cout + 1
        if cout == 3:
            print("Try Again")
            exit(0)
        else:
            create_api()
        
api = create_api()
# user = api.me()

def trend_topic():
    try:
        trend_result = api.trends_place(1)
        for trends in trend_result[0]["trends"]:
            print(trends["name"])
        return True
    except tweepy.TweepError as ter:
        print(ter.reason)
        print("Failed")
        return False


def follow_follower(num=10):
    try:
        for follower in tweepy.Cursor(api.followers).items(num):
            if not follower.following:
                follower.follow()
            else:
                pass
        return True
    except tweepy.TweepError as ffer:
        print(ffer.reason)
        print("Failed")
        

def follow_someone(name="realpython"):
    try:
        api.create_friendship(name)
        print("Successull")
        return True
    except tweepy.TweepError as fer:
        print(fer.reason)
        print("Failed")
        return False


def user_details(name="twitter"):
    '''
    :param name: Screen Nmae
    :return: True or False
    '''
    try:
        you = api.get_user(name)
        print("User Name: {}".format(you.name))
        print("User Descrition: {}".format(you.description))
        print("User location: {}".format(you.location))
        print("Last 20 Followers: ")
        for fl in you.followers():
            print(fl.name)
        return True
    except tweepy.TweepError as uer:
        print(uer.reason)
        print("Eror")
        return False
    pass


def verify():
    try:
        api.verify_credentials()
        print("Authentication OK")
        return True
    except tweepy.TweepError as ver:
        print("Error during authentication")
        print(ver.reason)
        return False

# print(user)
def user_data():
    print("User name: {}".format(user.screen_name))
    print("Loaction: {}".format(user.location))
    print("Description: {}".format(user.description))
    print("Total Likes; {}".format(user.favourites_count))

tweet = tweepy.Cursor(api.search)

def follow(number=10, gf=30):
    '''
    :param number: number of follow operation
    :param gf: criteria
    :return: follower name or error message
    '''
    count = 0
    for follower in tweepy.Cursor(api.followers).items(number):
        try:
            if follower.friends_count > gf:
                follower.follow()
                count = count + 1
                print(follower.screen_name)
        except tweepy.TweepError as er:
            print(er.reason)
    return  count
    

def like(tag="hello", number=10):
    ''''
    :argument tag, number-of_likes
    '''
    print((datetime.now()))
    for likes in tweepy.Cursor(api.search, q=tag).items(number):
        try:
            twee_id = dict(likes._json)["id"]
            tweet_text = dict(likes._json)["text"]
            print("Id: {}".format(twee_id))
            print("text: {}".format(tweet_text))
            if True:
                likes.favorite()
                print("Tweet Likes")
        except tweepy.TweepError as r:
            print(r.reason)
        print("--------------------------------")
    sleep(1)
    pass


def retweet(hashtag, id_list=[], nm=20):
    '''
    :param hashtag: tag to find
    :param id_list: list of Id
    :return: message or error
    '''
    while True:
        f = open("tweet_id.txt", 'a')
        print(datetime.now())
        for tweet in tweepy.Cursor(api.search, q=hashtag).items(nm):
            try:
                twee_id = dict(tweet._json)["id"]
                tweet_text = dict(tweet._json)["text"]
                print("Id: {}".format(twee_id))
                print("text: {}".format(tweet_text))
                if twee_id in id_list:
                    print("Already Tweeted!")
                    tweet.favorite()
                    print("Tweet Likes")
                else:
                    api.retweet(twee_id)
                    tweet.favorite()
                    print("Tweet Likes")
                    print("Retweete successful!")
                    f.write(str(twee_id))
                    f.write("\n")
                    id_list.append(twee_id)
            except tweepy.TweepError as r:
                print(r.reason)
            print("--------------------------------")
        f.close()
        break


def only_retweet(hashtag="heppiness", num=20, id_list=[5632]):
    print(datetime.now())
    f = open("tweet_id.txt", 'a')
    try:
        for tweet in tweepy.Cursor(api.search, q=hashtag).items(num):
            try:
                twee_id = dict(tweet._json)["id"]
                tweet_text = dict(tweet._json)["text"]
                print("Id: {}".format(twee_id))
                print("text: {}".format(tweet_text))
                if True:
                    api.retweet(twee_id)
                    print("Retweete successful!")
                    f.write(str(twee_id))
                    f.write("\n")
                    id_list.append(twee_id)
            except tweepy.TweepError as r:
                print(r.reason)
            print("--------------------------------")
        f.close()
    except KeyboardInterrupt:
        f.close()
        sys.exit("Thank You")
    

def read_id():
    try:
        file = open("tweet_id.txt", 'r')
        id = file.readlines()
        id = [int(i.replace("\n", '' )) for i in id]
        return id
    except:
        a = [123456789]
        return a

def banner():
    print(colored('''
    |------------------------------------------------|
    | ++      ++      ++++++++++      ++          ++ |
    | ++      ++      ++++++++++      ++          ++ |
    | ++++++++++          ++          ++          ++ |
    | ++++++++++          ++          ++     +    ++ |
    | ++      ++          ++          ++    ++    ++ |
    | ++      ++    *     ++      *   ++  /+  +\  ++ |
    |------------------------------------------------|
    @A.I.SH.A
    ''', 'blue'))
    
def post_feed(post="hello Tweeter"):
    try:
        api.update_status(post)
        print("Status Udated")
        return  True
    except tweepy.TweepError as err:
        print(err.reason)
        return False



if __name__ == "__main__":
    id_list = read_id()
    # retweet("#Shankhnaad", 30, id_list)
    # follow(50)
    # print(api.trends_available())
    banner()
    print(colored("Hello User. This is Twitter Bot.", 'green'))
    user_data()
    qury = '1'
    while qury != 0:
        print('''
[1]. likes Tweets
[2]. Retweet
[3]. Like and tweet
[4]. follow followers
[5]. User Details
[0]. Quit
            ''')
        qury = input("A.I.SH.A >> ")
        if qury == '0':
            print("Thanks")
            exit(0)
        # likes
        elif qury == '1':
            tag = input("Enter Keyword or hash tag: >> ")
            while tag is None:
                print("Please Enter Any Keyword Or Hash tag")
                tag = input("Enter Keyword or hash tag: >> ")
            
            number = int(input("How many tweets want to Likes? >> "))
            while number > 700:
                print("Please enter Below 700")
                number = int(input("How many tweets want to Likes? >> "))
            like(tag=tag, number=number)
            print("Done")
            
        elif qury == '2':
            tag = input("Enter Keyword or hash tag: >> ")
            while tag is None:
                print("Please Enter Any Keyword Or Hash tag")
                tag = input("Enter Keyword or hash tag: >> ")
    
            number = int(input("How many tweets want to Retweet? >> "))
            while number > 700:
                print("Please enter Below 700")
                number = int(input("How many tweets want to Retweets? >> "))
            only_retweet(tag, number, id_list)
            print("Done")
            
        elif qury == '3':
            tag = input("Enter Keyword or hash tag: >> ")
            while tag is None:
                print("Please Enter Any Keyword Or Hash tag")
                tag = input("Enter Keyword or hash tag: >> ")
    
            number = int(input("How many tweets want to Retweet and Likes? >> "))
            while number > 700:
                print("Please enter Below 700")
                number = int(input("How many tweets want to Retweet and Likes? >> "))
            retweet(tag, id_list, number)
            print("Done")
            
        elif qury == '4':
            number = int(input("How many follower wants to follow? >> "))
            while number > 700:
                print("Please enter Below 700")
                number = int(input("How many follower wants to follow? >> "))
            follow_follower(num=number)
            print("Done")
            
        elif qury == '5':
            name = str(input("Enter Screen Name >> "))
            while name is None:
                name = str(input("please Enter Screen Name >> "))
            user_details(name=name)
            print("Done")
        
        else:
            print("Choose Veiled Option")
        banner()
        
        