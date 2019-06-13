'''AT Internet API Helper

This script allows the user to fetch data from the AT Internet RESTful API.
It is assumed that the user has valid credentials or an API key for accessing
the data.

This script requires that the `requests` library is installed within
the Python environment you are running this script in.
'''

# import needed modules
import requests
import json
import math

class Request:
    '''
    A class used to represent a specific RESTful API call setup for AT Internet.
    
    Attributes
    ----------
    params : str | dict
        string (separated by '&') or dicitonary with request parameters *
    auth : str 
        combined string of authentication method 'apikey:' or 'header:' and 
        either API Key from AT Internet or BASE64 encoded string of 'email@email.com:password'
    allrows : bool, optional
        takes boolean to export all rows for the chosen period if True - default is False
    dataformat : str, optional
        takes string with one of the possible formats 'json', 'html', 'xml' or 'csv' - default is 'json'

    Methods
    -------
    get_rows(format=default)
        retrieves the amount of rows for the requested data - returns response
    get_maxdate(format=default)
        retrieves the ISO time until which the data is already available today - returns response
    get_data(format=default)
        retrieves the data - returns array of responses

    * for more information about the AT Internet API and possible paramters see here: 
    https://developers.atinternet-solutions.com/rest-api-en/getting-started-rest-en/code-samples-php-javascript/#python-script-json-format_3 

    '''

    COMPATIBLE_FORMATS_DATA = ["json", "html", "xml", "csv"]
    COMPATIBLE_FORMATS_ROWCOUNT_MAXDATE = ["json", "html", "xml"]
    DEFAULT_FORMAT = "json"

   
    def __init__(self, params, auth, allrows=False, dataformat=DEFAULT_FORMAT):
        '''Retrieve parameters submitted
        
        Parameters
        ----------
        params : str | dict
            either string of queryparameters like in a URL or dictionary *
        auth : str 
            combined string of authentication method 'apikey:' or 'header:' and 
            either API Key from AT Internet or BASE64 encoded string of 'email@email.com:password'
        allrows : bool, optional
            takes boolean to export all rows for the chosen period if True - default is False
        dataformat : str, optional
            takes string with one of the possible formats 'json', 'html', 'xml' or 'csv' - default is 'json'
        '''

        self.allrows = allrows
        self.params = self.__parse_params(params)
        self.auth = self.__parse_auth(auth)
        self.dataformat = self.__configure_format(dataformat)
        

    def get_rows(self, format="default"):
        '''Gets the amount of rows for the specified request from the AT Internet API

        Parameters
        ----------
        format : str, optional
            Format of the data to be retrieved (default is inherited from Class configuration)

        Returns
        -------
        response
            returns response of the request 
        '''

        # use format from paramter or else the default format
        rowcount_format = self.__configure_format(self.dataformat, "rowcount") if format=="default" else self.__configure_format(format, "rowcount")
        rowcount_params = self.params.copy()
        rowcount_params.update({"max-results" : "1", "page-num" : "1"})

        return self.__call_api("getrowcount", rowcount_format, rowcount_params)


    def get_maxdate(self, format="default"):
        '''Gets the ISO time until which data is already available today

        Parameters
        ----------
        format : str, optional
            Format of the data to be retrieved (default is inherited from Class configuration)

        Returns
        -------
        response
            returns response of the request 
        '''

        # use format from paramter or else the default format
        maxdate_format = self.__configure_format(self.dataformat, "maxdate") if format=="default" else self.__configure_format(format, "maxdate")
        # only space is needed for this request of the max date
        maxdate_params = {"space": self.params["space"]} 

        return self.__call_api("getmaxdate", maxdate_format, maxdate_params)


    def get_data(self, format="default"):
        '''Gets the data for the specified request from the AT Internet API'

        Parameters
        ----------
        format : str, optional
            Format of the data to be retrieved (default is inherited from Class configuration)

        Returns
        -------
        list
            returns list of responses
        '''

        # use format from paramter or else the default format
        data_format = self.dataformat if format=="default" else self.__configure_format(format)
        route = "getdata"
        result_list = [] 
        
        # check if all rows should be returned instead of selection within parameters
        if(self.allrows == True):
            # get amount of rows and calculate amount of pages whith equals the amount of api calls
            rowdata = json.loads(self.get_rows("json").text)
            if rowdata["ErrorCode"]:
                return [rowdata]
            rows = int(rowdata["RowCounts"][0]["RowCount"])   
            pages = int(math.ceil(rows / 10000))
            get_data_params = self.params.copy()

            for page in range(1, pages + 1):
                get_data_params.update({"max-results" : "10000", "page-num" : str(page)})
                res = self.__call_api(route, data_format, get_data_params)
                result_list.append(res)  

        else: 
            res = self.__call_api(route, data_format, self.params)
            result_list.append(res)

        return result_list


    def __call_api(self, route, format, params):
        url = "https://apirest.atinternet-solutions.com/data/v2/{}/{}?".format(format, route)
        # depending on authentification method a different requestes is done
        if self.auth_method == "header":
            return requests.request("GET", url, headers=self.auth, params=params)

        else:
            params["apikey"] = self.auth
            return requests.request("GET", url, params=params)


    def __parse_params(self, params):
        # if parameters are submitted as string they will be translated to a dictionary
        if isinstance(params, str) and (params.startswith("http")==False):
            params_object = {}
            if params.startswith("?"):
                params = params[1:]
            if params.startswith("&"):
                params = params[1:]
            params_list = params.split("&")
            for x in params_list:
                params_object[x.split("=", 1)[0]] = x.split("=", 1)[1]
            return params_object

        elif isinstance(params, dict):
            return params

        else:
            raise Exception("Parameters must either be a string separeted by '&' or a dictionary.")    


    def __parse_auth(self, auth):
        # check if authentification will be done via headers or apikey
        if auth.startswith("apikey"):
            self.auth_method = "apikey"
            return auth.split(":")[1]

        if auth.startswith("header"):
            self.auth_method = "header"
            auth = {
                'authorization': "Basic " + auth.split(":")[1]
            }   
            return auth

        else:
            raise Exception("Authentication string must start with either 'apikey:' or 'header:'.")


    def __configure_format(self, dataformat, request="default"):
        # check if valid strings for data format was submitted
        if (request == "rowcount") or (request == "maxdate"):
            if dataformat in Request.COMPATIBLE_FORMATS_ROWCOUNT_MAXDATE:
                return dataformat
            else:
                return "json"
        else:
            if dataformat in Request.COMPATIBLE_FORMATS_DATA:
                return dataformat
            else:
                return "json"
