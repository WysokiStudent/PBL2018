import requests  # lib for using http methods and interacting with sites
import webbrowser  # lib just to open the html file in a browser
# from bs4 import BeautifulSoup  # lib for parsing html

import os

class LicenseWebAnalyzer:
    """
    Can send a license to a web analyzer and then fetch the result of analysis
    """

    def __init__(self):
        self.analyzer_url = \
            'http://www.spywareguide.com/analyze/go.php'
        self.session = requests.Session()  # session object used for http methods
        self.session.get(self.analyzer_url, verify=False)


    def analyze_license_file(self, license_path: str):
        with open(license_path, 'r') as input_file:  # reading the license text from a file into a variable
            input_license = input_file.read()
        self.analyze_license_string(input_license)


    def analyze_license_string(self, license_text: str):
        response_text = self.request_license_analysis(license_text).text
        with open('response.html', 'w', encoding="utf-8") as newfile:
            for line in response_text.splitlines():
                if 'Notice: Undefined' not in line:
                    newfile.write(line)
        '''
        # removing the html tags
        post_response_without_tags = BeautifulSoup(post_response.text, 'html.parser')
        
        # saving the resulting text without html tags as a text file
        with open("output.txt", "w") as output_file:
            print(post_response_without_tags.get_text(), file=output_file)
        '''

    def request_license_analysis(self, license_text: str):
        # configuring http headers and FormData (seems like header can be empty)
        request_headers = {}
        request_data = dict(title='none', url='none', license=license_text, anmode=0, comment='none', submit='Start Analyzer')
        # calling the http 'post' method with the prepared headers & data and save the http response as a variable
        post_response = self.session.post(
            self.analyzer_url,
            data=request_data,
            headers=request_headers,
            verify=False)
        return post_response

    def write_response(self, response_text: str):
        with open("response.html", "w") as response_file:  # writing the resulting response to an html file
            print(response_text, file=response_file)


    def open_analysis_in_browser(self):
        webbrowser.open("file://" + os.path.realpath("response.html"))  # opening the html file in a browser


# to test:
# lic = LicenseWebAnalyzer()
# lic.analyze_license_file('license.txt')
# lic.open_analysis_in_browser()
