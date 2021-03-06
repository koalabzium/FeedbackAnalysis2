import csv
import json


class Feedback:

    def __init__(self, file_path):
        if file_path.lower().endswith(".json"):
            feedback = Feedback.read_json(file_path)

        elif file_path.lower().endswith(".csv"):
            feedback = Feedback.read_csv(file_path)
        else:
            raise ValueError("This file format is not supported yet.")

        self.feedback = feedback

    def distribution_fellow_passengers(self):
        number_of_fellow_passengers = self.feedback["number_of_fellow_passengers"]
        distribution = [(x, number_of_fellow_passengers.count(x)) for x in set(number_of_fellow_passengers)]

        for el, key in sorted(distribution):
            print("Having " + str(el) + " fellow passengers has occurred " + str(key) + " times.")

        return distribution

    def calculate_average_compensation_per_passenger(self):
        compensation_per_passenger = []
        for compensation, passengers in zip(self.feedback["total_compensation_amount"],
                                            self.feedback["number_of_fellow_passengers"]):
            if compensation != 0:
                compensation_per_passenger.append(compensation / (passengers + 1))
        if len(compensation_per_passenger) == 0:
            raise ZeroDivisionError("There are no passengers that got the compensation")

        return sum(compensation_per_passenger) / len(compensation_per_passenger)

    def find_most_popular_airline(self):
        airline_code = self.feedback["airline_code"]
        if len(airline_code) == 0:
            raise ValueError("airline_code column is empty")
        result = []
        airline_summary = [(x, airline_code.count(x)) for x in set(airline_code)]
        airline_summary = sorted(airline_summary, key=lambda x: -x[1])
        max_value = airline_summary[0][1]
        for k, v in airline_summary:
            if v == max_value:
                result.append(k)
            else:
                break
        return set(result)

    def calculate_got_compensation_percentage(self):
        did_receive_compensation = self.feedback["did_receive_compensation"]
        if len(did_receive_compensation) == 0:
            raise ZeroDivisionError("Did_receive_compensation column is empty, zero division")
        count_receive = did_receive_compensation.count(1)
        return count_receive / len(did_receive_compensation) * 100

    def extract_messages(self):
        return self.feedback["message"]

    @staticmethod
    def read_csv(file_path):
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            data = dict([("message", []), ("airline_code", []), ("number_of_fellow_passengers", []),
                         ("did_receive_compensation", []), ("total_compensation_amount", [])])
            for row in reader:
                for key, el in row.items():
                    if key == "message" or key == "airline_code":
                        data[key].append(el)
                    else:
                        data[key].append(int(el))
        Feedback.find_missing_data(data)
        return data

    @staticmethod
    def read_json(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
        Feedback.find_missing_data(data)
        return data

    @staticmethod
    def find_missing_data(d):
        for key in d:
            for el in d[key]:
                if el != el:
                    raise ValueError("There is data missing")
