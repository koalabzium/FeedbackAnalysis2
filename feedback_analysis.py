# zgarnij wszystko w klasę
# rób tylko na dictionaries
#  OGARNIJ LEPIEJ CZYTANIE Z CSV... BO OBCIACH TROCHE NO ALE NO...

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

    def calculate_average_compensation_per_passenger1(self):
        compensation_per_passenger = []
        for compensation, passengers in zip(self.feedback['total_compensation_amount'], self.feedback['number_of_fellow_passengers']):
            if compensation != 0:
                compensation_per_passenger.append(compensation/(passengers+1))
        if len(compensation_per_passenger) == 0:
            raise ZeroDivisionError("There are no clients that got the compensation")
        return sum(compensation_per_passenger)/len(compensation_per_passenger)

    def calculate_average_compensation_per_passenger2(self):

        total_compensation_sum = sum(self.feedback['total_compensation_amount'])
        passenger_number_sum = sum(self.feedback['number_of_fellow_passengers']) + len(self.feedback['number_of_fellow_passengers'])
        if passenger_number_sum == 0:
            raise ZeroDivisionError("Number_of_fellow_passengers column is empty")
        return total_compensation_sum/passenger_number_sum


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
print(f.calculate_got_compensation_percentage())