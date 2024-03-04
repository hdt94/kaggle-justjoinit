import argparse
from pprint import PrettyPrinter
from typing import Dict

from Analyst import Analyst


def main(data_dir: str, prefix: str = "small" ):
    analyst = Analyst()
    pp = PrettyPrinter(indent=2)

    def update_records_len_str(map, field):
        map[field] = f"[{len(map[field])} records]"

    print("\nCargando datos...")
    report = analyst.read_data_dir(data_dir, prefix)
    update_records_len_str(report, "records_first_jobs")
    update_records_len_str(report, "records_latest_jobs")
    pp.pprint(report)

    print("\nRequerimiento 1")
    report = analyst.requirement_1(2, "PL", "junior")
    update_records_len_str(report, "records")
    pp.pprint(report)

    print("\nRequerimiento 2")
    report = analyst.requirement_2("Gazelle Global IT Recruitment", "2023-08-31", "2023-09-02")
    update_records_len_str(report, "records")
    pp.pprint(report)

    print("\nRequerimiento 3")
    report = analyst.requirement_3("PL", "2023-08-31", "2023-09-02")
    update_records_len_str(report, "records")
    pp.pprint(report)

    print("\nRequerimiento 4")
    report = analyst.requirement_4(10, "2022-04-09", "2023-09-02", "junior", "US")
    update_records_len_str(report, "records")
    pp.pprint(report)

    print("\nRequerimiento 5")
    report = analyst.requirement_5(4, "2022-04-09", "2023-09-02")
    pp.pprint(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-dir")
    parser.add_argument("-p", "--prefix", default="small")
    args = parser.parse_args()
    main(args.data_dir, args.prefix)
