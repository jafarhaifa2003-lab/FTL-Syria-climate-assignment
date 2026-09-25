# FTL Syria - Python Assignment
# ---------- Exercise 1 ----------
# list of cities, each one is a dict
# note: Hama has no temperature on purpose

cities = [
    {"city": "Damascus", "temperature": 38, "humidity": 30, "rainfall": 2},
    {"city": "Aleppo",   "temperature": 35, "humidity": 40, "rainfall": 8},
    {"city": "Homs",     "temperature": 41, "humidity": 20, "rainfall": 0},
    {"city": "Latakia",  "temperature": 29, "humidity": 70, "rainfall": 20},
    {"city": "Hama",     "temperature": None, "humidity": 50, "rainfall": 10},
]

print("Exercise 1 - all cities")
print("-----------------------")

# just printing everything first
for c in cities:
    print("City:", c["city"])
    print("  Temp:", c["temperature"])
    print("  Humidity:", c["humidity"], "%")
    print("  Rainfall:", c["rainfall"], "mm")
    print()

# now the actual classification part
print("Classification:")
print("----------------")

valid_temps = []
results = {}

for c in cities:
    t = c["temperature"]

    # skip the city if temp is missing
    if t is None:
        print(c["city"] + ": no temperature, skipping")
        continue

    valid_temps.append(t)

    # figure out the category
    if t >= 40:
        label = "Extreme Heat"
    elif t >= 35:
        label = "High Heat"
    elif t >= 30:
        label = "Moderate Heat"
    else:
        label = "Normal"

    results[c["city"]] = label
    print(c["city"] + " -> " + str(t) + "C -> " + label)

# some quick stats
count = len(valid_temps)
avg = round(sum(valid_temps) / count, 2)
high = max(valid_temps)
low = min(valid_temps)

print()
print("Valid readings:", count)
print("Average temp:", avg)
print("Hottest:", high)
print("Coldest:", low)

print()
print("Results dict:", results)


# ---------- Exercise 2 ----------
print()
print("Exercise 2 - risk levels")
print("------------------------")

# this one returns the risk based on temp + rain
def calculate_risk(temperature, rainfall):
    if temperature >= 40:
        return "EXTREME"
    elif temperature >= 35 or rainfall < 5:
        return "HIGH"
    elif temperature >= 30 or rainfall < 15:
        return "MODERATE"
    else:
        return "LOW"


# helper function that gives us avg, min and max together
def get_stats(temps):
    a = round(sum(temps) / len(temps), 2)
    return (a, min(temps), max(temps))


# check the risk for each city
for c in cities:
    t = c["temperature"]
    if t is None:
        continue
    r = calculate_risk(t, c["rainfall"])
    print(c["city"], "|", t, "C |", c["rainfall"], "mm |", r)

# stats
print()
print("Stats (avg, min, max):", get_stats(valid_temps))

# only show the dangerous ones
print()
print("Only HIGH or EXTREME:")
for c in cities:
    t = c["temperature"]
    if t is None:
        continue
    r = calculate_risk(t, c["rainfall"])
    if r == "HIGH" or r == "EXTREME":
        print(" ", c["city"], "-", r)

# sort by temperature, hottest first
# using lambda here like the assignment asked
sorted_list = sorted(
    [c for c in cities if c["temperature"] is not None],
    key=lambda x: x["temperature"],
    reverse=True
)

print()
print("Sorted (hottest to coldest):")
for c in sorted_list:
    print(" ", c["city"], c["temperature"], "C")


# ---------- Exercise 3 ----------
print()
print("Exercise 3 - OOP")
print("----------------")

class ClimateStation:
    def __init__(self, city, temperature, humidity, rainfall):
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.rainfall = rainfall

    def display_summary(self):
        print("City:", self.city)
        print("  Temp:", self.temperature, "C")
        print("  Humidity:", self.humidity, "%")
        print("  Rainfall:", self.rainfall, "mm")

    def calculate_risk(self):
        # same logic as before, just inside the class now
        if self.temperature >= 40:
            return "EXTREME"
        elif self.temperature >= 35 or self.rainfall < 5:
            return "HIGH"
        elif self.temperature >= 30 or self.rainfall < 15:
            return "MODERATE"
        else:
            return "LOW"

    def update_temperature(self, new_temperature):
        self.temperature = new_temperature
        print(self.city, "temp changed to", new_temperature, "C")


# making 5 stations
station1 = ClimateStation("Damascus", 38, 30, 2)
station2 = ClimateStation("Aleppo", 35, 40, 8)
station3 = ClimateStation("Homs", 41, 20, 0)
station4 = ClimateStation("Latakia", 29, 70, 20)
station5 = ClimateStation("Hama", 33, 50, 10)

all_stations = [station1, station2, station3, station4, station5]

print()
print("All stations:")
for s in all_stations:
    s.display_summary()
    print("  Risk:", s.calculate_risk())
    print()

# quick test on the update method
print("Testing update_temperature on Damascus...")
station1.update_temperature(42)
print("New risk:", station1.calculate_risk())


# child class
class SmartClimateStation(ClimateStation):
    def __init__(self, city, temperature, humidity, rainfall, sensor_status):
        # call the parent constructor first
        super().__init__(city, temperature, humidity, rainfall)
        self.sensor_status = sensor_status

    def check_sensor(self):
        if self.sensor_status == "OK":
            print(self.city + ": sensor working fine")
        else:
            print(self.city + ": sensor needs fixing!")

    # bonus method
    def recommendation(self):
        r = self.calculate_risk()
        if r == "LOW":
            return "Normal monitoring"
        elif r == "MODERATE":
            return "Continue monitoring"
        elif r == "HIGH":
            return "Increased monitoring recommended"
        else:
            return "Immediate attention required"


print()
print("Smart stations:")
print("---------------")

smart1 = SmartClimateStation("Damascus", 38, 30, 2, "OK")
smart2 = SmartClimateStation("Homs",     41, 20, 0, "FAULTY")
smart3 = SmartClimateStation("Latakia",  29, 70, 20, "OK")
smart4 = SmartClimateStation("Aleppo",   35, 40, 8, "OK")
smart5 = SmartClimateStation("Hama",     33, 50, 10, "FAULTY")

smart_list = [smart1, smart2, smart3, smart4, smart5]

for s in smart_list:
    s.display_summary()          # from parent class
    s.check_sensor()             # own method
    print("  Risk:", s.calculate_risk())
    print("  Recommendation:", s.recommendation())
    print()