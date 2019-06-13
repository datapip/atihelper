# atihelper
Python helper class to easily fetch data from AT Internet RESTful API.

## Usage
```python
import atihelper

# Authentification can be done via header containing base64 encoded 'email@email.com:password' string
# or an apikey retrieved from the AT Internet API Account interface - it is mandatory to indicate the used
# authentification method by either "header:" or "apikey:" prefix.
auth = "header:a1B2c3"
token = "apikey:ab-c12-3"

# Requested API can be parameter string or dictionary
params = "columns={d_visit_id,m_page_loads}&sort={-m_page_loads}&space={s:123456}&period={D:{start:'2018-12-31',end:'2018-12-31'}}"

# Create new instantiation of atihelper
ati_request = atihelper.Request(params, auth, allrows=True, dataformat="json")

# Get maxdate for specified API request - returns response
ati_request_maxdate = ati_request.get_maxdate()

# Get amount of rows for specified API request - returns response
ati_request_rowcount = ati_request.get_rows()

# Get data for specified API request - returns list of responses
ati_request_data = ati_request.get_data()

# Change parameter of exisiting instance
ati_request.params["space"] = "{s:654321}"
```

## Contribution
I am thankful for any feedback and improvements.

## License
This project is licensed under MIT License - see the [LICENSE.md](https://github.com/datapip/atihelper/blob/master/LICENSE) file for details 
