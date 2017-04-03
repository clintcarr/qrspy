# import unittest
# import qrspy


# qrs = qrspy.ConnectQlik('qs2.qliklocal.net:4242', ('C:/certs/qs2.qliklocal.net/client.pem',
#                                       'C:/certs/qs2.qliklocal.net/client_key.pem'),
#            'C:/certs/qs2.qliklocal.net/root.pem')

# results = [{'buildVersion': '12.14.0.0', 'buildDate': '9/20/2013 10:09:00 AM', 'databaseProvider': 'Devart.Data.PostgreSql', 'nodeType': 1, 'sharedPersistence': True, 'requiresBootstrap': False, 'schemaPath': 'About'},
# 			[{'id': 'bbba08d3-42a8-42aa-8fe8-6660eb4edeed', 'name': 'Operations Monitor', 'appId': '', 'publishTime': '2017-01-18T21:41:38.860Z', 'published': True, 'stream': {'id': 'a70ca8a5-1d59-4cc9-b5fa-6e207978dcaf', 'name': 'Monitoring apps', 'privileges': None}, 'savedInProductVersion': '12.2.1', 'migrationHash': '82b8362010f6f32f12217392e08c75194db0d4fc', 'availabilityStatus': 0, 'privileges': None}]]

# class Qrspy(unittest.TestCase):

# 	def test_pingproxy(self):
# 		self.assertEqual(qrs.ping_proxy(), 200)

# 	def test_getabout(self):
# 		self.assertEqual(qrs.get_about(), results[0])

# 	def test_getapp(self):
# 		self.assertEqual(qrs.get_app('Name eq', 'Operations Monitor'), results[1])

# if __name__ == '__main__':
#     unittest.main(verbosity=2)

# print (results)

# server = 'qs2.qliklocal.net:4242'

# print (server[:server.index('4')]+str(4243))

# from httmock import urlmatch, HTTMock
# import requests

# # define matcher:
# @urlmatch(netloc=r'(.*\.)?google\.com$')
# def google_mock(url, request):
#     return 'Feeling lucky, punkjkjlk?'

# # open context to patch
# with HTTMock(google_mock):
#     # call requests
#     r = requests.get('http://google.com/')
# print (r.content)  # 'Feeling lucky, punk?'
# headers = {}

# # headers['User-Agent'] = '''Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'''

# # print (headers[''])

# import random
# import string
# characters = string.ascii_letters
# for i in range(25000):
# 	with open ('c:/dev/csv/newuser.txt', 'a') as user:
# 		user.write (''.join(random.sample(characters, 5)) + ',New,' + ''.join(random.sample(characters, 5)))


# 		imported 25000 users
# [Finished in 398.3s]


n = input('Enter number')
while n >= 0:
	print (n)