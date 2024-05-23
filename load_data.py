
import csv
import requests
import json


def read_data_files(data_path: str) -> dict:

    with open(f"{data_path}\\departments.csv") as csv_file:
        departments_reader = csv.reader(csv_file, delimiter=',')
        departments = [{
                        "id": dep[0],
                        "department": dep[1]
                       } for dep in departments_reader]

    with open(f"{data_path}\\jobs.csv") as csv_file:
        jobs_reader = csv.reader(csv_file, delimiter=',')
        jobs = [{
                    "id": job[0],
                    "job": job[1]
                } for job in jobs_reader]

    with open(f"{data_path}\\hired_employees.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        employees = [{
                        "id": emp[0],
                        "name": emp[1],
                        "datetime": emp[2],
                        "department_id": emp[3] if emp[3] != '' else -1,
                        "job_id": emp[4] if emp[4] != '' else -1
                     } for emp in csv_reader]

    return {
        "departments": departments,
        "jobs": jobs,
        "employees": employees
    }


if __name__ == "__main__":

    # TODO: send to .env file
    DATA_PATH = "I:\\Raposera\\pruebas\\globant\\data_challenge_files"
    API_URL = "http://127.0.0.1:8000"

    try:
        # drop data
        restart_schema = API_URL + "/restart-schema/"
        response = requests.delete(restart_schema)
        if response.status_code != 200:
            raise Exception(f"Problem restarting schema: status response {response.status_code}, error: {response.text}")

        # get data from csv files
        company_data = read_data_files(DATA_PATH)
        # print(company_data)

        # load company data
        load_departments = API_URL + "/load-departments/"
        response = requests.post(load_departments, data={"departments": json.dumps(company_data["departments"])})
        if response.status_code != 200:
            raise Exception(f"Problem loading departments: status response {response.status_code}, error: {response.text}")

        load_jobs = API_URL + "/load-jobs/"
        response = requests.post(load_jobs, data={"jobs": json.dumps(company_data["jobs"])})
        if response.status_code != 200:
            raise Exception(f"Problem loading jobs: status response {response.status_code}, error: {response.text}")

        load_employees = API_URL + "/load-employees/"
        response = requests.post(load_employees, data={"employees": json.dumps(company_data["employees"])})
        if response.status_code != 200:
            raise Exception(f"Problem loading employees: status response {response.status_code}, error: {response.text}")

    except Exception as e:
        print("An error occured loading the data: ", e)
