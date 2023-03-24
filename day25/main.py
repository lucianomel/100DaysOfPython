# with open("./weather_data.csv") as csv_data:
#     data = csv_data.readlines()

# print(data)

# import csv
#
# with open("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     temperatures = []
#     # Get second row
#     for row in data:
#         temperatures.append(row[1])
#     # Remove first element
#     temperatures = temperatures[1:]
#     # Turn type string into int
#     for i in range(len(temperatures)):
#         temperatures[i] = int(temperatures[i])
#     print(temperatures)

# PANDAS!
# import pandas
#
# data = pandas.read_csv("weather_data.csv")
# # print(data)
# # print(type(data["temp"]))
# # print(type(data))
#
# data_dict = data.to_dict()
# print(data_dict)
#
# temp_list = data["temp"].to_list()
# print(temp_list)
#
# # Way 1
# print(data["temp"].mean())
#
# # Way 2
# n_temps = 0
# temp_sum = 0
# for temp in temp_list:
#     temp_sum += temp
#     n_temps += 1
# mean_temp = temp_sum / n_temps
#
# print(mean_temp)
#
# # Getting the max temperature
# print(data["temp"].max())
#
# # Another way (like an object)
# print(data.condition)
#
# # Geta in the rows of a dataframe
# print(data.iloc[[0]])
# # This way gets all rows where day is Monday
# print(data[data.day == "Monday"])
# # Row of data where temp was max
# print(data[data.temp == data.temp.max()])
# # Getting that particular row condition
# print(data[data.temp == data.temp.max()].condition)
# # Or
# monday = data[data.day == "Monday"]
# print(monday.condition)
# # Challenge:get mondays temperature in farenheit
# monday_temp = data[data.day == "Monday"].temp.iloc[0]
# print(f"In celcius: {monday_temp}")
# monday_temp_fahrenheit = (9/5)*int(monday_temp)+32
# print(f"In fahrenheit: {monday_temp_fahrenheit}")
#
# # Create a df from scratch
# data_dict = {
#     "students": ["Amy", "James", "Angela"],
#     "scores": [76, 56, 65]
# }
#
# df = pandas.DataFrame(data= data_dict)
#
# df.to_csv("new_data.csv")
# print(df)
#
import pandas as pd

# Create a csv squirrel_count.csv that has squirrel color (how many) -> Fur colour and count

df = pd.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
COLORS = ["Gray", "Cinnamon", "Black"]

colors_dict = {"Fur Color": COLORS, "count": []}
for color in COLORS:
    colors_dict["count"].append(df[df["Primary Fur Color"] == color].count()["Primary Fur Color"])
print(colors_dict)

df_fur_colors = pd.DataFrame(colors_dict)

print(df_fur_colors)