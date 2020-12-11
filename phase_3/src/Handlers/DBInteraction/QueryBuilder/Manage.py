class Earthquake(object):

	@staticmethod
	def get(key):
		query = """
			SELECT
				e_earthquakekey,
				e_time,
				e_longitude,
				e_latitude,
				e_depth,
				e_mag,
				e_type,
				e_citykey
			FROM
				earthquake
			WHERE
				e_earthquakekey = {}
			;
		"""
		return query.format(str(key))

	@staticmethod
	def update(key, time, long, lat, depth, mag, eqtype):
		query = """
			UPDATE earthquake
			SET
				e_time = {},
				e_longitude = {},
				e_latitude = {},
				e_depth = {},
				e_mag = {},
				e_type = '{}'
			WHERE
				e_earthquakekey = {}
			;
		"""
		return query.format(str(time), str(long), str(lat), str(depth), str(mag), str(eqtype), str(key))

	@staticmethod
	def insert(time, long, lat, depth, mag, type):
		query = """
			INSERT INTO earthquake_input(e_time, e_longitude, e_latitude, e_depth, e_mag, e_type)
			VALUES({}, {}, {}, {}, {}, '{}')
			;
		"""
		return query.format(str(time), str(long), str(lat), str(depth), str(mag), str(type))

	@staticmethod
	def getLatestKey():
		query = """
			SELECT
				max(e_earthquakekey) + 1 as e_earthquakekey
			FROM
				earthquake
			;
		"""
		return query


class Nuclear(object):

	@staticmethod
	def getKey(earthquakeKey):
		query = """
			SELECT
				ne_nuclearkey
			FROM
				nuclear
			WHERE
				ne_earthquakekey = {}
			;
		"""
		return query.format(str(earthquakeKey))

	@staticmethod
	def get(key):
		query = """
			SELECT
				ne_nuclearkey,
				ne_nationkey,
				ne_yield,
				ne_earthquakekey
			FROM
				nuclear
			WHERE
				ne_nuclearkey = {}
			;
		"""
		return query.format(str(key))
	
	@staticmethod
	def update(key, nationKey, expYield):
		query = """
			UPDATE nuclear
			SET
				ne_nationkey = {},
				ne_yield = {}
			WHERE
				ne_nuclearkey = {}
			;
		"""
		return query.format(str(nationKey), str(expYield), str(key))

	@staticmethod
	def insert(nationKey, expYield, earthquakeKey):
		query = """
			INSERT INTO nuclear(ne_nationkey, ne_yield, ne_earthquakekey)
			VALUES({}, {}, {})
			;
		"""
		return query.format(str(nationKey), str(expYield), str(earthquakeKey))

	@staticmethod
	def delete(key):
		query = """
			DELETE FROM nuclear
			WHERE
				ne_nuclearkey = {}
			;
		"""
		return query.format(str(key))

	@staticmethod
	def getLatestKey():
		query = """
			SELECT
				max(ne_nuclearkey) as ne_nuclearkey
			FROM
				nuclear
			;
		"""
		return query


class EarthquakeSource(object):

	@staticmethod
	def get(key):
		query = """
			SELECT
				esm_earthquakekey,
				esm_eskey
			FROM
				earthquakesourcemapping
			WHERE
				esm_earthquakekey = {}
			;
		"""
		return query.format(str(key))


	@staticmethod
	def remove_all(key):
		query = """
			DELETE FROM
				earthquakesourcemapping
			WHERE
				esm_earthquakekey = {}
			;
		"""
		return query.format(str(key))

	@staticmethod
	def add(key, sourceKey):
		query = """
			INSERT INTO
				earthquakesourcemapping(esm_earthquakekey, esm_eskey)
			VALUES({}, '{}')
			;
		"""
		return query.format(str(key), str(sourceKey))

class NuclearSource(object):

	@staticmethod
	def get(key):
		query = """
			SELECT
				nesm_nuclearkey,
				nesm_neskey
			FROM
				nuclearsourcemapping
			WHERE
				nesm_nuclearkey = {}
			;
		"""
		return query.format(str(key))


	@staticmethod
	def remove_all(key):
		query = """
			DELETE FROM
				nuclearsourcemapping
			WHERE
				nesm_nuclearkey = {}
			;
		"""
		return query.format(str(key))

	@staticmethod
	def add(key, sourceKey):
		query = """
			INSERT INTO
				nuclearsourcemapping(nesm_nuclearkey, nesm_neskey)
			VALUES({}, '{}')
			;
		"""
		return query.format(str(key), str(sourceKey))

class Manage(object):

	Earthquake = Earthquake
	Nuclear = Nuclear
	EarthquakeSource = EarthquakeSource
	NuclearSource = NuclearSource