
class Earthquake(object):

	@staticmethod
	def types():
		query = """
			SELECT DISTINCT
				e_type
			FROM
				earthquake
			ORDER BY
				e_type ASC
			;
		"""
		return query

	@staticmethod
	def sources():
		query = """
			SELECT
				es_eskey,
				es_name
			FROM
				earthquakesource
			ORDER BY
				es_name ASC
			;		
		"""
		return query

class Nuclear(object):

	@staticmethod
	def sources():
		query = """
			SELECT
				nes_neskey,
				nes_name
			FROM
				nuclearsource
			ORDER BY
				nes_name ASC
			;		
		"""
		return query

class Location(object):

	@staticmethod
	def allNation():
		query = """
			SELECT
				n_nationkey,
				n_name
			FROM
				nation
			ORDER BY
				n_name ASC
			;
		"""
		return query

	@staticmethod
	def region():
		query = """
			SELECT
				r_regionkey,
				r_name
			FROM
				region
			ORDER BY
				r_name ASC
			;
		"""
		return query
	
	@staticmethod
	def nation(regionkey):
		query = """
			SELECT
				n_nationkey,
				n_name
			FROM
				nation
			WHERE
				n_regionkey = {}
			ORDER BY
				n_name ASC
			;
		"""
		return query.format(str(regionkey))

	@staticmethod
	def state(nationkey):
		query = """
			SELECT
				s_statekey,
				s_name
			FROM
				state
			WHERE
				s_nationkey = {}
			ORDER BY
				s_name ASC
			;
		"""
		return query.format(str(nationkey))

	@staticmethod
	def city(statekey):
		query = """
			SELECT
				c_citykey,
				c_name
			FROM
				city
			WHERE
				c_statekey = {}
			ORDER BY
				c_name ASC
			;
		"""
		return query.format(str(statekey))

class Options(object):

	Earthquake = Earthquake
	Nuclear = Nuclear
	Location = Location

if __name__ == "__main__":
	print(Options.Earthquake.types())
	print(Options.Nuclear.sources())
	print(Options.Location.city(1138957))