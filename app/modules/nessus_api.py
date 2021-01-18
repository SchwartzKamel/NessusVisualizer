import requests
import json
import time
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
                       'X-Cookie': str(self.token)}
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
        if resp.status_code != 200:
            e = resp.json()
            sys.exit(e['error_msg'])
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

    def logout(self):
        """
        Logs out of Nessus
        """
        data = self.connect('DELETE', '/session')

    ### CORE UTILS ###
    def scans_export(self, scan_id, history_id, filename, status_interval=1, status_max=300, verbose=False):
        """
        Parameters:
        status_interval: Wait n seconds before checking status again
        """
        request = self.scans_export_request(scan_id, history_id)
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
            scan_id, file_id, filename)
        return download_response

    def download_file(self, url, filename):
        payload = {}

        with requests.get(url, params=payload, stream=True) as r:
            r.raise_for_status()
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush()
        return filename

    def get_scan_folders(self):
        """
        Get all of the scan folders

        Returns:
        ret (list): a list of tuples (folder_id, folder_name)
        """
        folders_list = self.folders_list.json()
        ret = [(f['id'], f['name']) for f in folders_list['folders']]
        return ret

    def get_scan_ids(self, folder_id=None):
        """
        Get all of the scans for a speficied folder

        Parameters:
        folder_id (int): the id for the folder containing your scans (optional)
        Returns:
        ret (list): a list of tuples (scan_id, scan_name)
        """
        scans_list = self.scans_list()
        ret = [(f['id'], f['name']) for f in scans_list['scans']
               if not folder_id or f['folder_id'] == folder_id]
        return ret

    def get_scan_history_ids(self, scan_id, completed=True):
        """
        Get all of the history ids for a specified scan
        Parameters:
        scan_id (int): id for the scan
        completed (bool): only collect completed scans
        Returns:
        history (list): a list of tuples (history_id(int),timestamp:int)
        """
        scans_details = self.scans_details(scan_id)
        if scans_details['history']:
            history = [(f['history_id'], f['creation_date'])for f in scans_details['history']
                       if not completed or f['status'] == 'completed']
        else:
            history = []
        return history

    ### FOLDER UTILS ###
    def folders_list(self):
        path = '/folders'
        payload = {}

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

        response = self.connect('GET', path, data=payload)
        response_text = json.loads(response.text)
        return response_text

    def scans_details(self, scan_id):
        return self.scans_list(scan_id=scan_id)

    def scans_export_request(self, scan_id, history_id=None, format_type='csv'):
        path = '/scans' + str(scan_id) + '/export'
        if history_id:
            path = path + '?history_id=' + str(history_id)

        csvColumns = {"id": True, "cve": True, "cvss": True, "risk": True, "hostname": True, "protocol": True,
                      "port": True, "plugin_name": True, "synopsis": True, "description": True, "solution": True,
                      "see_also": True, "plugin_output": True, "stig_severity": True, "cvss3_base_score": True,
                      "cvss_temporal_score": True, "cvss3_temporal_score": True, "risk_factor": True, "references": True,
                      "plugin_information": True, "exploitable_with": True}

        # Build payload
        data = '{"format":"csv","filter.search_type":"and","reportContents.formattingOptions.page_breaks":false,"reportContents.hostSections.scan_information":true,"reportContents.hostSections.host_information":true,"reportContents.vulnerabilitySections.synopsis":true,"reportContents.vulnerabilitySections.description":true,"reportContents.vulnerabilitySections.see_also":true,"reportContents.vulnerabilitySections.solution":true,"reportContents.vulnerabilitySections.risk_factor":true,"reportContents.vulnerabilitySections.cvss3_base_score":true,"reportContents.vulnerabilitySections.cvss3_temporal_score":true,"reportContents.vulnerabilitySections.cvss_base_score":true,"reportContents.vulnerabilitySections.cvss_temporal_score":true,"reportContents.vulnerabilitySections.stig_severity":true,"reportContents.vulnerabilitySections.references":true,"reportContents.vulnerabilitySections.exploitable_with":true,"reportContents.vulnerabilitySections.plugin_information":true,"reportContents.vulnerabilitySections.plugin_output":true}'

        response = self.connect('POST', path, data=payload)
        response_text = json.loads(response.text)
        return response_text

    def scans_export_status(self, scan_id, file_id, simple=True):
        path = '/scans' + '/' + str(scan_id) + '/export/' + \
            str(file_id) + '/status'

        payload = {}
        response = self.connect('GET', path, data=payload)

        state = json.loads(response.text)['status']

        if simple:
            if response.status_code == 200 and state == 'ready':
                return True
            else:
                return False
        else:
            return response

    def scans_export_download(self, scan_id, file_id, filename):
        path = '/scans' + str(scan_id) + '/export/' + \
            str(file_id) + '/download'
        payload = {}

        response = self.download_file(url, filename, data=payload)
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
