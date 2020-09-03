import csv
from collections import defaultdict

reader = csv.reader(open("2268427.csv", "r"))

TARGET = 68
MIN_T = "07:00:00"
MAX_T = "18:00:00"

deg_hr_total = 0
n_deg_hr = 0

all_temps = defaultdict(int)
working_hr_temps = defaultdict(int)
working_hr_heating_degrees = defaultdict(int)
working_hrs = defaultdict(int)

seen = set()

for i, row in enumerate(reader):
    ts = row[1]
    temp = row[43]

    if i == 0:
        assert temp == "HourlyDryBulbTemperature"
        continue

    if temp.endswith("s"):
        # suspect value, still use
        temp = temp[:-2]

    if not temp:
        continue
    
    temp = int(temp)
    date, time = ts.split("T")

    h, m, s = time.split(":")
    key = "%s-%s" % (date, h)
    if key in seen:
        continue
    seen.add(key)

    n_deg_hr += 1
    all_temps[temp] += 1
    
    if time < MIN_T or time >= MAX_T:
        continue

    working_hrs[h] += 1
    working_hr_temps[temp] += 1

    delta = TARGET - temp
    working_hr_heating_degrees[max(delta, 0)] += 1

    if delta < 0:
        continue
   
    deg_hr_total += delta

print("hr distribution")
for h, count in sorted(working_hrs.items()):
    print ("  %s\t%s" % (h, count))

print("")
print("all temps")
for temp, count in sorted(all_temps.items()):
    print ("  %s\t%s" % (temp, count))

print("")
print("working hour temps")
for temp, count in sorted(working_hr_temps.items()):
    print ("  %s\t%s" % (temp, count))

print("")
print("working hour heating degrees")
for delta, count in sorted(working_hr_heating_degrees.items()):
    print ("  %s\t%s" % (delta, count))

print("samples\t%s" % (n_deg_hr))
print("average heating degrees\t%.2f" % (deg_hr_total / n_deg_hr))



