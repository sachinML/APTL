import requests
import logging
from time import sleep

class APIConnector:
    def __init__(self, api_key=None, retry_count=3, retry_interval=3):
        self.api_key = api_key
        self.session = requests.Session()
        self.retry_count = retry_count
        self.retry_interval = retry_interval
    
     def _make_request(self, endpoint, method='get', **kwargs):
        headers = kwargs.get('headers', {})
        if self.api_key:
                    headers['Authorization'] = f'Bearer {self.api_key}'
                kwargs['headers'] = headers
                for i in range(self.retry_count):
                    try:
                        if method == 'get':
                            response = self.session.get(endpoint, **kwargs)
                        elif method == 'post':
                            response = self.session.post(endpoint, **kwargs)
                        elif method == 'put':
                            response = self.session.put(endpoint, **kwargs)
                        elif method == 'delete':
                            response = self.session.delete(endpoint, **kwargs)
                        else:
                            raise ValueError(f'Invalid method: {method}')
                        response.raise_for_status()
                        return response.json()
        
 
        

class Get_Response:
        
    def data(self, response):
        if response.status == 200:
            logging.info('That was lucky')
            return json.loads(response.data)
    
    def error_handler(self, auth):
        if auth == 400:
            logger.error("According to the API, your request is Malformed.")
            
        elif auth == 401:
            logging.error("Unauthorized error, give the proper credentials.")
            
        elif auth == 403:
            logging.error("The client attempts a resource interaction that is outside of its permitted scope, contact with the developers!")
            
        elif auth == 404:
            logging.error("Client Error: Bad Request for url") 
            
        elif 500 <= auth < 600:
            logging.error("Sorry, There seems to be an internal issue with the API.")
            
        else:
            logging.error(f"Got an unexpected status code from the API (`{response.status}`).")
            
      
        
def download_data(**kwargs):
    
    if not validators.url(kwargs["path"]):
        print("Url is Invalid")   # will check the url format
        
    else:
        http = urllib3.PoolManager(num_pools=3)
        ranges = tuple(x for x in requests.status_codes._codes if x != 401)
        retry = Retry(3, raise_on_status=True, status_forcelist=ranges)

        try:
            r = http.request('GET', kwargs["path"], retries=retry)
            
            Response = Get_Response()
            return Response.data(r)
        
        except MaxRetryError as m_err:
            x = int(str([m_err.reason]).split(" ")[2])
            Error = Get_Response()
            print(x)
            
            return Error.error_handler(x)
        
        
#         data=get_data(r, path)
#         print("Give the File name: ")
        
#         file_name = input()
#         file_location = "D:\\ApiC\\API_VT" + "\\" + file_name + ".json"
#         with open(file_location, "w+") as file:
#             json.dump(data, file)


print("url entered is: ")
# x = input()
# download_data(x)

x = input()
y = input()
z = input()
download_data(path=x, userid=y, password=z)
            
