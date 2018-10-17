import random
import json
import csv


def generate_random_data(passenger_amount):
    data = dict(message=["Hi, I am the feedback message"] * passenger_amount,
                airline_code=[str(random.randint(0, 5)) for i in range(passenger_amount)],
                number_of_fellow_passengers=[random.randint(0, 17) for i in range(passenger_amount)],
                did_receive_compensation=[random.randint(0, 1) for i in range(passenger_amount)])
    data["total_compensation_amount"] = [random.randint(1000, 10000) if data["did_receive_compensation"][i] == 1
                                         else 0 for i in range(passenger_amount)]
    return data


def serialize_to_json(data, file_path):
    with open(file_path, "w") as fp:
        json.dump(data, fp)


def serialize_to_csv(data, file_path):
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["message", "airline_code", "number_of_fellow_passengers",
                                                     "did_receive_compensation", "total_compensation_amount"])
        writer.writeheader()
        for i in range(len(data["message"])):
            temp = {}
            for name in writer.fieldnames:
                temp[name] = data[name][i]
            writer.writerow(temp)

data = generate_random_data(10)
serialize_to_json(data, "testowy.json")
serialize_to_csv(data, "testowy.csv")
