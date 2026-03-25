import urllib.request
import json
try:
    url = "http://127.0.0.1:5000/api/payroll/employees/EMP001/detail"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as response:
        print("Status:", response.status)
        print("Response:", response.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
