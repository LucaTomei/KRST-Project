import requests, json, time
from datetime import datetime

try:
	from .AppStoreConfigs import AppStoreConfigs
	importa = 1
except ImportError:
	from AppStoreConfigs import AppStoreConfigs
	importa = 2

class AppStoreTracker(object):
	def __init__(self, inputUrl = ''):
		self.inputUrl = inputUrl
		self.appId = self.getAppId()
		
		self.AppStoreConfigs = AppStoreConfigs(importa)

	def retrieveDATA(self):
		requestsURL = 'https://itunes.apple.com/lookup?id='+self.appId+'&country=it'
		
		try:
			response = requests.get(requestsURL)
			content = response.json()
			if content['resultCount'] > 0:	return content
			return None
		except:	return None

	def getAppId(self):
		idStr = self.inputUrl.split("/")[-1]
		if 'id' in idStr:	return idStr.split('id')[1].split('?')[0]
		return ''
	
	def getPriceOfThisApp(self, content):	return content['results'][0]['price']

	def getNameOfThisApp(self, content):	return content['results'][0]['trackName']

	def returnTuplaToMonitor(self):
		thisData = self.retrieveDATA()
		toRet = {'name':"", "price":0, "url":self.inputUrl}
		if thisData != None:
			name = self.getNameOfThisApp(thisData)
			price = self.getPriceOfThisApp(thisData)
			toRet['name'] = name
			toRet['price'] = price
			return toRet
		return None

	def main(self):
		listOfTuples = self.AppStoreConfigs.getTupleOfSiteToMonitor()
		for name, old_price, url in listOfTuples:
			self.inputUrl = url
			self.appId = self.getAppId()
			tuplaToMonitor = self.returnTuplaToMonitor()
			if tuplaToMonitor != None:
				new_price = tuplaToMonitor['price']
				if new_price < old_price:
					self.AppStoreConfigs.write_common_file(url, new_price)
					print("Prezzo diminuito, aggiorno il file locale e invio notifica")
				elif new_price > old_price:
					self.AppStoreConfigs.write_common_file(url, new_price)
					print("Prezzo aumentato, aggiorno il file locale")
				else:
					pass
					#print("Stesso Prezzo per "+ name +" ("+ str(new_price) +"), non faccio nulla")
			else:	pass	# non riesce a recuperare info sull'applicazione
			


if __name__ == '__main__':
	url = input()#"https://apps.apple.com/us/app/yahoo-weather/id628677149?uo=4&at=11l6hc&app=itunes&ct=fnd"
	AppStoreTrackerOBJ = AppStoreTracker(url)
	app_id = AppStoreTrackerOBJ.retrieveDATA()
	print("\nName:", app_id["results"][0]["trackName"])
	print("appSize:", app_id["results"][0]["fileSizeBytes"])
	print("hasUserRatingCount:", app_id["results"][0]["userRatingCount"])
	print("userRanking:", app_id["results"][0]["averageUserRating"])
	print("\tfirstVersionReleaseDate:", app_id["results"][0]["releaseDate"])
	print("\tcurrentVersionReleaseDate:", app_id["results"][0]["currentVersionReleaseDate"])