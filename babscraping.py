
import requests
import imaplib
import sys
import email
from bs4 import BeautifulSoup
import urllib
import time
import traceback
import re
import quopri
from html.parser import HTMLParser
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import json
import selenium 


gmail_username = "baborders2018@gmail.com"
gmail_password = "BABwework1"
order_number_formats = {'Amazon': '^\d{1,9}-\d{1,9}-\d{1,9}$'}
google_order_formats = {'GS.': '^\d{1,9}-\d{1,9}-\d{1,9}$'}
url_list = []
count = 1

class parseLinks(HTMLParser):
    
    def handle_starttag(self, tag, attrs):

        # print("im back here in handle_starttag")
        strval = " "
        
        global global_futures_fair_value
        if tag == 'a':
            for name, value in attrs:
                # count = count + 1
                if name == 'href':
                    # print("value before")
                    #print(value)
                    if 'bestbuy' in value and 'tracking' in value:

                        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

                        
                        if value not in url_list:
                                # tracktemp = "I got the track url" + strval
                                # print(tracktemp)
                                # print(value)
                                # print("im back here in best buy")
                                url_list.append(value)
                                # print("lets print the url list")
                                # print(url_list)
                                response = requests.get(value, headers=headers)
                                html_page = response.text
                                extract_tracking_best_buy(html_page)
                                break

                    elif 'shiptrack' in value:
                        # tracktemp = "I got the track url" + strval
                        # print(tracktemp)
                        # print("im back here in amazon")
                        extract_tracking_amazon(value)
                        break  #why are we not returning - just changed to break

                    # google tracking 
                    
                    # elif count == 4: #the 4th url in the email is for tracking
                        # strtemp = "I got the track url" + value
                        # print(strtemp)
                    
                    # print(count)  
                    # print(value)





def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def extract_tracking_best_buy(value):

        html = BeautifulSoup(value, 'lxml')
        script_part = html.find_all("script")
        # print(script_part);
        pattern = re.compile("trackingnumber=")
        print("============")
        print("printing script part for best buy")
        # print(script_part)
        for i in script_part:
            if 'trackingnumber' in i.text.lower():
                # item = re.findall(pattern,i.text)
                # print("BEST BUY")
                # print("tracking #")
                # print(item)

                item = i.text.split('trackingnumber')
                temp = str(item)
                data = temp.split()
                for i in data:
                    if "number" in i: 
                        print(i)


                # data = json.loads(str(i), type='application/ld+json')
                # print(data.test)

def extract_tracking_amazon(value):

    rawhtml = simple_get(value)

    html = BeautifulSoup(rawhtml, 'lxml')
    list = html.find_all("a",class_='carrierRelatedInfo-trackingId-text')

    for i,a in enumerate(list):
        print("AMAZON")
        # print("tracking #")
        print(a.text)

    # for a in html.find_all('a', href = re.compile("orderId=")):
    #   url = a['href'].split('=')
    #   print(url[-1])

    item = html.find_all("a", href=re.compile("orderId="))
    temp = str(item)
    # print("printing this temp now")

    print(temp[132:151])
    # print(item)
    # temp = item.split('orderId:')[1].split("&")[0]
    # print(temp)
 #    print url[-1]
    # print(type(item))
    # print(item.find_all('orderId'))
    # item = item.split('orderId=')[1].split("}")[0]
    

    # # amazon_order_number = " "
    # script_part = html.find_all("script")
    # # print(script_part)
    # for i in script_part:
    #   if 'orderId' in i.text.lower():
    #       print
    #       item = i.text.split('orderId:')[1].split("}")[0]
    #       print(item)

def extract_tracking_google(url):

    rawhtml = simple_get(url)
    html = BeautifulSoup(rawhtml,'lxml')
    script_part = html.find_all("script")
    print("printing script part now")
    print(script_part)
    print("get script text")
    for i in script_part:
        print(i.text.lower())

    # print("hellow")
    #   pattern = re.compile("trackingnumber=")
    #   print("============")
    #   print("printing script part for best buy")
    #   # print(script_part)
    #   for i in script_part:
    #       if 'trackingnumber' in i.text.lower():
    #           # item = re.findall(pattern,i.text)
    #           # print("BEST BUY")
    #           # print("tracking #")
    #           # print(item)

    #           item = i.text.split('trackingnumber')
    #           temp = str(item)
    #           data = temp.split()
    #           for i in data:
    #               if "number" in i: 
    #                   print(i)



    # list = html.find_all("h1",class_='RedesignedDetailTitleBarTVC')

    # for i,a in enumerate(list):
    #   print("GOOGLE")
    #   # print("tracking #")
    #   print(a.text)


def get_inbox_list():
    email_keys = []
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    try:
        mail.login(gmail_username, gmail_password)
        mail.select("inbox")

    except Exception as e:
        print("couldnt login")
        print(e)
        sys.exit()

    result, inbox_data = mail.uid('search', None, "ALL")

    for i in inbox_data:
        email_keys.append(i)

    inbox_item_list = email_keys[0].split()

    return mail, inbox_item_list


def get_email(mail, item):

    result, message = mail.uid('fetch', item, '(RFC822)')
    raw_email = message[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)

    subject = email_message['subject']
    # print("we are in get_email and printing subject")
    # print(subject)

    for part in email_message.walk():
        if part.get_content_type() == 'text/html':
            html_email = part.get_payload()

    return subject, html_email


def identify_store(strong_tags):
    store = ' '
    for tag in strong_tags:
        if 'Amazon' in str(tag.text):
            store = 'Amazon'
            break

        if 'Best Buy' in str(tag.text):
            store = 'Best Buy'
            break

        if 'Google' in str(tag.text):
            store = 'Google'
            break

    return store


def extract_amazon(soup):

    # print("inside amazon function")
    # added - inital variable amazon_order_number
    amazon_order_number = " "
    script_part = soup.find_all("script")
    print(script_part)
    print("printing the script part")
    print(script_part)
    print("im here before this for loop")
    for i in script_part:
        if 'orderId' in i.text.lower():
            item = i.text.split('orderId":')[1].split("}")[0]
            print(item)
    # atags = soup.find_all('a')
    # for a in atags:
    #   tag_text = a.text
    #   print("tag text")
    #   print(tag_text)
    #   if re.compile(order_number_formats['Amazon']).fullmatch(tag_text.replace('=', '')):
    #       print("in here")
    #       print(a.text)
    #       amazon_order_number = a.text
    #       break
    return amazon_order_number

# def extract_googe(email_msg):

def extract_google(msg):
    google_order_number = " "
    print("i ammmm here now ")
    
    if 'GS.' in msg:
        temp = msg.split('GS.')
        print("after gs split==========")
        print("order number")
        temp = temp[1].split('</a>')
        print(temp[0])
        google_order_number = temp[0]
        # print(temp[1])
        
    # if re.compile(google_order_formats['GS.']).fullmatch(msg.replace('GS.', 'GS.')):
    #   print("in here----------++++++++++++++")
        # print(msg)
            # google_order_number = msg
        # break

    return google_order_number

def decodeUrl_tracking(html_email):
        # print("type of email is")
        # print(type(html_email))
        msg = str(html_email)
        msg = quopri.decodestring(msg)
        msg = str(msg)
        # print("type on coverting is")
        # print(type(msg))

        # print("printing message now ========")
        # # print(msg)
        # print("type is")
        # print(type(msg))
        if 'Track Shipment' in msg:
             temp = msg.split('Track Shipment')
             # print("======= printing 0")
             temp = temp[0].split('href="')
             temp = temp[4].split('" style')[0]
             print("this is the track url")
             print(temp)

             extract_tracking_google(temp)
             # print("======= printing 1")
             # print(temp[1])
        print("done with if")
        # for a in atags:
        #   tag_text = a.text
        #   print("tag_text")
        #   print(tag_text)
        linkParser = parseLinks()
        # print("back here in decode url ")
        msg = quopri.decodestring(msg)
        msg = msg.decode('utf-8')
        # print("im before feed ")
        linkParser.feed(msg)
        return msg
        # print("im after feed")



def extract_bestbuy(subject):

    best_buy_order_number = re.search('Your order #(.*) has shipped', subject).group(1)

    return best_buy_order_number


mail, inbox_list = get_inbox_list()

for item in inbox_list:

    subject, html_email = get_email(mail, item)



    if 'shipped' in subject:
        soup = BeautifulSoup(html_email, 'lxml')
        # print(soup)
        # print("soup is of the type")
        # print(type(soup))
        strong_tags = soup.find_all('strong')
        atags = soup.find_all
        store = identify_store(strong_tags)
        # print(soup)
        if store == 'Amazon':
            # print("in amazon")
            decodeUrl_tracking(html_email)

            order_number = extract_amazon(soup)

        elif store == 'Best Buy':
            decodeUrl_tracking(html_email)
            # print("back here after decode url tracking")
            order_number = extract_bestbuy(str(subject))

        elif store == 'Google':
            print("im in google")
            msg = decodeUrl_tracking(html_email)

            order_number = extract_google(msg)

            # cleorder_number = extract_google(html_email)


        print("order #")
        print(order_number)

        #moving read procesed email - with word shipped to the shipped folder
    #   resp = mail.uid('COPY', item, 'shippedemails')
    #   if resp[0] == 'OK':
    #       mov, data_temp = mail.uid('STORE',item, '+FLAGS', '(\Deleted)')
    #       mail.expunge()
   
    # #moving unprocessed email to the unprocessed folder
    # resp = mail.uid('COPY', item, 'Unprocessed')
    # if resp[0] == 'OK':
    #   mov, data_temp = mail.uid('STORE',item, '+FLAGS', '(\Deleted)')
    #   mail.expunge()
