from ..Handlers.DBInteraction import *
from ..Common import DBTypes
from . import ValueCheck
from . import ViewGraphGen
import traceback
from time import gmtime, strftime

Action = DBTypes.EnumReq.Action
Fields = DBTypes.EnumReq.Fields
ResFields = DBTypes.EnumRes

def findIndex(listToSearch, val):
	try:
		return listToSearch.index(val)
	except ValueError as e:
		return -1

def getSelectionList(v):
	# earthquake types
	req_types = DBTypes.Request(
		Action.Options.Eq_Types,
		{
		}
	)
	res_types = v.dbi.complete(req_types)
	# nations
	req_nations = DBTypes.Request(
		Action.Options.Location_AllNations,
		{
		}
	)
	res_nations = v.dbi.complete(req_nations)
	# earthquake sources
	req_eqsrcs = DBTypes.Request(
		Action.Options.Eq_Srcs,
		{
		}
	)
	res_eqsrcs = v.dbi.complete(req_eqsrcs)
	# nuclear sources
	req_nesrcs = DBTypes.Request(
		Action.Options.Ne_Srcs,
		{
		}
	)
	res_nesrcs = v.dbi.complete(req_nesrcs)

	return {
		'types': res_types,
		'nations': res_nations,
		'eqsrcs': res_eqsrcs,
		'nesrcs': res_nesrcs
	}

def getLocationSelectionList(v, r_name = '...', n_name = '...', s_name = '...', c_name = '...'):

	# region
	req_regions = DBTypes.Request(
		Action.Options.Location_Regions,
		{
		}
	)
	res_regions = v.dbi.complete(req_regions)
	res_regions[ResFields.Region.Name].insert(0,"...")
	res_regions[ResFields.Region.Key].insert(0,None)
	r_idx = findIndex(res_regions[ResFields.Region.Name], r_name)
	if r_idx == -1:
		r_name = "..."
		r_idx = 0
	r_key = res_regions[ResFields.Region.Key][r_idx]
	
	# nation
	if r_key is None:
		res_nations = {ResFields.Nation.Name: [], ResFields.Nation.Key: []}
		n_name = "..."
	else:
		req_nations = DBTypes.Request(
			Action.Options.Location_Nations,
			{
				Fields.Options.RegionKey: r_key
			}
		)
		res_nations = v.dbi.complete(req_nations)
	res_nations[ResFields.Nation.Name].insert(0,"...")
	res_nations[ResFields.Nation.Key].insert(0,None)
	n_idx = findIndex(res_nations[ResFields.Nation.Name], n_name)
	if n_idx == -1:
		n_name = "..."
		n_idx = 0
	n_key = res_nations[ResFields.Nation.Key][n_idx]

	# state
	if n_key is None:
		res_states = {ResFields.State.Name: [], ResFields.State.Key: []}
		s_name = "..."
	else:
		req_states = DBTypes.Request(
			Action.Options.Location_States,
			{
				Fields.Options.NationKey: n_key
			}
		)
		res_states = v.dbi.complete(req_states)
	res_states[ResFields.State.Name].insert(0,"...")
	res_states[ResFields.State.Key].insert(0,None)
	s_idx = findIndex(res_states[ResFields.State.Name], s_name)
	if s_idx == -1:
		s_name = "..."
		s_idx = 0
	s_key = res_states[ResFields.State.Key][s_idx]

	# city
	if s_key is None:
		res_cities = {ResFields.City.Name: [], ResFields.City.Key: []}
		c_name = "..."
	else:
		req_cities = DBTypes.Request(
			Action.Options.Location_Cities,
			{
				Fields.Options.StateKey: s_key
			}
		)
		res_cities = v.dbi.complete(req_cities)
	res_cities[ResFields.City.Name].insert(0,"...")
	res_cities[ResFields.City.Key].insert(0,None)
	c_idx = findIndex(res_cities[ResFields.City.Name], c_name)
	if c_idx == -1:
		c_name = "..."
		c_idx = 0
	c_key = res_cities[ResFields.City.Key][c_idx]

	locationType = 0
	locationKey = None
	if r_key is not None:
		locationType = 1
		locationKey = r_key
	if n_key is not None:
		locationType = 2
		locationKey = n_key
	if s_key is not None:
		locationType = 3
		locationKey = s_key
	if c_key is not None:
		locationType = 4
		locationKey = c_key

	return {
		'regions': res_regions,
		'nations': res_nations,
		'states': res_states,
		'cities': res_cities,
		ResFields.Region.Name: r_name,
		ResFields.Region.Key: r_key,
		'r_idx': r_idx,
		ResFields.Nation.Name: n_name,
		ResFields.Nation.Key: n_key,
		'n_idx': n_idx,
		ResFields.State.Name: s_name,
		ResFields.State.Key: s_key,
		's_idx': s_idx,
		ResFields.City.Name: c_name,
		ResFields.City.Key: c_key,
		'c_idx': c_idx,
		'locationType': locationType,
		'locationKey': locationKey
	}

def getGraphSelectionDictionary(v, isNationSpecified):
	if isNationSpecified:
		return {
			(0, 0): "Aggregate: Count",
			(0, 1): "Aggregate: Count per Population",
			(0, 3): "Aggregate: Max Magnitude",
			(0, 4): "Aggregate: Min Magnitude",
			(1, 0): "Trend: Count",
			(1, 1): "Trend: Count per Population",
			(1, 3): "Trend: Max Magnitude",
			(1, 4): "Trend: Min Magnitude"
		}
	else:
		return {
			(0, 0): "Aggregate: Count",
			(0, 1): "Aggregate: Count per Population",
			(0, 2): "Aggregate: Count per Area",
			(0, 3): "Aggregate: Max Magnitude",
			(0, 4): "Aggregate: Min Magnitude",
			(1, 0): "Trend: Count",
			(1, 1): "Trend: Count per Population",
			(1, 2): "Trend: Count per Area",
			(1, 3): "Trend: Max Magnitude",
			(1, 4): "Trend: Min Magnitude"
		}

def validateOptions(v,
	yearLow, yearHigh,
	magLow, magHigh,
	yieldLow, yieldHigh
):
	msg = ""
	if not ValueCheck.isValidYear(yearLow):
		msg = msg + "yearLow is not valid\n"
	if not ValueCheck.isValidYear(yearHigh):
		msg = msg + "yearHigh is not valid\n"
	if ValueCheck.isValidYear(yearLow) and ValueCheck.isValidYear(yearHigh) and int(yearLow) > int(yearHigh):
		msg = msg + "yearLow is higher than yearHigh\n"

	if not ValueCheck.isValidMag(magLow):
		msg = msg + "magLow is not valid\n"
	if not ValueCheck.isValidMag(magHigh):
		msg = msg + "magHigh is not valid\n"
	if ValueCheck.isValidMag(magLow) and ValueCheck.isValidMag(magHigh) and float(magLow) > float(magHigh):
		msg = msg + "magLow is higher than magHigh\n"

	if yieldLow is not None and yieldHigh is not None:
		if not ValueCheck.isValidYield(yieldLow):
			msg = msg + "yieldLow is not valid\n"
		if not ValueCheck.isValidYield(yieldHigh):
			msg = msg + "yieldHigh is not valid\n"
		if ValueCheck.isValidYield(yieldLow) and ValueCheck.isValidYield(yieldHigh) and float(yieldLow) > float(yieldHigh):
			msg = msg + "yieldLow is higher than yieldHigh\n"

	if msg == "":
		return None
	else:
		return msg

def commit(v,
	yearLow, yearHigh,
	magLow, magHigh,
	yieldLow, yieldHigh,
	eqtypeIndexes, eqsrcIndexes, nenationIndexes, nesrcIndexes,
	isView, graphSelection
):
	assert isinstance(v, ViewGraph)

	yearLow = int(yearLow)
	yearHigh = int(yearHigh)
	magLow = float(magLow)
	magHigh = float(magHigh)

	eqtypes = list(map(
		lambda i: v.selectionList['types'][ResFields.Earthquake.Type][i],
		eqtypeIndexes
	))
	eqsrcKeys = list(map(
		lambda i: v.selectionList['eqsrcs'][ResFields.EarthquakeSource.Key][i],
		eqsrcIndexes
	))
	nenationKeys = list(map(
		lambda i: v.selectionList['nations'][ResFields.Nation.Key][i],
		nenationIndexes
	))
	nesrcKeys = list(map(
		lambda i: v.selectionList['nesrcs'][ResFields.NuclearSource.Key][i],
		nesrcIndexes
	))

	isNuclear = None
	if len(eqtypes) == 1 and eqtypes[0] == 'nuclear explosion':
		yieldLow = float(yieldLow)
		yieldHigh = float(yieldHigh)
		isNuclear = True
	else:
		yieldLow = None
		yieldHigh = None
		nenationIndexes = None
		nesrcIndexes = None
		isNuclear = False
	
	if not isView:
		graphChoice = list(v.graphSelectionDictionary.keys())[findIndex(list(v.graphSelectionDictionary.values()), graphSelection)]

	try:

		if isView:
			if not isNuclear:
				request = DBTypes.Request(
					Action.Report.Eq,
					{
						Fields.Filter.YearRange: [yearLow, yearHigh],
						Fields.Filter.EqTypes: eqtypes,
						Fields.Filter.MagnitudeRange: [magLow, magHigh],
						Fields.Filter.EqSrcs: eqsrcKeys,
						Fields.Filter.Location: [v.locationSelectionList['locationType'], v.locationSelectionList['locationKey']]
					}
				)
				result = v.dbi.complete(request)
			else:
				request = DBTypes.Request(
					Action.Report.EqNe,
					{
						Fields.Filter.YearRange: [yearLow, yearHigh],
						Fields.Filter.EqTypes: eqtypes,
						Fields.Filter.MagnitudeRange: [magLow, magHigh],
						Fields.Filter.EqSrcs: eqsrcKeys,
						Fields.Filter.Location: [v.locationSelectionList['locationType'], v.locationSelectionList['locationKey']],
						Fields.Filter.NeNationKeys: nenationKeys,
						Fields.Filter.YieldRange: [yieldLow, yieldHigh],
						Fields.Filter.NeSrcs: nesrcKeys
					}
				)
				result = v.dbi.complete(request)
			fname = ViewGraphGen.showMap(result, isNuclear)
			retValue = [True, True, fname]
		else:
			if not isNuclear:
				request = DBTypes.Request(
					Action.Graph.Eq,
					{
						Fields.Filter.YearRange: [yearLow, yearHigh],
						Fields.Filter.EqTypes: eqtypes,
						Fields.Filter.MagnitudeRange: [magLow, magHigh],
						Fields.Filter.EqSrcs: eqsrcKeys,
						Fields.Filter.Location: [v.locationSelectionList['locationType'], v.locationSelectionList['locationKey']],
						Fields.Graph.Type: graphChoice[0],
						Fields.Graph.Value: graphChoice[1]
					}
				)
				result = v.dbi.complete(request)
			else:
				request = DBTypes.Request(
					Action.Graph.EqNe,
					{
						Fields.Filter.YearRange: [yearLow, yearHigh],
						Fields.Filter.EqTypes: eqtypes,
						Fields.Filter.MagnitudeRange: [magLow, magHigh],
						Fields.Filter.EqSrcs: eqsrcKeys,
						Fields.Filter.Location: [v.locationSelectionList['locationType'], v.locationSelectionList['locationKey']],
						Fields.Filter.NeNationKeys: nenationKeys,
						Fields.Filter.YieldRange: [yieldLow, yieldHigh],
						Fields.Filter.NeSrcs: nesrcKeys,
						Fields.Graph.Type: graphChoice[0],
						Fields.Graph.Value: graphChoice[1]
					}
				)
				result = v.dbi.complete(request)
			ViewGraphGen.showGraph(result, graphSelection)
			retValue = [True, False]
		print(result)
		return retValue
	except Exception as e:
		print(e)
		traceback.print_exc()
		return [False, e]

class ViewGraph(object):
	
	def __init__(self, dbi):
		assert isinstance(dbi, DBInteraction)
		self.dbi = dbi
		self.selectionList = getSelectionList(self)
		self.locationSelectionList = getLocationSelectionList(self)
		self.graphSelectionDictionary = getGraphSelectionDictionary(self, False)

	def updateLocationSelection(self, region, nation, state, city):
		self.locationSelectionList = getLocationSelectionList(self, region, nation, state, city)
		self.graphSelectionDictionary = getGraphSelectionDictionary(self, nation != "...")

	def validateOptions(self,
		yearLow, yearHigh,
		magLow, magHigh,
		yieldLow, yieldHigh
	):
		return validateOptions(self,
			yearLow, yearHigh,
			magLow, magHigh,
			yieldLow, yieldHigh
		)

	def commit(self,
		yearLow, yearHigh,
		magLow, magHigh,
		yieldLow, yieldHigh,
		eqtypeIndexes, eqsrcIndexes, nenationIndexes, nesrcIndexes,
		isView, graphSelection
	):
		return commit(self,
			yearLow, yearHigh,
			magLow, magHigh,
			yieldLow, yieldHigh,
			eqtypeIndexes, eqsrcIndexes, nenationIndexes, nesrcIndexes,
			isView, graphSelection
		)