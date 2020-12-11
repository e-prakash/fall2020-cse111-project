from enum import Enum, auto

class Options(Enum):
        Eq_Types = auto()
        Eq_Srcs = auto()

        Ne_Srcs = auto()

        Location_AllNations = auto()
        Location_Regions = auto()
        Location_Nations = auto()
        Location_States = auto()
        Location_Cities = auto()

class Manage(Enum):
        Eq_Get = auto()
        Eq_Update = auto()
        Eq_Insert = auto()

        Eq_GetLatestKey = auto()
        Ne_GetKey = auto()
        Ne_Get = auto()
        Ne_Update = auto()
        Ne_Insert = auto()
        Ne_Delete = auto()
        Ne_GetLatestKey = auto()

        EqSrc_Get = auto()
        EqSrc_RemoveAll = auto()
        EqSrc_Add = auto()

        NeSrc_Get = auto()
        NeSrc_RemoveAll = auto()
        NeSrc_Add = auto()

class Report(Enum):
        Eq = auto()
        EqNe = auto()

class Graph(Enum):
        Eq = auto()
        EqNe = auto()


class FilterFields(Enum):
        YearRange = auto()
        EqTypes = auto()
        MagnitudeRange = auto()
        EqSrcs = auto()
        Location = auto()
        NeNationKeys = auto()
        YieldRange = auto()
        NeSrcs = auto()

class GraphFields(Enum):
        Value = auto()
        Type = auto()

class ManageFields(Enum):
        EqKey = auto()
        EqTime = auto()
        EqLongitude = auto()
        EqLatitude = auto()
        EqDepth = auto()
        EqMag = auto()
        EqType = auto()

        NeKey = auto()
        NeNationKey = auto()
        NeYield = auto()

        EqSrcKey = auto()

        NeSrcKey = auto()

class OptionsFields(Enum):
        RegionKey = auto()
        NationKey = auto()
        StateKey = auto()

class Action(object):
        Options = Options
        Manage = Manage
        Report = Report
        Graph = Graph

class Fields(object):
        Filter = FilterFields
        Graph = GraphFields
        Manage = ManageFields
        Options = OptionsFields

class EnumReq(object):
        Action = Action
        Fields = Fields