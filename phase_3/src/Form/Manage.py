from ..Handlers.DBInteraction import *
from ..Common import DBTypes
from . import ValueCheck
import traceback

Action = DBTypes.EnumReq.Action
Fields = DBTypes.EnumReq.Fields
ResFields = DBTypes.EnumRes

def getEqEntry(m):
	# None if EqKey given is invalid for edit or Entry if valid
	# latest key for insert
	if m.mode:
		request = DBTypes.Request(
			Action.Manage.Eq_Get,
			{
				Fields.Manage.EqKey: m.eqkey
			}
		)
		result = m.dbi.complete(request)
		if(len(result[ResFields.Earthquake.Key]) == 0):
			result = None
		else:
			result[ResFields.Earthquake.Key] = result[ResFields.Earthquake.Key][0]
			result[ResFields.Earthquake.Time] = result[ResFields.Earthquake.Time][0]
			result[ResFields.Earthquake.Longitude] = result[ResFields.Earthquake.Longitude][0]
			result[ResFields.Earthquake.Latitude] = result[ResFields.Earthquake.Latitude][0]
			result[ResFields.Earthquake.Depth] = result[ResFields.Earthquake.Depth][0]
			result[ResFields.Earthquake.Mag] = result[ResFields.Earthquake.Mag][0]
			result[ResFields.Earthquake.Type] = result[ResFields.Earthquake.Type][0]
			result[ResFields.Earthquake.CityKey] = result[ResFields.Earthquake.CityKey][0]
	else:
		request = DBTypes.Request(
			Action.Manage.Eq_GetLatestKey,
			{
			}
		)
		result = m.dbi.complete(request)
		result[ResFields.Earthquake.Key] = result[ResFields.Earthquake.Key][0]
	return result

def getNeEntry(m):
	assert isinstance(m, Manage)
	if m.mode:
		if m.current_eqentry is not None:
			request_key = DBTypes.Request(
				Action.Manage.Ne_GetKey,
				{
					Fields.Manage.EqKey: m.current_eqentry[ResFields.Earthquake.Key]
				}
			)
			result_key = m.dbi.complete(request_key)
			if(len(result_key[ResFields.Nuclear.Key]) == 0):
				result = None
			else:
				request = DBTypes.Request(
					Action.Manage.Ne_Get,
					{
						Fields.Manage.NeKey: result_key[ResFields.Nuclear.Key][0]
					}
				)
				result = m.dbi.complete(request)
				result[ResFields.Nuclear.Key] = result[ResFields.Nuclear.Key][0]
				result[ResFields.Nuclear.NationKey] = result[ResFields.Nuclear.NationKey][0]
				result[ResFields.Nuclear.Yield] = result[ResFields.Nuclear.Yield][0]
				result[ResFields.Nuclear.EarthquakeKey] = result[ResFields.Nuclear.EarthquakeKey][0]
		else:
			result = None
	else:
		result = None
	return result

def getEqSrcs(m):
	assert isinstance(m, Manage)
	if m.mode:
		if m.current_eqentry is not None and ResFields.Earthquake.Time in m.current_eqentry:
			request = DBTypes.Request(
				Action.Manage.EqSrc_Get,
				{
					Fields.Manage.EqKey: m.current_eqentry[ResFields.Earthquake.Key]
				}
			)
			result = m.dbi.complete(request)
			return result
		else:
			result = None
	else:
		result = None
	return result

def getNeSrcs(m):
	assert isinstance(m, Manage)
	if m.mode:
		if m.current_neentry is not None and ResFields.Nuclear.Yield in m.current_neentry:
			request = DBTypes.Request(
				Action.Manage.NeSrc_Get,
				{
					Fields.Manage.NeKey: m.current_neentry[ResFields.Nuclear.Key]
				}
			)
			result = m.dbi.complete(request)
			return result
		else:
			result = None
	else:
		result = None
	return result

def getSelectionList(m):
	# earthquake types
	req_types = DBTypes.Request(
		Action.Options.Eq_Types,
		{
		}
	)
	res_types = m.dbi.complete(req_types)
	# nations
	req_nations = DBTypes.Request(
		Action.Options.Location_AllNations,
		{
		}
	)
	res_nations = m.dbi.complete(req_nations)
	# earthquake sources
	req_eqsrcs = DBTypes.Request(
		Action.Options.Eq_Srcs,
		{
		}
	)
	res_eqsrcs = m.dbi.complete(req_eqsrcs)
	# nuclear sources
	req_nesrcs = DBTypes.Request(
		Action.Options.Ne_Srcs,
		{
		}
	)
	res_nesrcs = m.dbi.complete(req_nesrcs)

	return {
		'types': res_types,
		'nations': res_nations,
		'eqsrcs': res_eqsrcs,
		'nesrcs': res_nesrcs
	}

def getCurrentSelection(m):
	assert isinstance(m, Manage)
	typeIndex = None
	eqsrcs = None
	nationIndex = None
	nesrcs = None

	if m.current_eqentry is not None and ResFields.Earthquake.Time in m.current_eqentry:
		
		typesList = m.selectionList['types'][ResFields.Earthquake.Type]
		typeSelected = m.current_eqentry[ResFields.Earthquake.Type]
		for i in range(len(typesList)):
			if(typesList[i] == typeSelected):
				typeIndex = i
	
		eqsrcs = []
		eqsrcsList = m.selectionList['eqsrcs'][ResFields.EarthquakeSource.Key]
		eqsrcsSelected = m.current_eqsrcs[ResFields.EarthquakeSourceMapping.SourceKey]
		for i in range(len(eqsrcsList)):
			for j in range(len(eqsrcsSelected)):
				if(eqsrcsList[i] == eqsrcsSelected[j]):
					eqsrcs = eqsrcs + [i]

	if m.current_neentry is not None and ResFields.Nuclear.Yield in m.current_neentry:

		nationsList = m.selectionList['nations'][ResFields.Nation.Key]
		nationSelected = m.current_neentry[ResFields.Nuclear.NationKey]
		for i in range(len(nationsList)):
			if(nationsList[i] == nationSelected):
				nationIndex = i

		nesrcs = []
		nesrcsList = m.selectionList['nesrcs'][ResFields.NuclearSource.Key]
		nesrcsSelected = m.current_nesrcs[ResFields.NuclearSourceMapping.SourceKey]
		for i in range(len(nesrcsList)):
			for j in range(len(nesrcsSelected)):
				if(nesrcsList[i] == nesrcsSelected[j]):
					nesrcs = nesrcs + [i]
	
	return {
		'type': typeIndex,
		'nation': nationIndex,
		'eqsrcs': eqsrcs,
		'nesrcs': nesrcs
	}

def validateOptions(m,
	year, month, day, hour, minute, second,
	longitude, latitude, depth,
	magnitude, eqtype, nation, yieldVal
):
	msg = ""
	if not ValueCheck.isValidYear(year):
		msg = msg + "year is not valid\n"
	if not ValueCheck.isValidMonth(month):
		msg = msg + "month is not valid\n"
	if not ValueCheck.isValidDay(month, day):
		msg = msg + "day is not valid\n"
	if not ValueCheck.isValidHour(hour):
		msg = msg + "hour is not valid\n"
	if not ValueCheck.isValidMinute(minute):
		msg = msg + "minute is not valid\n"
	if not ValueCheck.isValidSecond(second):
		msg = msg + "second is not valid\n"
	if not ValueCheck.isValidLongitude(longitude):
		msg = msg + "longitude is not valid\n"
	if not ValueCheck.isValidLatitude(latitude):
		msg = msg + "latitude is not valid\n"
	if not ValueCheck.isValidDepth(depth):
		msg = msg + "depth is not valid\n"
	if not ValueCheck.isValidMag(magnitude):
		msg = msg + "mag is not valid\n"
	if (not yieldVal is None) and (not ValueCheck.isValidYield(yieldVal)):
		msg = msg + "yield is not valid\n"
	if not eqtype in m.selectionList['types'][ResFields.Earthquake.Type]:
		msg = msg + "type is not valid\n"
	if (not nation is None) and (not nation in m.selectionList['nations'][ResFields.Nation.Name]):
		msg = msg + "nation is not valid\n"

	if msg == "":
		return None
	else:
		return msg

def commit(
	m,
	year, month, day, hour, minute, second,
	longitude, latitude, depth,
	magnitude, eqtype, nation, yieldVal,
	eqsrcIndexes, nesrcIndexes
):
	assert isinstance(m, Manage)
	"""
	EDIT
		UPDATE EARTHQUAKE
			REMOVE ALL EQSRC
			ADD EQSRC
		NUCLEAR
			REMOVE IF NOT NUCLEAR
				REMOVE ALL NESRC
			UPDATE IF STILL NUCLEAR
				REMOVE ALL NESRC
				ADD NESRC
			ADD NUCLEAR
				ADD NESRC
	INSERT
		ADD EARTHQUAKE
			ADD EQSRC
		ADD NUCLEAR
			ADD NESRC
	"""
	julian = ValueCheck.datetimeToJulian(int(year), int(month), int(day), int(hour), int(minute), int(second))
	longitude = float(longitude)
	latitude = float(latitude)
	depth = float(depth)
	magnitude = float(magnitude)
	eqtype = eqtype
	if nation is not None:
		nationkey = m.selectionList['nations'][ResFields.Nation.Key][m.selectionList['nations'][ResFields.Nation.Name].index(nation)]
	if yieldVal is not None:
		yieldVal = float(yieldVal)
	eqsrcKeys = list(map(
		lambda i: m.selectionList['eqsrcs'][ResFields.EarthquakeSource.Key][i],
		eqsrcIndexes
	))
	if nesrcIndexes is not None:
		nesrcKeys = list(map(
			lambda i: m.selectionList['nesrcs'][ResFields.NuclearSource.Key][i],
			nesrcIndexes
		))
	
	neededChanges = []
	if(m.current_eqentry is not None and ResFields.Earthquake.Time in m.current_eqentry):
		neededChanges.append("UPDATE_EQ")
		neededChanges.append("REMOVE_EQSRC")
		neededChanges.append("ADD_EQSRC")
		if(m.current_neentry is not None and ResFields.Nuclear.Yield in m.current_neentry):
			if(eqtype != "nuclear explosion"):
				neededChanges.append("REMOVE_NESRC")
				neededChanges.append("REMOVE_NE")
			else:
				neededChanges.append("UPDATE_NE")
				neededChanges.append("REMOVE_NESRC")
				neededChanges.append("ADD_NESRC")
		else:
			if(eqtype != "nuclear explosion"):
				pass
			else:
				neededChanges.append("ADD_NE")
				neededChanges.append("ADD_NESRC")
	else:
		neededChanges.append("ADD_EQ")
		neededChanges.append("ADD_EQSRC")
		if(eqtype == "nuclear explosion"):
			neededChanges.append("ADD_NE")
			neededChanges.append("ADD_NESRC")

	print('In Manage.py:', neededChanges)

	try:
		for change in neededChanges:
			if change == "UPDATE_EQ":
				request = DBTypes.Request(
					Action.Manage.Eq_Update,
					{
						Fields.Manage.EqTime: julian,
						Fields.Manage.EqLongitude: longitude,
						Fields.Manage.EqLatitude: latitude,
						Fields.Manage.EqDepth: depth,
						Fields.Manage.EqMag: magnitude,
						Fields.Manage.EqType: eqtype,
						Fields.Manage.EqKey: m.current_eqentry[ResFields.Earthquake.Key]
					}
				)
				m.dbi.complete(request)
			elif change == "ADD_EQ":
				request = DBTypes.Request(
					Action.Manage.Eq_Insert,
					{
						Fields.Manage.EqTime: julian,
						Fields.Manage.EqLongitude: longitude,
						Fields.Manage.EqLatitude: latitude,
						Fields.Manage.EqDepth: depth,
						Fields.Manage.EqMag: magnitude,
						Fields.Manage.EqType: eqtype
					}
				)
				m.dbi.complete(request)
			elif change == "REMOVE_EQSRC":
				request = DBTypes.Request(
					Action.Manage.EqSrc_RemoveAll,
					{
						Fields.Manage.EqKey: m.current_eqentry[ResFields.Earthquake.Key]
					}
				)
				m.dbi.complete(request)
			elif change == "ADD_EQSRC":
				for i in eqsrcKeys:
					request = DBTypes.Request(
						Action.Manage.EqSrc_Add,
						{
							Fields.Manage.EqKey: m.current_eqentry[ResFields.Earthquake.Key],
							Fields.Manage.EqSrcKey: i
						}
					)
					m.dbi.complete(request)
			elif change == "ADD_NE":
				request = DBTypes.Request(
					Action.Manage.Ne_Insert,
					{
						Fields.Manage.NeNationKey: nationkey,
						Fields.Manage.NeYield: yieldVal,
						Fields.Manage.EqKey: m.current_eqentry[ResFields.Earthquake.Key]
					}
				)
				m.dbi.complete(request)
				request = DBTypes.Request(
					Action.Manage.Ne_GetLatestKey,
					{
					}
				)
				result = m.dbi.complete(request)
				m.current_neentry = {ResFields.Nuclear.Key: result[ResFields.Nuclear.Key][0]}
			elif change == "UPDATE_NE":
				request = DBTypes.Request(
					Action.Manage.Ne_Update,
					{
						Fields.Manage.NeNationKey: nationkey,
						Fields.Manage.NeYield: yieldVal,
						Fields.Manage.NeKey: m.current_neentry[ResFields.Nuclear.Key]
					}
				)
				m.dbi.complete(request)
			elif change == "REMOVE_NE":
				request = DBTypes.Request(
					Action.Manage.Ne_Delete,
					{
						Fields.Manage.NeKey: m.current_neentry[ResFields.Nuclear.Key]
					}
				)
				m.dbi.complete(request)
			elif change == "REMOVE_NESRC":
				request = DBTypes.Request(
					Action.Manage.NeSrc_RemoveAll,
					{
						Fields.Manage.NeKey: m.current_neentry[ResFields.Nuclear.Key]
					}
				)
				m.dbi.complete(request)
			elif change == "ADD_NESRC":
				for i in nesrcKeys:
					request = DBTypes.Request(
						Action.Manage.NeSrc_Add,
						{
							Fields.Manage.NeKey: m.current_neentry[ResFields.Nuclear.Key],
							Fields.Manage.NeSrcKey: i
						}
					)
					m.dbi.complete(request)
			else:
				raise ValueError("Unhandled Change " + change)
		return [True]
	except Exception as e:
		print(e)
		traceback.print_exc()
		return [False, e]

def getDate(m):
	if m.current_eqentry is not None and ResFields.Earthquake.Time in m.current_eqentry:
		result = ValueCheck.julianToDatetime(m.current_eqentry[ResFields.Earthquake.Time])
	else:
		result = None
	return result

class Manage(object):

	def __init__(self, dbi, eqkey = None):
		assert isinstance(dbi, DBInteraction)
		# None = insert
		self.eqkey = eqkey
		# True if edit, False if insert
		self.mode = not self.eqkey is None
		self.dbi = dbi

		self.current_eqentry = getEqEntry(self)
		self.current_neentry = getNeEntry(self)
		self.current_eqsrcs = getEqSrcs(self)
		self.current_nesrcs = getNeSrcs(self)

		self.selectionList = getSelectionList(self)
		self.current_selection = getCurrentSelection(self)
		self.current_date = getDate(self)

	def getSelectionList(self):
		return self.selectionList

	def getEqEntry(self):
		return self.current_eqentry

	def getNeEntry(self):
		return self.current_neentry
	
	def getEqSrcs(self):
		return self.current_eqsrcs
	
	def getNeSrcs(self):
		return self.current_nesrcs

	def getCurrentSelection(self):
		return self.current_selection

	def getDate(self):
		return self.current_date

	def validateOptions(self,
		year, month, day, hour, minute, second,
		longitude, latitude, depth,
		magnitude, eqtype, nation, yieldVal
	):
		return validateOptions(
			self, year, month, day, hour, minute, second,
			longitude, latitude, depth,
			magnitude, eqtype, nation, yieldVal
		)

	def commit(self,
		year, month, day, hour, minute, second,
		longitude, latitude, depth,
		magnitude, eqtype, nation, yieldVal,
		eqsrcIndexes, nesrcIndexes
	):
		return commit(
			self,
			year, month, day, hour, minute, second,
			longitude, latitude, depth,
			magnitude, eqtype, nation, yieldVal,
			eqsrcIndexes, nesrcIndexes
		)


def test_1():
	print("test 1...")
	dbi = DBInteraction(r'data/data.sqlite')
	m = Manage(dbi, 39486)
	print(m.getEqEntry())
	print(m.getNeEntry())
	print(m.getSelectionList())
	print(m.getEqSrcs())
	print(m.getNeSrcs())
	print(m.getCurrentSelection())
	print(m.getDate())

if __name__ == "__main__":
	test_1()