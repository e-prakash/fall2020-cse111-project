class CityEnum(object):
        Key = 'c_citykey'
        StateKey = 'c_statekey'
        Name = 'c_name'
        Latitude = 'c_latitude'
        Longitude = 'c_longitude'
        Population = 'c_population'

class StateEnum(object):
        Key = 's_statekey'
        NationKey = 's_nationkey'
        Name = 's_name'
        Population = 's_population'

class NationEnum(object):
        Key = 'n_nationkey'
        RegionKey = 'n_regionkey'
        Name = 'n_name'
        Population = 'n_population'
        Area = 'n_area'

class RegionEnum(object):
        Key = 'r_regionkey'
        Name = 'r_name'
        Population = 'r_population'
        Area = 'r_area'


class EarthquakeEnum(object):
        Key = 'e_earthquakekey'
        Time = 'e_time'
        Longitude = 'e_longitude'
        Latitude = 'e_latitude'
        Depth = 'e_depth'
        Mag = 'e_mag'
        Type = 'e_type'
        CityKey = 'e_citykey'

class EarthquakeSourceEnum(object):
        Key = 'es_eskey'
        Name = 'es_name'

class EarthquakeSourceMappingEnum(object):
        EarthquakeKey = 'esm_earthquakekey'
        SourceKey = 'esm_eskey'


class NuclearEnum(object):
        Key = 'ne_nuclearkey'
        NationKey = 'ne_nationkey'
        Yield = 'ne_yield'
        EarthquakeKey = 'ne_earthquakekey'

class NuclearSourceEnum(object):
        Key = 'nes_neskey'
        Name = 'nes_name'
        IsPublic = 'nes_ispublic'
        RunBy = 'nes_runby'

class NuclearSourceMappingEnum(object):
        NuclearKey = 'nesm_nuclearkey'
        SourceKey = 'nesm_neskey'


class ReportEnum(object):
        EarthquakeSourceMappingSourceKeys = 'esm_eskeys'
        NuclearSourceMappingSourceKeys = 'nesm_neskeys'

class GraphEnum(object):
        XValue = 'xvalue'
        YValue = 'yvalue'
        Year = 'year'
        Aggregate = 'AGG'

class OptionsEnum(object):
        pass

class EnumRes(object):
        City = CityEnum
        State = StateEnum
        Nation = NationEnum
        Region = RegionEnum

        Earthquake = EarthquakeEnum
        EarthquakeSource = EarthquakeSourceEnum
        EarthquakeSourceMapping = EarthquakeSourceMappingEnum

        Nuclear = NuclearEnum
        NuclearSource = NuclearSourceEnum
        NuclearSourceMapping = NuclearSourceMappingEnum

        Report = ReportEnum
        Graph = GraphEnum
        Options = OptionsEnum

if __name__ == "__main__":
        print(CityEnum.Key)
        print(CityEnum.Key == CityEnum.Key)
        print(CityEnum.Key == CityEnum.Name)
        # print(CityEnum('c_citykey'))
        # print(CityEnum('c_citykey'))
        print(DBEnum.City)
        print(DBEnum.City == DBEnum.City)
        print(DBEnum.City == DBEnum.State)
        print(DBEnum.City.Key)
        print(DBEnum.City.Key)