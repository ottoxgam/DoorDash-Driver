from User import User
from Dasher import Dasher
from terminaltables import AsciiTable
import requests
import sys
import datetime
import re
import csv
from docopt import docopt

class Dash(object):

	def __init__(self):
		super(Dash, self).__init__()
		self.dasherObject = None
		self.authorizationToken = None
		self.profileInformation = None
		self.weeklyEarningsArray = None

	def beginDashing(self, username, password):
		userObject = User()
		userObject.authenticate(username, password)
		self.authorizationToken = userObject.authorizationToken
		if self.authorizationToken != None:
			self.fetchDasherInfo()
			self.fetchRating()
			self.fetchEarnings()
		else:
			print "Could not find Log In."

	def fetchDasherInfo(self):
		dasherObject = Dasher(self.authorizationToken)
		data = dasherObject.getDasherInfo()
		#self.listDasherInfo(data)
		print ('------------------------------')
		print
		print ('Dasher Name: ' + (data['first_name']) + ' ' + (data['last_name']))
		print ('Phone Number: ' + (data['phone_number']))
		print ('Email: ' + (data['email']))
		print ('Dasher ID: ' + str((data['id'])))
		print
	def fetchRating(self):
		ratingObject = Dasher(self.authorizationToken)
		rating = ratingObject.getRatings()
		print ('------------------------------')
		print
		print ('Average Customer Rating: ' + (str(rating['new_recent_customer_rating'])))
		print ('Acceptance: ' + (str(round(rating["acceptance_rate"]*100.0, 2))))
		print ('Lifetime Deliveries: ' + (str(rating['num_lifetime_deliveries'])))
		print

	def fetchEarnings(self):
		earningObject = Dasher(self.authorizationToken)
		earnings = earningObject.getEarnings()
		earningsData = earningObject.getWeeklyEarnings()
		self.printWeeklyEarnings(earningsData)
		#self.printWeeklyTrends(earningsData)

	def printWeeklyEarnings(self,data):
		weeklyShifts = data["shifts"]
		resultArray = []
		headerArray = ["No","Start Time", "End Time", "# Deliveries", "Delivery Pay", "Tip Amount", "Boost Pay", "Total Pay", "Total Active Time", "Shift ID"]
		resultArray.append(headerArray)
		shiftNumber = -1
		for shifts in weeklyShifts:
			shiftDetails = []
			shiftNumber+=1
			shiftDetails.append(str(shiftNumber))
			shiftDetails.append(datetime.datetime.strptime((shifts["check_in_time"]), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%H:%M:%S %m-%d-%Y"))
			shiftDetails.append(datetime.datetime.strptime((shifts["check_out_time"]), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%H:%M:%S %m-%d-%Y"))
			shiftDetails.append(shifts["num_deliveries"])
			shiftDetails.append(("$%.2f") % (shifts["delivery_pay"]/100.0))
			shiftDetails.append(("$%.2f") % (shifts["tip_amount"]/100.0))
			shiftDetails.append(("$%.2f") % (shifts["boost_pay"]/100.0))
			shiftDetails.append(("$%.2f") % (shifts["total_pay"]/100.0))
			shiftDetails.append(str(datetime.timedelta(seconds=shifts["total_active_time"])))
			shiftDetails.append(shifts["id"])
			resultArray.append(shiftDetails)

		table = AsciiTable(resultArray)
		print ('------------------------------')
		print
		print (data['weekly_trend_data']['insight']['title'])
		print table.table
		print ("Updated at: ") + str((data['weekly_trend_data']['updated_at']))

		file = open('dd_earnings.csv', 'w+')
		with file:
    			write = csv.writer(file)
    			write.writerows(resultArray)



	def printWeeklyTrends(self,data):
		monthlyTrend = (data["weekly_trend_data"]["monthly_data_points"])
		resultArray = []
		headerArray = ["Month", " week1", "week2"]
		resultArray.append(headerArray)
		month = -1
		week = -1
		#print weeklyTrend[month]
		for monthly_data_points in monthlyTrend: #enumerate months
			monthDetails = []
			month+=1
			week+=1
			monthDetails.append(monthlyTrend[month]['month'])
			monthDetails.append(monthlyTrend[month]['weekly_data_points'][0]['week_total_pay'])
			monthDetails.append(gotdata)
			resultArray.append(monthDetails)

		table = AsciiTable(resultArray)
		print ('------------------------------')
		print table.table



def main():
	if len(sys.argv) <= 2:
		print "Please enter your username and password seperated by space."
		return

	dashObject = Dash()
	dashObject.beginDashing(str(sys.argv[1]), str(sys.argv[2]))

main()
