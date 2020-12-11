import numpy as np
import math
import pandas as pd
import sqlite3

from .QueryBuilder import *
from ...Common import DBTypes

def getargs(args, fieldList):
	return list(map(lambda x: args[x], fieldList))

def generateQuery(request):
	assert isinstance(request, DBTypes.Request)
	
	query = None
	action = request.action
	actionType = request.getActionType()
	args = request.fields

	if(actionType == DBTypes.EnumReq.Action.Options):
		actions = DBTypes.EnumReq.Action.Options
		fields = DBTypes.EnumReq.Fields.Options
		qb = QueryBuilder.Options

		if(action == actions.Eq_Types):
			query = qb.Earthquake.types(*getargs(args,[
			]))
		elif(action == actions.Eq_Srcs):
			query = qb.Earthquake.sources(*getargs(args,[
			]))
		elif(action == actions.Ne_Srcs):
			query = qb.Nuclear.sources(*getargs(args,[
			]))
		elif(action == actions.Location_AllNations):
			query = qb.Location.allNation(*getargs(args,[
			]))
		elif(action == actions.Location_Regions):
			query = qb.Location.region(*getargs(args,[
			]))
		elif(action == actions.Location_Nations):
			query = qb.Location.nation(*getargs(args,[
				fields.RegionKey
			]))
		elif(action == actions.Location_States):
			query = qb.Location.state(*getargs(args,[
				fields.NationKey
			]))
		elif(action == actions.Location_Cities):
			query = qb.Location.city(*getargs(args,[
				fields.StateKey
			]))
		else:
			query = "DBInteraction-Error"

	elif(actionType == DBTypes.EnumReq.Action.Manage):
		actions = DBTypes.EnumReq.Action.Manage
		fields = DBTypes.EnumReq.Fields.Manage
		qb = QueryBuilder.Manage

		if(action == actions.Eq_Get):
			query = qb.Earthquake.get(*getargs(args,[
				fields.EqKey
			]))
		elif(action == actions.Eq_Update):
			query = qb.Earthquake.update(*getargs(args,[
				fields.EqKey,
				fields.EqTime,
				fields.EqLongitude,
				fields.EqLatitude,
				fields.EqDepth,
				fields.EqMag,
				fields.EqType
			]))
		elif(action == actions.Eq_Insert):
			query = qb.Earthquake.insert(*getargs(args,[
				fields.EqTime,
				fields.EqLongitude,
				fields.EqLatitude,
				fields.EqDepth,
				fields.EqMag,
				fields.EqType
			]))
		elif(action == actions.Eq_GetLatestKey):
			query = qb.Earthquake.getLatestKey(*getargs(args,[
			]))
		elif(action == actions.Ne_GetKey):
			query = qb.Nuclear.getKey(*getargs(args,[
				fields.EqKey
			]))
		elif(action == actions.Ne_Get):
			query = qb.Nuclear.get(*getargs(args,[
				fields.NeKey
			]))
		elif(action == actions.Ne_Update):
			query = qb.Nuclear.update(*getargs(args,[
				fields.NeKey,
				fields.NeNationKey,
				fields.NeYield
			]))
		elif(action == actions.Ne_Insert):
			query = qb.Nuclear.insert(*getargs(args,[
				fields.NeNationKey,
				fields.NeYield,
				fields.EqKey
			]))
		elif(action == actions.Ne_Delete):
			query = qb.Nuclear.delete(*getargs(args,[
				fields.NeKey
			]))
		elif(action == actions.Ne_GetLatestKey):
			query = qb.Nuclear.getLatestKey(*getargs(args,[
			]))
		elif(action == actions.EqSrc_Get):
			query = qb.EarthquakeSource.get(*getargs(args,[
				fields.EqKey
			]))
		elif(action == actions.EqSrc_RemoveAll):
			query = qb.EarthquakeSource.remove_all(*getargs(args,[
				fields.EqKey
			]))
		elif(action == actions.EqSrc_Add):
			query = qb.EarthquakeSource.add(*getargs(args,[
				fields.EqKey,
				fields.EqSrcKey
			]))
		elif(action == actions.NeSrc_Get):
			query = qb.NuclearSource.get(*getargs(args,[
				fields.NeKey
			]))
		elif(action == actions.NeSrc_RemoveAll):
			query = qb.NuclearSource.remove_all(*getargs(args,[
				fields.NeKey
			]))
		elif(action == actions.NeSrc_Add):
			query = qb.NuclearSource.add(*getargs(args,[
				fields.NeKey,
				fields.NeSrcKey
			]))
		else:
			query = "DBInteraction-Error"

	elif(actionType == DBTypes.EnumReq.Action.Report):
		actions = DBTypes.EnumReq.Action.Report
		fields = DBTypes.EnumReq.Fields.Filter
		qb = QueryBuilder.Report

		if(action == actions.Eq):
			query = qb.getEarthquake(*getargs(args,[
				fields.YearRange,
				fields.EqTypes,
				fields.MagnitudeRange,
				fields.EqSrcs,
				fields.Location
			]))
		elif(action == actions.EqNe):
			query = qb.getEarthquakeNuclear(*getargs(args,[
				fields.YearRange,
				fields.EqTypes,
				fields.MagnitudeRange,
				fields.EqSrcs,
				fields.Location,
				fields.NeNationKeys,
				fields.YieldRange,
				fields.NeSrcs
			]))
		else:
			query = "DBInteraction-Error"

	elif(actionType == DBTypes.EnumReq.Action.Graph):
		actions = DBTypes.EnumReq.Action.Graph
		flt_fields = DBTypes.EnumReq.Fields.Filter
		fields = DBTypes.EnumReq.Fields.Graph
		qb = QueryBuilder.Graph

		if(action == actions.Eq):
			query = qb.getEarthquake(*getargs(args,[
				flt_fields.YearRange,
				flt_fields.EqTypes,
				flt_fields.MagnitudeRange,
				flt_fields.EqSrcs,
				flt_fields.Location,
				fields.Value,
				fields.Type
			]))
		elif(action == actions.EqNe):
			query = qb.getEarthquakeNuclear(*getargs(args,[
				flt_fields.YearRange,
				flt_fields.EqTypes,
				flt_fields.MagnitudeRange,
				flt_fields.EqSrcs,
				flt_fields.Location,
				flt_fields.NeNationKeys,
				flt_fields.YieldRange,
				flt_fields.NeSrcs,
				fields.Value,
				fields.Type
			]))
		else:
			query = "DBInteraction-Error"

	else:
		query = "DBInteraction-Error"

	return query

class DBInteraction(object):

	def __init__(self, dbfilename):
		self.cnx = sqlite3.connect(dbfilename)

	def __del__(self):
		self.cnx.close()

	def complete(self, request):
		query = generateQuery(request)
		data = False
		if(("UPDATE" in query) or ("DELETE" in query) or ("INSERT" in query)):
			try:
				self.cnx.execute("PRAGMA foreign_keys = on;")
				self.cnx.execute(query)
				self.cnx.commit()
				data = True
			except Exception as e:
				print(e)
				self.cnx.rollback()
				data = False
		else:
			df = pd.read_sql_query(query, self.cnx)
			data = df.to_dict('list')
		return data

def test_1():
	print("test 1...")
	Action = DBTypes.EnumReq.Action
	Fields = DBTypes.EnumReq.Fields
	request = DBTypes.Request(
		Action.Graph.EqNe,
		{
			Fields.Filter.YearRange: [1900, 1901],
			Fields.Filter.EqTypes: ['earthquake', 'nuclear explosion'],
			Fields.Filter.MagnitudeRange: [0, 10],
			Fields.Filter.EqSrcs: ['AK', 'US', 'ISCGEM'],
			Fields.Filter.Location: [1, 6255147],
			Fields.Filter.NeNationKeys: None,
			Fields.Filter.YieldRange: [0, 100000],
			Fields.Filter.NeSrcs: None,
			Fields.Graph.Value: 1,
			Fields.Graph.Type: 1
		}
	)
	dbi = DBInteraction(r'data/data.sqlite')
	print(generateQuery(request))
	print(dbi.complete(
		request
	))

def test_2():
	print("test 2...")
	Action = DBTypes.EnumReq.Action
	Fields = DBTypes.EnumReq.Fields
	request = DBTypes.Request(
		Action.Manage.Ne_Update,
		{
			Fields.Manage.NeKey: 2050,
			Fields.Manage.NeNationKey: 226074,
			Fields.Manage.NeYield: 2559
		}
	)
	dbi = DBInteraction(r'data/data.sqlite')
	print(generateQuery(request))
	print(dbi.complete(
		request
	))

if __name__ == "__main__":
	test_1()
	#test_2()