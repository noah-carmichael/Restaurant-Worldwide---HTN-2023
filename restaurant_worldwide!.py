import cohere
import serial
import time


# ardiuno stuff
arduino_port = "COM4" # serial port of Arduino, change if necessary
baud = 9600 # arduino uno runs at 9600 baud
ser = serial.Serial(arduino_port, baud)

print("Restaurant Worldwide!\n")

# when called, reads the serial monitor for controller input
def check_serial():
    while True:
        getData=ser.readline()
        dataString = getData.decode('utf-8')
        data=dataString[0:][:-2]
        # print(data)
        if int(data) >= 1000: # down, wires up
            return "D"
        if int(data) <= 60: # up, wires up       
            return "U"     
        
# # writes to the serial monitor
# def write_read(x):
#     ser.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = ser.readline()
#     return data


# initialize the Cohere Client with an API Key
co = cohere.Client('pS5EODFdSJ8qm02qMvV0YWSGiNBNzYoN4z04pkLD')

# generate a prediction for a prompt
response = co.generate(
    model='7a011a87-c9f0-427e-85fe-dcc1f5d00a51-ft',
    prompt='Generate 2 different types of cuisines from different regions. Return these with the format "%[cuisine 1]%, @[cuisine 2]@"',
  temperature=0.9,  
  max_tokens=100
)
# For example: Mexican, American, Italian, French, Japanese, Indian. See country training data for more examples

reponse = format(response.generations[0].text)
indexes_1 = [i for i in range(len(reponse)) if reponse[i] == "%"]
indexes_2 = [i for i in range(len(reponse)) if reponse[i] == "@"]

print("Cuisine types:")
# write_read("Cuisine types:")
print(reponse[indexes_1[0]+1:indexes_1[1]].title() + ", " + reponse[indexes_2[0]+1:indexes_2[1]].title())

print("Up or down option?")
user_country = check_serial()
if user_country == "U":
    cuisine_type = reponse[indexes_1[0]+1:indexes_1[1]]
if user_country == "D":
    cuisine_type = reponse[indexes_2[0]+1:indexes_2[1]]

print(cuisine_type.title())



response_2 = co.generate(
    model='4a6a555c-311e-4774-b78c-eb15d3fcd145-ft',
    prompt=f'Generate 2 different main courses commonly found in {cuisine_type} cuisine. Return these with the format "%[dish 1]%, @[dish 2]@"',
  temperature=0.9,  
  max_tokens=100
)

reponse_2 = format(response_2.generations[0].text)
indexes_main_1 = [i for i in range(len(reponse_2)) if reponse_2[i] == "%"]
indexes_main_2 = [i for i in range(len(reponse_2)) if reponse_2[i] == "@"]

print("\nMain course options:")
print(reponse_2[indexes_main_1[0]+1:indexes_main_1[1]].title() + ", " + reponse_2[indexes_main_2[0]+1:indexes_main_2[1]].title())


print("Up or Down option?")
user_main = check_serial()
if user_main == "U":
    main = reponse_2[indexes_main_1[0]+1:indexes_main_1[1]]
if user_main == "D":
    main = reponse_2[indexes_main_2[0]+1:indexes_main_2[1]]



# desserts
response_3 = co.generate(
    model='6e814468-328b-446c-af34-5be0e5d95abd-ft',
    prompt=f'Generate 2 different desserts commonly found in {cuisine_type} cuisine. Return these with the format "%[dessert 1]%", @[dessert 2]@"',
  temperature=0.9,  
  max_tokens=100
)

reponse_3 = format(response_3.generations[0].text)
indexes_dessert_1 = [i for i in range(len(reponse_3)) if reponse_3[i] == "%"]
indexes_dessert_2 = [i for i in range(len(reponse_3)) if reponse_3[i] == "@"]

print("\nDessert options: ")
print(reponse_3[indexes_dessert_1[0]+1:indexes_dessert_1[1]].title() + ", " + reponse_3[indexes_dessert_2[0]+1:indexes_dessert_2[1]].title())


print("Up or Down option?")
user_dessert = check_serial()
if user_dessert == "U":
    dessert = reponse_3[indexes_dessert_1[0]+1:indexes_dessert_1[1]]
if user_dessert == "D":
    dessert = reponse_3[indexes_dessert_2[0]+1:indexes_dessert_2[1]]

print(dessert.title())



# price generator
def price(item):
    gener = co.generate(
        model='f98da576-a48f-49f2-a37c-1f76eda4a14f-ft',
        prompt=f'Generate the price of one plate of {item}. It must be between $8 and $40. Return with the format "%[$price]%"',
    temperature=0.9,  
    max_tokens=10
    )

    # print(gener)
    price_final = format(gener.generations[0].text)
    return price_final


main_price = price(main)
dessert_price = price(dessert)

print(f"""\n\nYour order is:
      
    {main.title()} - {main_price}
    {dessert.title()} - {dessert_price}

    TAX: ${round((int(main_price[2:])+int(dessert_price[2:]))*0.13, 2)}
    TOTAL: ${round((int(main_price[2:])+int(dessert_price[2:]))*1.13, 2)}
    """)