from .Form.ViewGraphApp import ViewGraphApp
from .Form.ManageApp import ManageApp
from .Handlers.DBInteraction import DBInteraction
import sys

if __name__ == "__main__":
        if len(sys.argv) == 1:
                print("options: 'view' or 'edit earthquake_key' or 'edit' for new earthquake")
        else:
                arg1 = str(sys.argv[1])
                dbi = DBInteraction(r'src/data/data.sqlite')
                if(arg1 == 'view'):
	                va = ViewGraphApp(dbi)
	                va.run()
                elif(arg1 == 'edit'):
                        if len(sys.argv) > 2:
                                ma = ManageApp(dbi, int(sys.argv[2]))
                                ma.run()
                        else:
	                        ma = ManageApp(dbi)
	                        ma.run()
                else:
                        print("options: 'view' or 'edit earthquake_key' or 'edit' for new earthquake")