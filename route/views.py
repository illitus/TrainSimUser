from django.shortcuts import render
import csv
from datetime import datetime, timedelta, date
a=""
b=""

# Create your views here.
def stationlist():
    stat="statics/csv/distance_up.csv"
    statfields=[]
    statlist=[]
    with open(stat, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        statfields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            statlist.append(row[0])
    return statlist

def select(request):
    statlist=stationlist()
    return render(request,"route/select.html",{'statlist':statlist})

def route_info(request,routecode):


    route = routecode

    # csv file name
    filename = "statics/csv/churchgate_up.csv"

    # initializing the titles and rows list
    fields_up = []
    rows_up = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields_up = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows_up.append(row)

    route_info = []
    details = []
    flag = True

    for i in range(0, len(rows_up)):
        if route == rows_up[i][0]:
            route_info=fields_up[3:]
            for k in range(3, len(rows_up[i])):
                if rows_up[i][k]:
                    details.append(rows_up[i][k])
                else:
                    details.append('--:--')
            flag = False
            break

    if flag:
        # csv file name
        filename = "statics/csv/virar_down.csv"

        # initializing the titles and rows list
        fields_down = []
        rows_down = []

        # reading csv file
        with open(filename, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting field names through first row
            fields_down = next(csvreader)

            # extracting each data row one by one
            for row in csvreader:
                rows_down.append(row)

            for i in range(0, len(rows_down)):
                if route == rows_down[i][0]:
                    route_info=fields_down[3:]
                    for k in range(3, len(rows_down[i])):
                        if rows_down[i][k]:
                            details.append(rows_down[i][k])
                        else:
                            details.append('--:--')
                    flag = False
                    break
    info=zip(route_info,details)
    return render(request,'route/route_info.html',{'routecode':routecode,'info':info})

def schedule(request):
    # csv file name
    filename = "statics/csv/churchgate_up.csv"

    # initializing the titles and rows list
    fields_up = []
    rows_up = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields_up = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows_up.append(row)

    # csv file name
    filename = "statics/csv/virar_down.csv"

    # initializing the titles and rows list
    fields_down = []
    rows_down = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields_down = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows_down.append(row)

    # fetching current time
    x = datetime.now()
    x = x.strftime("%H") + ":" + x.strftime("%M")

    # converting x into a time variable again
    x = x.split(":")
    x = timedelta(hours=int(x[0]), minutes=int(x[1]))
    if request.POST['source']:
        a = request.POST['source']
        b = request.POST['dest']

    if fields_up.index(b) > fields_up.index(a):
        a_i = fields_up.index(a)
        b_i = fields_up.index(b)
        rows = rows_up
        fields = fields_up

    else:
        a_i = fields_down.index(a)
        b_i = fields_down.index(b)
        rows = rows_down
        fields = fields_down

    trains = []
    for i in range(0, len(rows_up)):
        details = []
        if rows[i][a_i]:
            if rows[i][b_i]:
                details.append(rows[i][0])
                details.append(a)
                details.append(rows[i][a_i])
                details.append(b)
                details.append(rows[i][b_i])
                t = rows[i][a_i]
                t = t.split(":")
                t = timedelta(hours=int(t[0]), minutes=int(t[1]))
                if x <= t:
                    details.append(True)
                else:
                    details.append(False)

                trains.append(details)
    statlist=stationlist()
    return render(request,'route/select.html',{'trains':trains,'statlist':statlist})