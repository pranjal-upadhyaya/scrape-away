import requests
import pickle as pickle
import tldextract as tld
from fake_useragent import UserAgent

class Spider:

    def __init__(self, url) -> None:
        self.url = url
        self.headers = None
        self.proxies = None
        self.user_agent = None
        self.cookies = None
        self.method = "get"
        self.response_obj = {}

    def get_proxy():
        pass

    def get_cookies(self, headers = None, proxies = None):
        extracted_url = tld.extract(self.url)
        domain = extracted_url.domain

        url = "https://www.google.com/search?q=" + domain

        response = requests.get(url, headers = headers, proxies = proxies)

        # Get the cookies from the response object
        cookies = response.cookies

        # Save the cookies to a file using pickle
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(cookies, file)

        # Load the cookies from the file using pickle
        with open('cookies.pkl', 'rb') as file:
            loaded_cookies = pickle.load(file)

        return loaded_cookies

    def get_user_agent(self, browsers: list | str = [], os : str | list = [], platform: str | list = []):
        ua = UserAgent(browsers=browsers, os = os, platforms=platform)
        self.user_agent = ua.random
        return self.user_agent
    
    def get_headers(self, user_agent = None, response_language: str = 'en-US,en;q=0.5'):
        headers = {}
        if user_agent:
            headers["User-Agent"] = user_agent
        if response_language:
            headers["Accept-Language"] = response_language
        self.headers = headers
        return self.headers
    
    def send_request(self, params: dict | None = None, data: dict | None = None, browsers: list | str = [], os : str | list = [], platform: str | list = [], response_language: str = 'en-US,en;q=0.5', timeout: int = 10):
        
        output = {}
        
        try:

            extracted_url = tld.extract(self.url)
            if extracted_url.subdomain == extracted_url.suffix == "":
                return output

            try:
                self.user_agent = self.get_user_agent(browsers, os, platform)
            except Exception as e:
                print(e)
            try:
                self.headers = self.get_headers(self.user_agent, response_language)
            except Exception as e:
                print(e)
            try:
                self.cookies = self.get_cookies(headers = self.headers, proxies= self.proxies)
            except Exception as e:
                print(e)

            try:
                if self.method == "get":
                    response = requests.get(url=self.url, params=params, headers=self.headers, data=data, proxies=self.proxies, cookies=self.cookies, timeout=timeout)
                if self.method == "post":
                    response = requests.post(url=self.url, params=params, headers=self.headers, data=data, proxies=self.proxies, cookies=self.cookies, timeout=timeout)
            except Exception as e:
                print(e)

            if response:
                # Input url
                output["input_url"] = self.url

                # Status code
                output["status_code"] = response.status_code

                # Content-Type
                content_type = response.headers.get('Content-Type')
                output["content_type"] = content_type

                # Content-Length
                content_length = response.headers.get('Content-Length')
                output["content_length"] = content_length

                if content_type.startswith("text/"):
                    output["response_data"] = response.text
                if content_type == "application/json":
                    output["response_data"] = response.json()

                # Date
                date = response.headers.get('Date')
                output["request_date"] = date

                # Server
                server = response.headers.get('Server')
                output["server"] = server

                # Set-Cookie
                set_cookie = response.headers.get('Set-Cookie')
                if set_cookie:
                    # Save the cookies to a file using pickle
                    with open('cookies.pkl', 'wb') as file:
                        pickle.dump(set_cookie, file)

                # Cache-Control
                cache_control = response.headers.get('Cache-Control')
                output["cache_control"] = cache_control

                # Expires
                expires = response.headers.get('Expires')
                output["expires"] = expires

                # Last-Modified
                last_modified = response.headers.get('Last-Modified')
                output["last_modified"] = last_modified

                # Location
                location = response.headers.get('Location')
                output["location"] = location

                # ETag
                etag = response.headers.get('ETag')
                output["etag"] = etag

                # WWW-Authenticate
                www_authenticate = response.headers.get('WWW-Authenticate')
                output["www_authenticate"] = www_authenticate

                # Allow
                allow = response.headers.get('Allow')
                output["allow"] = allow

                # Access-Control-Allow-Origin
                access_control_allow_origin = response.headers.get('Access-Control-Allow-Origin')
                output["access_control_allow_origin"] = access_control_allow_origin

                # Content-Encoding
                content_encoding = response.headers.get('Content-Encoding')
                output["content_encoding"] = content_encoding

                # Transfer-Encoding
                transfer_encoding = response.headers.get('Transfer-Encoding')
                output["transfer_encoding"] = transfer_encoding

                # Vary
                vary = response.headers.get('Vary')
                output["vary"] = vary

                # Connection
                connection = response.headers.get('Connection')
                output["connection"] = connection

                # Accept-Ranges
                accept_ranges = response.headers.get('Accept-Ranges')
                output["accept_ranges"] = accept_ranges

                # X-Powered-By
                x_powered_by = response.headers.get('X-Powered-By')
                output["x_powered_by"] = x_powered_by

                # X-Frame-Options
                x_frame_options = response.headers.get('X-Frame-Options')
                output["x_frame_options"] = x_frame_options

                # Strict-Transport-Security
                strict_transport_security = response.headers.get('Strict-Transport-Security')
                output["strict_transport_security"] = strict_transport_security

                # Content-Disposition
                content_disposition = response.headers.get('Content-Disposition')
                output["content_disposition"] = content_disposition

                # Content-Security-Policy
                content_security_policy = response.headers.get('Content-Security-Policy')
                output["content_security_policy"] = content_security_policy

                self.response_obj = output
        
        except Exception as e:
            print(e)
            
        return output


    
    
