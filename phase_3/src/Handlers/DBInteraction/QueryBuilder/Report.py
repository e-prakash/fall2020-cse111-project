class Report(object):

	@staticmethod
	def getEarthquake(yearRange, eqTypes, magRange, sources, location):
		"""
		0: All, 1: Region, 2: Nation, 3: State, 4: City
		"""
		query = """
			SELECT
				e_earthquakekey,
				e_time,
				e_longitude,
				e_latitude,
				e_depth,
				e_mag,
				e_type,
				e_citykey,
				r_name,
				n_name,
				s_name,
				c_name,
				GROUP_CONCAT(esm_eskey,',') as esm_eskeys
			FROM
				earthquake,
				earthquakesourcemapping,
				city,
				state,
				nation,
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
			ORDER BY
				e_time ASC
			;
		"""
		return query.format(
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
	def getEarthquakeNuclear(yearRange, eqTypes, magRange, sources, location, nationKeys, yieldRange, neSources):
		"""
		0: All, 1: Region, 2: Nation, 3: State, 4: City
		"""
		query = """
			SELECT
				e_earthquakekey,
				e_time,
				e_longitude,
				e_latitude,
				e_depth,
				e_mag,
				e_type,
				e_citykey,
				r_name,
				eqnation.n_name as n_name,
				s_name,
				c_name,
				GROUP_CONCAT(esm_eskey,',') as esm_eskeys,
				ne_nuclearkey,
				ne_nationkey,
				nenation.n_name as ne_nationname,
				ne_yield,
				GROUP_CONCAT(nesm_neskey,',') as nesm_neskeys
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
			ORDER BY
				e_time ASC
			;
		"""
		return query.format(
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
	print(Report.getEarthquake(None, None, None, None, [0]))
	print(Report.getEarthquake(None, None, None, None, [4, 935227]))
	print(Report.getEarthquake(None, None, None, None, [3, 5332921]))
	print(Report.getEarthquake(None, None, None, None, [2, 6252001]))
	print(Report.getEarthquake(None, None, None, None, [1, 6255149]))
	print(Report.getEarthquake([2000, 2030], ['nuclear explosion', 'earthquake'], [6.5, 10.0], ['AK'], [1, 6255149]))

def test_2():
	print("test 2...")
	print(Report.getEarthquakeNuclear([1900, 2030], ['nuclear explosion', 'earthquake'], [5.5, 10.0], None, [1, 6255147], [1814991, 0], [0, 50000], ['H', 'N']));
	print(Report.getEarthquakeNuclear([1900, 2030], ['nuclear explosion', 'earthquake'], [5.5, 10.0], None, [1, 6255147], None, None, None));

if __name__ == "__main__":
	#test_1()
	test_2()