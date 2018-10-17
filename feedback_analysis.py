# zgarnij wszystko w klasę
# rób tylko na dictionaries
#  OGARNIJ LEPIEJ CZYTANIE Z CSV... BO OBCIACH TROCHE NO ALE NO...
# POMYŚL JAK ŁADNIE PRZEDTSAWIĆ DYSTRYBUCJĘ

import csv
import json


class Feedback:

    def __init__(self, file_path):
        if file_path.lower().endswith(".json"):
            self.feedback = Feedback.read_json(file_path)

        elif file_path.lower().endswith(".csv"):
            self.feedback = Feedback.read_csv(file_path)

        else:
            raise ValueError("This file format is not supported yet.")

    def distribution_fellow_passengers(self):
        number_of_fellow_passengers = self.feedback["number_of_fellow_passengers"]
        distribution = dict((str(x) + " passengers have", str(number_of_fellow_passengers.count(x)) + " fellow passengers") for x in set(number_of_fellow_passengers))
        return distribution

    def calculate_average_compensation_per_passenger(self):
        compensation_per_passenger = []
        for compensation, passengers in zip(self.feedback['total_compensation_amount'],
                                            self.feedback['number_of_fellow_passengers']):
            if compensation != 0:
                compensation_per_passenger.append(compensation / (passengers + 1))
        if len(compensation_per_passenger) == 0:
            raise ZeroDivisionError("There are no passengers that got the compensation")
        return sum(compensation_per_passenger) / len(compensation_per_passenger)

    def calculate_most_popular_airline(self):
        return max(set(self.feedback["airline_code"]), key=self.feedback["airline_code"].count)

    def calculate_got_compensation_percentage(self):
        count_receive = 0
        for compensation in self.feedback["did_receive_compensation"]:
            if compensation == 1:
                count_receive += 1

        if self.feedback["did_receive_compensation"] == 0:
            raise ZeroDivisionError("Did_receive_compensation column is empty.")
        return count_receive / len(self.feedback["did_receive_compensation"]) * 100

    @staticmethod
    def read_csv(file_path):
        with open(file_path, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            data = dict([('message', []), ('airline_code', []), ('number_of_fellow_passengers', []),
                         ('did_receive_compensation', []), ('total_compensation_amount', [])])
            for row in reader:
                data['message'].append(row['message'])
                data['airline_code'].append(row['airline_code'])
                data['number_of_fellow_passengers'].append(row['number_of_fellow_passengers'])
                data['did_receive_compensation'].append(row['did_receive_compensation'])
                data['total_compensation_amount'].append(row['total_compensation_amount'])

        return data

    @staticmethod
    def read_json(file_path):
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError("There is no such file.")


f = Feedback('testowy.json')
print(f.distribution_fellow_passengers())
