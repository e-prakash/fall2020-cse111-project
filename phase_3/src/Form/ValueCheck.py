import datetime

from . import TimeFunc

def RepresentsInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False
def RepresentsFloat(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def isValidYear(year):
	return RepresentsInt(year)
def isValidMonth(month):
	return (
		RepresentsInt(month) and
		int(month) >= 1 and int(month) <= 12
	)
def isValidDay(month, day):
	days = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	return (
		isValidMonth(month) and
		RepresentsInt(day) and
		int(day) >= 1 and int(day) <= 31 and
		int(day) <= days[int(month)]
	)
def isValidHour(hour):
	return (
		RepresentsInt(hour) and
		int(hour) >= 0 and int(hour) <= 23
	)
def isValidMinute(minute):
	return (
		RepresentsInt(minute) and
		int(minute) >= 0 and int(minute) <= 59
	)
def isValidSecond(sec):
	return (
		RepresentsInt(sec) and
		int(sec) >= 0 and int(sec) <= 59
	)

def julianToDatetime(julianday):
        date = TimeFunc.jd_to_datetime(julianday)
        return (date.year,date.month,date.day,date.hour,date.minute,date.second)

def datetimeToJulian(year,month,day,hour,minute,second):
        if(
                isValidYear(year) and
                isValidMonth(month) and
                isValidDay(month, day) and
                isValidHour(hour) and
                isValidMinute(minute) and
                isValidSecond(second)
        ):
                dt = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second),0)
                result = TimeFunc.datetime_to_jd(dt)
        else:
                result = None
        return result

def isValidLatitude(lat):
        return(
                RepresentsFloat(lat) and
                float(lat) >= -90 and
                float(lat) <= 90
        )

def isValidLongitude(long):
        return(
                RepresentsFloat(long) and
                float(long) >= -180 and
                float(long) <= 180
        )

def isValidDepth(depth):
        return RepresentsFloat(depth)

def isValidMag(mag):
        return(
                RepresentsFloat(mag) and
                float(mag) >= 0.1 and 
                float(mag) <= 15.0
        )

def isValidYield(yieldVal):
        return(
                RepresentsFloat(yieldVal) and
                float(yieldVal) >= 0.01 and
                float(yieldVal) <= 100000.00
        )

def test_1():
        print("test 1...")
        print(julianToDatetime(2418442.677))
        print(datetimeToJulian(1909, 5, 16, 4, 14, 52))

if __name__ == "__main__":
        test_1()
