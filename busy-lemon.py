import io
import random
from sys import exit
from random import randint

class Attribute:
	def __init__(self, id, name):
		self.id = id
		self.name = name

class Activity:
	def __init__(self, id, name):
		self.id = id
		self.name = name
		self.attrs = []

attributes = []
activities = []

DBG = False

def getAttribute(attrId):
	for a in attributes:
		if a.id == attrId:
			return a
	return None

def getActivity(id):
	for a in activities:
		if a.id == id:
			return a
	return None

class History:
	def __init__(self):
		self.done = []
		historyCandidate = None
		
		self.load()
		self.normalize()
	
	def load(self):
		with io.open('history.txt', encoding='utf-8') as f:
			data = f.readlines()
			if not data:
				return

			l1 = data[0].strip()
			l2 = data[1].strip() if len(data) > 1 else None
			
			for activityStr in l1.split(' '):
				if activityStr and not activityStr.isspace():
					self.done.append(int(activityStr))
			
			if l2 and not l2.isspace():
				historyCandidate = int(l2)
				
				while True:
					print('Did you finish', getActivity(historyCandidate).name + '? (y/n)')
					
					answer = input()
					if answer == 'y':
						self.done.append(historyCandidate)
						historyCandidate = None
						break
					elif answer == 'n':
						historyCandidate = None
						break
					else:
						continue
	
	def save(self):
		with io.open('history.txt', 'w', encoding='utf-8') as f:
			for d in self.done:
				f.write(str(d))
				f.write(' ')
			f.write('\n')
			if self.historyCandidate:
				f.write(str(self.historyCandidate))
	
	def normalize(self):
		self.done.reverse()
		
		newDone = []
		
		for el in self.done:
			if el not in newDone:
				if getActivity(el) != None:
					newDone.append(el)
		
		newDone.reverse()
		self.done = newDone
	
	def printSelf(self):
		print('History')
		for a in self.done:
			print(a)
	
	def filter(self, attributeId = None):
		if attributeId == None:
			return self.done
		else:
			res = []
			for aId in self.done:
				activity = getActivity(aId)
				if activity and attributeId in activity.attrs:
					res.append(aId)
			return res

def init():
	ATTRIBUTES = 1
	ACTIVITIES = 2
	ACTIVITY_ATTRIBUTES = 3

	with io.open('topics.txt', encoding='utf-8') as f:
		data = f.readlines()
		
		state = 0
		
		for l in data:
			if l.isspace():
				continue
			if '[Attributes]' in l:
				state = ATTRIBUTES
				continue
			if '[Activities]' in l:
				state = ACTIVITIES
				continue

			if '\t' in l:
				state = ACTIVITY_ATTRIBUTES
			elif state == ACTIVITY_ATTRIBUTES:
				state = ACTIVITIES
			
			l = l.strip()
			
			if state == ATTRIBUTES or state == ACTIVITIES:
				spaceIdx = l.find(' ')
				id = int(l[0:spaceIdx])
				name = l[spaceIdx + 1:]
				if state == ATTRIBUTES:
					attributes.append(Attribute(id, name))
				elif state == ACTIVITIES:
					activities.append(Activity(id, name))
			elif state == ACTIVITY_ATTRIBUTES:
				activities[-1].attrs.append(int(l))

init()
history = History()

def chooseAttribute():
	print("\nChoose activity topic:")
	print("0 Any")
	for a in attributes:
		print(a.id, a.name)
	return int(input())

def chooseActivity(attributeId):
	
	choosenAttribute = getAttribute(attributeId)
	if choosenAttribute == None:
		attributeId = None
	
	allowedActivities = history.filter(attributeId) # in history ascending order
	if DBG:
		print('allowedActivities', allowedActivities)
	
	nonregisteredActivities = []
	for a in activities:
		if(
			(choosenAttribute != None and choosenAttribute.id not in a.attrs)
			or a.id in allowedActivities
		):
			continue
		nonregisteredActivities.append(a.id)
	
	random.shuffle(nonregisteredActivities)
	if DBG:
		print('nonregisteredActivities', nonregisteredActivities)
	
	if nonregisteredActivities:
		allowedActivities = nonregisteredActivities + allowedActivities
	
	if DBG:
		print('allowedActivities', allowedActivities)
	
	if not allowedActivities:
		return None
	
	accepted = False
	
	for a in allowedActivities:
		activity = getActivity(a)
		
		while True:
			print('\n' + activity.name + '? (y/n)')
			answer = input()
			if answer == 'y':
				accepted = True
				break
			elif answer == 'n':
				accepted = False
				break
			else:
				continue
		
		if accepted:
			break
		
	if accepted:
		return activity
	else:
		return None

chosenAttribute = chooseAttribute()
chosenActivity = chooseActivity(chosenAttribute);

if chosenActivity == None:
	print('\nNo activity! Try again')
	exit()
else:
	history.historyCandidate = chosenActivity.id
	print('\n' + chosenActivity.name + '. Enjoy')

history.save()
