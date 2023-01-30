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
                    
                    except requests.exceptions.HTTPError as http_err:
                        if response.status_code == 401:
                            logging.error(f'Error: {response.status_code} - Unauthorized')
                        elif response.status_code == 403:
                            logging.error(f'Error: {response.status_code} - Forbidden')
                        elif response.status_code == 404:
                            logging.error(f'Error: {response.status_code} - Not Found')
                        elif response.status_code == 429:
                            logging.error(f'Error: {response.status_code} - Too Many Requests')
                        elif response.status_code >= 500:
                            logging.error(f'Error: {response.status_code} - Server Error')
                        else:
                            logging.error(f'Error: {response.status_code} - Other Error')

                        if response.status_code in [401, 403, 404]:
                            raise Exception(f'Error: {response.status_code}')
                        elif response.status_code == 429:
                            logging.warning(f'Retrying in {self.retry_interval} seconds')
                            sleep(self.retry_interval)
                        elif response.status_code >= 500:
                            logging.warning(f'Retrying in {self.retry_interval} seconds')
                            sleep(self.retry_interval)
                    except Exception as err:
                            logging.error(f'Other error occurred: {err}')
                            break
                            
    def get_data(self, endpoint, page_num=1, page_size=10):
        params = {'page': page_num, 'page_size': page_size}
        return self._make_request(endpoint, params=params)
    
    def post_data(self, endpoint, data):
        return self._make_request(endpoint, method='post', json=data)

    def put_data(self, endpoint, data):
        return self._make_request(endpoint, method='put', json=data)

    def delete_data(self, endpoint):
        return self._make_request(endpoint, method='delete')

    def authenticate(self, username, password):
        auth_endpoint = "https://example.com/authenticate"
        auth_data = {'username': username, 'password': password}
        response = self._make_request(auth_endpoint, method='post', json=auth_data)
        self.api_key = response['access_token']    

        
