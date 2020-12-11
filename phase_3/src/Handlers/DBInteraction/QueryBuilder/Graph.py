def selectHelper(graphType, location, graphValue):

	locationOption = location[0]
	xvalue = None
	if locationOption == 0:
		xvalue = "r_name"
	elif locationOption == 1:
		xvalue = "n_name"
	elif locationOption == 2:
		xvalue = "s_name"
	elif locationOption == 3:
		xvalue = "c_name"
	elif locationOption == 4:
		xvalue = "c_name"
	else:
		xvalue == "selectHelper-Error"
	
	yvalueTop = None
	yvalueBottom = None
	if graphValue == 0:
		yvalueTop = "CAST(count(*) AS REAL)"
		yvalueBottom = "1"
	elif graphValue == 1:
		yvalueTop = "CAST(count(*) AS REAL)"
		if locationOption == 0:
			yvalueBottom = "CAST(r_population AS REAL)"
		elif locationOption == 1:
			yvalueBottom = "CAST(n_population AS REAL)"
		elif locationOption == 2:
			yvalueBottom = "CAST(s_population AS REAL)"
		elif locationOption == 3:
			yvalueBottom = "CAST(c_population AS REAL)"
		elif locationOption == 4:
			yvalueBottom = "CAST(c_population AS REAL)"
		else:
			yvalueBottom = "selectHelper-Error"
	elif graphValue == 2:
		yvalueTop = "CAST(count(*) AS REAL)"
		if locationOption == 0:
			yvalueBottom = "CAST(r_area AS REAL)"
		elif locationOption == 1:
			yvalueBottom = "CAST(n_area AS REAL)"
		elif locationOption == 2:
			yvalueBottom = "selectHelper-Error"
		elif locationOption == 3:
			yvalueBottom = "selectHelper-Error"
		elif locationOption == 4:
			yvalueBottom = "selectHelper-Error"
		else:
			yvalueBottom = "selectHelper-Error"
	elif graphValue == 3:
		yvalueTop = "max(e_mag)"
		yvalueBottom = "1"
	elif graphValue == 4:
		yvalueTop = "min(e_mag)"
		yvalueBottom = "1"
	else:
		yvalueTop = "selectHelper-Error"
		yvalueBottom = "selectHelper-Error"
	
	year = None
	if graphType == 0:
		year = "'AGG'"
	elif graphType == 1:
		year = "CAST(strftime('%Y', e_time) AS INTEGER)"
	else:
		year = "selectHelper-Error"

	return [xvalue, (yvalueTop, yvalueBottom), year]


class Graph(object):

	# use group by even for siutations with no grouping
	# sctrach this - won't do all option, just go with normal spread stuff
	# trend lines will be color coded with key and bar graph will have names
	# on a-axis

	# always spread on next one, so can't graph one thing

	@staticmethod
	def getEarthquake(yearRange, eqTypes, magRange, sources, location, graphValue, graphType):
		"""
		[0: All gby Region, 1: Region gby Nation, 2: Nation gby State, 3: State gby City, 4: City; location name]
		[0: total, 1: total per population, 2: total per area, 3: max mag, 4: min mag]
		[0: aggregate, 1: trend]
		"""
		query = """
			SELECT
				{} as xvalue,
				{}/{} as yvalue,
				{} as year
			FROM
				(
					SELECT
						e_earthquakekey,
						e_time,
						e_mag,
						r_name,
						n_name,
						s_name,
						c_name,
						c_population,
						s_population,
						n_area,
						n_population,
						r_area,
						r_population
					FROM
						earthquake,
						earthquakesourcemapping,
						city,
						state,
						nation as eqnation,
						region
					WHERE
						e_earthquakekey = esm_earthquakekey AND
						e_citykey = c_citykey AND
						c_statekey = s_statekey AND
						s_nationkey = n_nationkey AND
						n_regionkey = r_regionkey AND

						{} <= CAST(strftime('%Y', e_time) AS INTEGER) AND
						{} >= CAST(strftime('%Y', e_time) AS INTEGER) AND
						{} <= e_mag AND
						{} >= e_mag AND
						e_type {} in ({}) AND
						esm_eskey {} in ({}) AND

						c_citykey = {} AND
						s_statekey = {} AND
						n_nationkey = {} AND
						r_regionkey = {}
					GROUP BY
						e_earthquakekey
				)
			GROUP BY
				xvalue,
				year
			ORDER BY
				yvalue DESC
			;
		"""
		selectOptions = selectHelper(graphType, location, graphValue)
		return query.format(
			selectOptions[0],
			selectOptions[1][0],
			selectOptions[1][1],
			selectOptions[2],
			-2147483648 if yearRange is None else yearRange[0],
			2147483647 if yearRange is None else yearRange[1],
			0 if magRange is None else magRange[0],
			2147483647 if magRange is None else magRange[1],
			"not" if eqTypes is None else "",
			"" if eqTypes is None else ("'" + "', '".join(eqTypes) + "'"),
			"not" if sources is None else "",
			"" if sources is None else ("'" + "', '".join(sources) + "'"),
			location[1] if location[0] == 4 else "c_citykey",
			location[1] if location[0] == 3 else "s_statekey",
			location[1] if location[0] == 2 else "n_nationkey",
			location[1] if location[0] == 1 else "r_regionkey"
		)

	@staticmethod
	def getEarthquakeNuclear(yearRange, eqTypes, magRange, sources, location, nationKeys, yieldRange, neSources, graphValue, graphType):
		query = """
			SELECT
				{} as xvalue,
				{}/{} as yvalue,
				{} as year
			FROM
				(
					SELECT
						e_earthquakekey,
						e_time,
						e_mag,
						r_name,
						eqnation.n_name as n_name,
						s_name,
						c_name,
						c_population,
						s_population,
						eqnation.n_area as n_area,
						eqnation.n_population as n_population,
						r_area,
						r_population
					FROM
						earthquake,
						earthquakesourcemapping,
						nuclear,
						nuclearsourcemapping,
						city,
						state,
						nation as eqnation,
						nation as nenation,
						region
					WHERE
						e_earthquakekey = esm_earthquakekey AND
						e_citykey = c_citykey AND
						c_statekey = s_statekey AND
						s_nationkey = eqnation.n_nationkey AND
						eqnation.n_regionkey = r_regionkey AND

						{} <= CAST(strftime('%Y', e_time) AS INTEGER) AND
						{} >= CAST(strftime('%Y', e_time) AS INTEGER) AND
						{} <= e_mag AND
						{} >= e_mag AND
						e_type {} in ({}) AND
						esm_eskey {} in ({}) AND

						c_citykey = {} AND
						s_statekey = {} AND
						eqnation.n_nationkey = {} AND
						r_regionkey = {} AND

						e_earthquakekey = ne_earthquakekey AND
						ne_nuclearkey = nesm_nuclearkey AND
						ne_nationkey = nenation.n_nationkey AND

						{} <= ne_yield AND
						{} >= ne_yield AND
						ne_nationkey {} in ({}) AND
						nesm_neskey {} in ({})
					GROUP BY
						e_earthquakekey
				)
			GROUP BY
				xvalue,
				year
			ORDER BY
				yvalue DESC
			;
		"""
		selectOptions = selectHelper(graphType, location, graphValue)
		return query.format(
			selectOptions[0],
			selectOptions[1][0],
			selectOptions[1][1],
			selectOptions[2],
			-2147483648 if yearRange is None else yearRange[0],
			2147483647 if yearRange is None else yearRange[1],
			0 if magRange is None else magRange[0],
			2147483647 if magRange is None else magRange[1],
			"not" if eqTypes is None else "",
			"" if eqTypes is None else ("'" + "', '".join(eqTypes) + "'"),
			"not" if sources is None else "",
			"" if sources is None else ("'" + "', '".join(sources) + "'"),
			location[1] if location[0] == 4 else "c_citykey",
			location[1] if location[0] == 3 else "s_statekey",
			location[1] if location[0] == 2 else "eqnation.n_nationkey",
			location[1] if location[0] == 1 else "r_regionkey",
			0 if yieldRange is None else yieldRange[0],
			2147483647 if yieldRange is None else yieldRange[1],
			"not" if nationKeys is None else "",
			"" if nationKeys is None else (", ".join(list(map(lambda x: str(x), nationKeys)))),
			"not" if neSources is None else "",
			"" if neSources is None else ("'" + "', '".join(neSources) + "'")
		)


def test_1():
	print("test 1...")
	print(Graph.getEarthquake(
		[1900, 2000], ['earthquake', 'nuclear explosion'], [5, 10], ['US'], [1, 6255149], 0, 0
	))
	print(Graph.getEarthquake(
		[1900, 2000], ['earthquake', 'nuclear explosion'], [5, 10], ['US'], [1, 6255149], 0, 1
	))
	print(Graph.getEarthquake(
		[1900, 2000], ['earthquake', 'nuclear explosion'], [5, 10], None, [1, 6255149], 0, 1
	))
	print(Graph.getEarthquake(
		None, None, None, None, [0], 0, 1
	))
	print(Graph.getEarthquake(
		None, None, None, None, [0], 4, 1
	))

def test_2():
	print("test 2...")
	print(Graph.getEarthquakeNuclear([1900, 2030], ['nuclear explosion', 'earthquake'], [0, 10.0], None, [1, 6255147], [1814991, 1168579], [0, 50000], ['H', 'N'], 0, 0));

if __name__ == "__main__":
	#test_1()
	test_2()