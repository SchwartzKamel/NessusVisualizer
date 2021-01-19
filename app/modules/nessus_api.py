import requests
import json
import time
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class NessusAPI(object):
    """
    Class to handle our Nessus API calls.
    """

    url_pull_scan = None

    ### CONNECTION ###
    def __init__(self, username: str, password: str, url: str):
        self.username = username
        self.password = password
        self.url = url
        self.token = None

    def build_url(self, resource):
        """
          Formats the Nessus URL with the requested resource.
          """
        return '{0}{1}'.format(self.url, resource)

    def connect(self, method: str, resource: str, data: dict = None, headers: dict = None):
        """
        The connect method is used to connect to Nessus and pass our API calls.
        """
        if headers is None:
            headers = {'Content-type': 'application/json',
                       'X-Cookie': "token=" + str(self.token)}
        if data is not None:
            data = json.dumps(data)
        if method == "POST":
            resp = requests.post(self.build_url(resource),
                                 data=data, headers=headers, verify=False)
        elif method == "DELETE":
            resp = requests.delete(self.build_url(
                resource), data=data, headers=headers, verify=False)
        elif method == 'PATCH':
            resp = requests.patch(self.build_url(resource),
                                  data=data, headers=headers, verify=False)
        else:
            resp = requests.get(self.build_url(resource),
                                data=data, headers=headers, verify=False)
        return resp

    def login(self):
        """
        Logs into Nessus and retrieves our token. We create a separate header here since we do not
        have a X-Cookie token yet.
        """
        headers = {'Content-Type': 'application/json'}
        login = {'username': self.username, 'password': self.password}
        # We use the connect function and pass it a POST method, /rest/token resource,
        # and our login credentials as data.  We also pass our headers from above for this function.
        data = self.connect('POST', '/session', data=login, headers=headers)

        # We pull our token out from the returned data.
        self.token = data.json()['token']
        return self.token

    def get_session_token(self):
        if not self.token:
            token = self.login()
            self.token = token

        return self.token

    def update_payload_token(self, dictionary):
        dictionary['token'] = self.get_session_token()

    def logout(self):
        """
        Logs out of Nessus
        """
        data = self.connect('DELETE', '/session')

    ### CORE UTILS ###
    def scans_export(self, scan_id, status_interval=1, status_max=300, verbose=False):
        """
        Parameters:
        status_interval: Wait n seconds before checking status again
        """
        request = self.scans_export_request(scan_id)
        file_id = request['file']
        # check for updates
        ready_status = False
        status_check = 1
        while not ready_status:

            ready_status = self.scans_export_status(scan_id, file_id)
            if ready_status:
                break
            if verbose:
                print("Waiting for file download (" + str(file_id) + ") to be ready (" + str(status_check) +
                      "/" + str(status_max) + ")")
            time.sleep(status_interval)

            if status_check >= status_max:
                raise Exception(
                    "File not ready for download in time, increase status_max value")
            status_check = status_check + 1

        download_response = self.scans_export_download(
            scan_id, file_id)
        return download_response

    def get_scan_folders(self):
        """
        Get all of the scan folders

        Returns:
        ret (list): a list of tuples (folder_id, folder_name)
        """
        folders_list = self.folders_list
        ret = [(f['id'], f['name']) for f in folders_list['folders']]
        return ret

    def get_scan_ids(self, folder_id=None):
        """
        Get all of the scans for a specified folder

        Parameters:
        folder_id (int): the id for the folder containing your scans (optional)
        Returns:
        ret (list): a list of tuples (scan_id, scan_name)
        """
        scans_list = self.scans_list()
        ret = [(f['id'], f['name']) for f in scans_list['scans']
               if not folder_id or f['folder_id'] == folder_id]
        return ret

    ### FOLDER UTILS ###
    def folders_list(self):
        path = '/folders'
        payload = {}
        self.update_payload_token(payload)
        response = self.connect('GET', path, data=payload)
        response_text = json.loads(response.text)
        return response_text

    ### SCAN UTILS ###
    def scans_list(self, folder_id=None, scan_id=None):
        path = '/scans'
        if scan_id:
            url = url + '/' + str(scan_id)

        payload = {}

        if folder_id:
            payload['folder_id'] = folder_id

        self.update_payload_token(payload)
        response = self.connect('GET', path, data=payload)
        response_text = json.loads(response.text)
        return response_text

    def scans_details(self, scan_id):
        return self.scans_list(scan_id=scan_id)

    def scans_export_request(self, scan_id):
        path = '/scans/' + str(scan_id) + '/export'

        # Build payload
        payload = {}
        payload['format'] = "csv"
        payload['filter.search_type'] = "and"
        payload['reportContents.formattingOptions.page_breaks'] = False
        payload['reportContents.hostSections.scan_information'] = False
        payload['reportContents.hostSections.host_information'] = False
        payload['reportContents.vulnerabilitySections.synopsis'] = False
        payload['reportContents.vulnerabilitySections.description'] = False
        payload['reportContents.vulnerabilitySections.see_also'] = False
        payload['reportContents.vulnerabilitySections.solution'] = False
        payload['reportContents.vulnerabilitySections.risk_factor'] = False
        payload['reportContents.vulnerabilitySections.cvss3_base_score'] = False
        payload['reportContents.vulnerabilitySections.cvss3_temporal_score'] = False
        payload['reportContents.vulnerabilitySections.cvss_base_score'] = False
        payload['reportContents.vulnerabilitySections.cvss_temporal_score'] = False
        payload['reportContents.vulnerabilitySections.stig_severity'] = False
        payload['reportContents.vulnerabilitySections.references'] = False
        payload['reportContents.vulnerabilitySections.exploitable_with'] = False
        payload['reportContents.vulnerabilitySections.plugin_information'] = False
        payload['reportContents.vulnerabilitySections.plugin_output'] = False

        response = self.connect('POST', path, data=payload)
        response_text = json.loads(response.text)
        return response_text

    def scans_export_status(self, scan_id, file_id, simple=True):
        path = '/scans/' + str(scan_id) + '/export/' + \
            str(file_id) + '/status'

        payload = {}
        self.update_payload_token(payload)
        response = self.connect('GET', path, data=payload)

        state = json.loads(response.text)['status']

        if simple:
            if response.status_code == 200 and state == 'ready':
                return True
            else:
                return False
        else:
            return response

    def scans_export_download(self, scan_id, file_id):
        path = '/scans/' + str(scan_id) + '/export/' + \
            str(file_id) + '/download'

        payload = {}
        self.update_payload_token(payload)
        response = self.connect('GET', path)
        return response


# Validate login works
if __name__ == '__main__':
    # Define variables to test
    url = "https://SERVER_IP:8834"
    username = "USER_HERE"
    password = "PASSWORD_HERE"

    # This calls the login function and passes it your credentials, no need to modify this.
    nessus = NessusAPI(url=url, username=username, password=password)
    token = nessus.login()

    # Print token
    print(token)
