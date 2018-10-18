from feedback_analysis import Feedback
from create_data import generate_random_data, serialize_to_csv, serialize_to_json


def main():
    data = serialize_to_csv(generate_random_data(10), 'test_data.csv')
    f = Feedback('test_data.csv')
    print(f.calculate_average_compensation_per_passenger())
    f.distribution_fellow_passengers()
    print(f.extract_messages())
    print(f.find_most_popular_airline())
    print(f.calculate_got_compensation_percentage())



if __name__ == "__main__":
    main()
