#sqldetails = ["host","user","password","db"]
file = open("sqlserverdetails.txt","r")
sqldetails = dict(zip(["host","user","password","db"],file.read().splitlines()))
