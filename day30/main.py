
#FileNotFund:
with open("a_file.txt") as file:
    file.read()

# KeyError:
dict = {"key":"value"}
value = dict["non_existent_key"]

# IndexError
fruit_list = ["apple", "banana", "pear"]
fruit = fruit_list[3]

# TypeError
text = "abc"
print(text+5)

# challengue
try:
    file = open("a_file.txt")
    a_dictionary = {"key":"value"}
    print(a_dictionary["key"])
except FileNotFoundError:
    open("a_file", "w")
    file.write("something")
except KeyError as error_message:
    print(f"that key {error_message} does not exist")
else:
    content = file.read()
    print(content)
finally:
    raise KeyError("This is an error that I made up")

height = float(input("Height: "))
weight = int(input("Weight: "))

if height > 3:
    raise ValueError("Human height should not be over 3 meters")
bmi = weight / height**2
print(bmi)



