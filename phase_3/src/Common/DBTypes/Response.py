class Response(object):

        def __init__(self, action, fields):
                # action is enum from EnumReq.Action
                # fields is a dictionary with keys from EnumDB
                self.action = action
                self.fields = fields

        def getActionType(self):
                return type(self.action)