import json
class AppStoreConfigs(object):
	def __init__(self, importa):
		if importa == 1:
			self.root_folder = "files/AppStore_Tracker/"
			self.common_file_name = 'files/Logs/UserLogs/' + 'appstorelog.json'
		else:
			self.root_folder = "../../files/AppStore_Tracker/"
			self.common_file_name = '../../files/Logs/UserLogs/' + 'appstorelog.json'
		self.toMonitorFileName = self.root_folder + 'appTrack.json'

		self.baseContent = props = {"user":{"telegram":{"chat_id":"","notifsEnabled":False,"first_name":"","last_name":"","username":""},"email":{"enabled":False,"address":""}},"urls":[]}
		

		self.backStr = "🔙Indietro🔙"


	def readContentOfFile(self):
		file = open(self.toMonitorFileName)
		content = json.load(file)
		file.close()
		return content

	def writeContentOfFile(self,content):
		file = open(self.toMonitorFileName,'w')
		json.dump(content, file, indent=4)
		file.close()
		return content

	def isUserJustInFile(self, first_name, last_name):
		users = self.contentOfFile['toTrack']
		for user in users:
			telegramUser = user['user']['telegram']
			if telegramUser['first_name'] == first_name and telegramUser['last_name'] == last_name:	return True
		return False

	def makeUser(self, first_name, last_name, chat_id, username):
		toAdd = self.baseContent
		toAdd['user']['telegram']['first_name'] = first_name
		toAdd['user']['telegram']['last_name'] = last_name
		toAdd['user']['telegram']['chat_id'] = chat_id
		toAdd['user']['telegram']['username'] = username
		self.contentOfFile['toTrack'].append(toAdd)
		self.contentOfFile = self.writeContentOfFile(self.contentOfFile)

	""" Ritorna l'indice dell'utente all'interno del file """
	def getIdxOfUserInFile(self, first_name, last_name):
		users = self.contentOfFile['toTrack']
		for i in range(len(users)):
			telegramUser = users[i]['user']['telegram']
			if telegramUser['first_name'] == first_name and telegramUser['last_name'] == last_name:	return i
		return -2

	""" Verifica se l'utente sta già monitorando il prodotto"""
	def isUserJustMonitorThisProduct(self, url,first_name, last_name):
		userIdxInFile = self.getIdxOfUserInFile(first_name, last_name)
		user = self.contentOfFile['toTrack'][userIdxInFile]['urls']
		for urlInFIle in user:
			if url in urlInFIle['url']:	return True
		return False

	""" Verifica che l'utente sia nel file e aggiunge i dettagli di viò che vuole monitorare"""
	def addDetailsOnFile(self, details, first_name, last_name, chat_id, username):
		url = details['url']
		contentOfFile = self.contentOfFile
		if self.isUserJustInFile(first_name, last_name):
			# verifica se già sta monitorando l'url
			if not self.isUserJustMonitorThisProduct(url, first_name, last_name):
				idxOfUserInFile = self.getIdxOfUserInFile(first_name, last_name)
				contentOfFile['toTrack'][idxOfUserInFile]['urls'].append(details)
				self.contentOfFile = self.writeContentOfFile(contentOfFile)
			else:
				pass
				#print("Già stai monitorando questo prodotto")
		else:
			# crea un utente e aggiungi i dettagli
			self.makeUser(first_name, last_name, chat_id, username)
			idxOfUserInFile = self.getIdxOfUserInFile(first_name, last_name)
			contentOfFile['toTrack'][idxOfUserInFile]['urls'].append(details)
			self.contentOfFile = self.writeContentOfFile(contentOfFile)

	""" Rimuove tutto il dizionario che contiene i dettagli del monitor passando solo l'url"""
	def removeDetailsOnFileByURL(self, url, first_name, last_name):
		contentOfFile = self.contentOfFile
		idxOfUserInFile = self.getIdxOfUserInFile(first_name, last_name)

		# prima prendo l'indice dei dettagli che contiene l'url
		detailsOfThisUser = contentOfFile['toTrack'][idxOfUserInFile]['urls']
		
		trueIdx = -1
		for idx in range(len(detailsOfThisUser)):
			if url in detailsOfThisUser[idx]['url']:	trueIdx = idx

		if trueIdx != -1:	# found
			del detailsOfThisUser[trueIdx]
			if detailsOfThisUser == []:
				del contentOfFile['toTrack'][idxOfUserInFile]
			self.contentOfFile = self.writeContentOfFile(contentOfFile)
		else:	pass	# not found

	"""Ritorna la lista contenente tutti gli url dei prodotti che l'utente sta monitorando"""
	def getListOfSitesByUser(self, first_name, last_name):
		contentOfFile = self.contentOfFile
		idxOfUserInFile = self.getIdxOfUserInFile(first_name, last_name)
		detailsOfThisUser = contentOfFile['toTrack'][idxOfUserInFile]['urls']
		toRet = []
		for item in detailsOfThisUser:	toRet.append(item['url'])
		return toRet

	"""Ritorna la lista contenente tutte le descrizioni dei prodotti che l'utente sta monitorando"""
	def getNamesOfAllSitesByUser(self, first_name, last_name):
		contentOfFile = self.contentOfFile
		idxOfUserInFile = self.getIdxOfUserInFile(first_name, last_name)
		if idxOfUserInFile != -2:
			detailsOfThisUser = contentOfFile['toTrack'][idxOfUserInFile]['urls']
			toRet = []
			for item in detailsOfThisUser:	toRet.append(item['name'])
			return toRet
		return []

	"""Ritorna la lista di tuple contenente tutte le descrizioni dei prodotti che l'utente sta monitorando"""
	def getNamesPriceOfAllSitesByUser(self, first_name, last_name):
		contentOfFile = self.contentOfFile
		idxOfUserInFile = self.getIdxOfUserInFile(first_name, last_name)
		if idxOfUserInFile != -2:
			detailsOfThisUser = contentOfFile['toTrack'][idxOfUserInFile]['urls']
			toRet = []
			for item in detailsOfThisUser:	toRet.append((item['name'], item['price']))
			return toRet
		return []

	def fromNameOfSiteToLink(self, nameOfSite, first_name, last_name):
		userSitesUrl = self.getListOfSitesByUser(first_name, last_name)
		userSitesDescr = self.getNamesOfAllSitesByUser(first_name, last_name)
		trueIdx = -1
		for idx in range(len(userSitesDescr)):
			if nameOfSite == userSitesDescr[idx]:	trueIdx = idx
		return userSitesUrl[trueIdx]

	def getShortestString(self, stringa, length=30, suffix='...'):
		if len(stringa) <= length:	return stringa
		return ' '.join(stringa[:length+1].split(' ')[0:-1]) + suffix

	""" Ritorna una lista di tuple composte da (name, price, url)"""
	def getTupleOfSiteToMonitor(self):	
		contentOfFile = self.contentOfFile['toTrack']
		toRet = []
		for track in contentOfFile:
			urls = track['urls']
			for singleUrl in urls:
				toRet.append((singleUrl['name'], singleUrl['price'], singleUrl['url']))
		return toRet

	""" Ritorna una lista di tuple contenti le info dell'utente che sta monitorando quell'url"""
	def whoIsMonitoringThisUrl(self, url):
		userDetails = []
		i = 0
		for item in self.contentOfFile['toTrack']:
			found = False
			for url_in_file in item['urls']:
				if url_in_file['url'] == url:	found = True
			if found:
				chat_id = item['user']['telegram']['chat_id']
				first_name = item['user']['telegram']['first_name']
				last_name = item['user']['telegram']['last_name']
				last_name = last_name if last_name != None else ''
				tupla = (chat_id, first_name,last_name)
				userDetails.append(tupla)
			i = i+1
		return userDetails

	def fromUrlToDesct(self, url):
		for item in self.contentOfFile['toTrack']:
			for url_in_file in item['urls']:
				if url_in_file['url'] == url:	return url_in_file['name']

	def fromUrlToPrice(self, url):
		for item in self.contentOfFile['toTrack']:
			for url_in_file in item['urls']:
				if url_in_file['url'] == url:	return url_in_file['price']

	def areThereProductToMonitor(self):
		content = self.getTupleOfSiteToMonitor()
		if len(content) != 0:	return True
		return False

	
	""" Scrive un file in comune per le notifiche del bot"""
	def write_common_file(self, url , newPrice):
		file = open(self.common_file_name)
		contentOfFile = json.load(file)
		file.close()
		nameOfObject = self.fromUrlToDesct(url)
		oldPrice = self.fromUrlToPrice(url)

		contentOfFile['changed'] = True
		toAppend = {'name':nameOfObject, 'url':url, 'newPrice':newPrice, 'oldPrice':oldPrice}
		contentOfFile['productsChanged'].append(toAppend)

		file = open(self.common_file_name,'w')
		json.dump(contentOfFile, file, indent=4)
		file.close()

		self.updatePriceInLocalFile(url, newPrice)

	""" Resetta il contenuto del file in comune"""
	def resetCommonFileName(self):
		toWrite = {"changed":False, "productsChanged":[]}
		file = open(self.common_file_name,'w')
		json.dump(toWrite, file, indent=4)
		file.close()

	""" Aggiorna il prezzo del prodotto nel file toTrack.json"""
	def updatePriceInLocalFile(self, url, newPrice):
		fileContent = self.contentOfFile
		contentOfFile = fileContent['toTrack']
		for item in contentOfFile:
			for product in item['urls']:
				if product['url'] == url:	product['price'] = newPrice
		self.contentOfFile = self.writeContentOfFile(fileContent)


	def stringContainsID(self, stringa):
		if 'id' in stringa:	return True
		return False


	def get_details_of_apps_by_user(self, first_name, last_name):
		userIdxInFile = self.getIdxOfUserInFile(first_name, last_name)
		return self.contentOfFile['toTrack'][userIdxInFile]['urls']

	def getShortestString(self, stringa, length=30, suffix='...'):
		if len(stringa) <= length:	return stringa
		return ' '.join(stringa[:length+1].split(' ')[0:-1]) + suffix

	def better_print_list(self, first_name, last_name):
		to_print = ""
		apps_list = self.get_details_of_apps_by_user(first_name, last_name)

		for item in apps_list:
			app_name, app_price, app_url = item['name'], item['price'], item['url']
			to_print += '・%s (%s) - %s€\n' % (self.getShortestString(app_name, 18), app_url, str(app_price))
		return to_print



if __name__ == '__main__':
	AppStoreConfigs = AppStoreConfigs(2)
	x = AppStoreConfigs.getNamesOfAllSitesByUser("No", "Name")	
	print(x)