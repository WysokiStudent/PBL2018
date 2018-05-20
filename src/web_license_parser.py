# lib for using http methods and interacting with sites
import requests
# lib just to open the html file in a browser
import webbrowser
# lib for parsing html
# from bs4 import BeautifulSoup


# session object used for http methods
session = requests.Session()
# setting up info for the post request data
parser_url = 'http://www.spywareguide.com/analyze/go.php'
session.get(parser_url)

# loading post request license text
with open('license.txt', 'r') as input_file:
    input_license = input_file.read()
request_data = dict(title='some title', url='some url', license=input_license, anmode=2, comment='heh xD', submit='Start Analyzer')
request_headers = {"Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 "Accept-Encoding": 'gzip, deflate' ,
                 "Accept-Language": 'en-GB,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,pl-PL;q=0.6,pl;q=0.5,fr-FR;q=0.4,fr;q=0.3,en-US;q=0.2',
                 "Cache-Control": 'max-age=0',
                 "Connection": 'keep-alive',
                 "Content-Length": '70',
                 "Content-Type": 'application/x-www-form-urlencoded',
                 "DNT": "1",
                 "Host": 'www.spywareguide.com',
                 "Origin": 'http://www.spywareguide.com',
                 "Referer": 'http://www.spywareguide.com/analyze/analyzer.php',
                 "Upgrade-Insecure-Requests": "1",
                 "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
                 }

# get the resulting page from using the http post method to send the license text to the parser
post_response = session.post(parser_url, data=request_data, headers=request_headers)

# saving the resulting response as a html file
with open("response.html", "w") as response_file:
    print(post_response.text, file=response_file)

# opening the html file in a browser
webbrowser.open("response.html")

'''
# removing the html tags
post_response_without_tags = BeautifulSoup(post_response.text, 'html.parser')

# saving the resulting text without html tags as a text file
with open("output.txt", "w") as output_file:
    print(post_response_without_tags.get_text(), file=output_file)
'''