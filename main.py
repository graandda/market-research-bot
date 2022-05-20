import requests
from bs4 import BeautifulSoup
import json
import lxml
import os



def add_sub_list(value:str):
    new_value = value.replace(" ", "%").lower()

    with open("subs.json") as file:
        data = json.load(file)

    data["key"] += [f"{new_value}"]

    with open("subs.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def check_sub_list():
    words = ""
    with open("subs.json", "r") as file:
        data = json.load(file)
        for word in data["key"]:
           words += str(word).replace("%", " ") + '\n'
        return words

def del_sub(value):

    with open("subs.json") as file:
        data = json.load(file)
    try:
        data["key"].remove(str(value).replace(" ", "%"))

    except ValueError:
        return f"ERROR : {value} NOT in your list"

    with open("subs.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    try:
        os.remove(f'new_dict_{str(value).replace(" ", "%")}.json')
    except FileNotFoundError:
        print("***")

    try:
        os.remove(f'last_ann_dict_{str(value).replace(" ", "%")}.json')
    except FileNotFoundError:
        print("***")

    return value



def token():
    url = "https://www.blocket.se/"
    json1 = {
    "Content - type": "application / json"
    }
    response = requests.post(url=url, json=json1)
    soup = BeautifulSoup(response.text, "lxml")
    script_id = json.loads(soup.find("script", id= "__NEXT_DATA__").text)
    return script_id["props"]['initialReduxState']["authentication"]["bearerToken"]


def get_last_announ(sub_word):

        headers = {
            "authorization" : f"Bearer {token()}",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
        }
        s = requests.Session()
        url = f"https://api.blocket.se/search_bff/v1/content?lim=40&q={sub_word}&st=s&include=all&gl=3&include=extend_with_shipping"
        response = s.get(url=url, headers=headers).json()
        anno_dict = {}

        for item in response["data"]:
            ad_id = item["ad_id"]
            ad_link = item["share_url"]
            ad_body = item["body"]
            if "price" not in item:
                ad_price = None
            else:
                ad_price = str(item["price"]["value"]) + " " + item["price"]["suffix"]

            anno_dict[ad_id] = {
                "link" : ad_link,
                "body" : ad_body,
                "price" : ad_price
            }

        with open(f"new_dict_{sub_word}.json", "w") as file:
            json.dump(anno_dict, file , indent=4, ensure_ascii=False)


def check_new_update(sub_word):
    with open(f"new_dict_{sub_word}.json") as file:
        anno_dict = json.load(file)

    headers = {
        "authorization": f"Bearer {token()}",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
    }

    s = requests.Session()
    url = f"https://api.blocket.se/search_bff/v1/content?lim=40&q={sub_word}&st=s&include=all&gl=3&include=extend_with_shipping"
    response = s.get(url=url, headers=headers).json()
    new_anno_dict = {}

    for item in response["data"]:

        ad_id = item["ad_id"]
        if ad_id in anno_dict:
            continue
        else:
            ad_link = item["share_url"]
            ad_body = item["body"]
            if "price" not in item:
                ad_price = None
            else:
                ad_price = str(item["price"]["value"]) + " " + item["price"]["suffix"]
            anno_dict[ad_id] = {
                "link": ad_link,
                "body": ad_body,
                "price": ad_price
            }

            new_anno_dict[ad_id] = {
                "link": ad_link,
                "body": ad_body,
                "price": ad_price
            }
            with open(f"last_ann_dict_{sub_word}.json", "w") as file:
                json.dump(new_anno_dict, file, indent=4, ensure_ascii=False)

    with open(f"new_dict_{sub_word}.json", "w") as file:
        json.dump(anno_dict, file, indent=4, ensure_ascii=False)


    return new_anno_dict

