# import requests
# url = 'http://lef1.qliktech.com/manuallef/default.aspx'
# payload = {'serial':9999000000001069}
# r = requests.post(url, params=payload)


 
import mechanize
br = mechanize.Browser()
br.open("http://lef1.qliktech.com/manuallef/default.aspx")
for f in br.forms():
    print (f)