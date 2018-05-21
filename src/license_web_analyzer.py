import requests  # lib for using http methods and interacting with sites
import webbrowser  # lib just to open the html file in a browser
# from bs4 import BeautifulSoup  # lib for parsing html


class LicenseWebAnalyzer:
    """
    Can send a license to a web analyzer and then fetch the result of analysis
    """
    @staticmethod
    def analyze(license_path: str):
        session = requests.Session()  # session object used for http methods
        analyzer_url = 'http://www.spywareguide.com/analyze/go.php'
        session.get(analyzer_url)
        with open(license_path, 'r') as input_file:  # reading the license text from a file into a variable
            input_license = input_file.read()
        # configuring http headers and FormData (seems like header can be empty)
        request_headers = {}
        request_data = dict(title='none', url='none', license=input_license, anmode=2, comment='none', submit='Start Analyzer')
        # calling the http 'post' method with the prepared headers & data and save the http response as a variable
        post_response = session.post(analyzer_url, data=request_data, headers=request_headers)
        with open("response.html", "w") as response_file:  # writing the resulting response to an html file
            print(post_response.text, file=response_file)
        webbrowser.open("response.html")  # opening the html file in a browser
 
        '''
        # removing the html tags
        post_response_without_tags = BeautifulSoup(post_response.text, 'html.parser')
        
        # saving the resulting text without html tags as a text file
        with open("output.txt", "w") as output_file:
            print(post_response_without_tags.get_text(), file=output_file)
        '''

# to test:
# LicenseWebAnalyzer.analyze('license.txt')
