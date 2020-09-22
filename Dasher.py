import requests
import json
import sys
import constants

class Dasher(object):
	"""docstring for Dasher"""
	def __init__(self, authorizationToken):
		super(Dasher, self).__init__()
		# self.status = details["status"]
		self.generatedToken = authorizationToken

	def getDasherInfo(self):

		url = "https://api.doordash.com/v1/dashers/me/"
		headers = {'authorization': self.generatedToken}
		try:
			response = requests.request("GET", url, headers=headers)
		except:
			print e.cause
			sys.exit(1)

		data = json.loads(response.text)
		return data
		#return response.json()

	def getRatings(self):
		headers = {'authorization': self.generatedToken}
		try:
			response = requests.request("GET", constants.ratingsURL, headers=headers)
		except requests.exceptions.RequestException as e:
			print e.cause
			sys.exit(1)
		return response.json()

	def getEarnings(self):
		headers = {'authorization': self.generatedToken}
		try:
			response = requests.request("GET", constants.earningsURL, headers=headers)
		except requests.exceptions.RequestException as e:
			print e.cause
			sys.exit(1)
		return response.json()
		
	def getWeeklyEarnings(self):
		headers = {'authorization': self.generatedToken}
		try:
			response = requests.request("GET", constants.weeklyEarningsURL, headers=headers)
		except requests.exceptions.RequestException as e:
			print e.cause
			sys.exit(1)
		return response.json()
