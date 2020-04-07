import json
import requests
from os.path import dirname, join
from datetime import date as Date
from datetime import timedelta

URL_BASE = "https://covid19.mathdro.id/api/" #daily/3-31-2020"
PATH = dirname(__file__)
# Initial date
def update_data():
    date = Date(2020, 1, 27)
    cases_history = {}
    while date < Date.today():
        date_str = date.strftime('%m-%d-%Y')
        print(URL_BASE + "daily/" + date_str)
        datas = requests.get(URL_BASE + "daily/" + date_str)
        datas = json.loads(datas.text)
        for data in datas:
            countryRegion = data['countryRegion']
            if countryRegion == "Mainland China":
                countryRegion = "China"
            countryRegion = countryRegion.lower()
            if not countryRegion in cases_history:
                cases_history[countryRegion] = {}
            #print(type(cases_history[countryRegion]))
            if not date_str in cases_history[countryRegion]:
                cases_history[countryRegion][date_str] = int(data["confirmed"])
            else:
                cases_history[countryRegion][date_str] += int(data["confirmed"])
        date = date + timedelta(days=1)

    file = open(join(PATH, 'data', 'cases_history.json'), 'w')
    file.writelines(json.dumps(cases_history, indent=4))
    file.close()
    print("done.")

if __name__ == "__main__":
    update_data()