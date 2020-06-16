import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import logging
from datetime import date

API_KEY = "[my_api_key]"
YEAR = '2019'
INSTITUTIONS_LIST = {
    "7002135" : "UB",
    "7005264" : "IEP",
    "7010019" : "INP",
    "7001791" : "UB",
    "7001750" : "UB_BX1",
    "7001792" : "UBM",
    "7001793" : "UB_BX4"
}
SEARCH_ITEMS = ["recherche","carte-mentale","classification","atlas","auteurs","chronologie"]
RECORDS_VIEW_ITEMS = ["encyclopedie","media","dictionnaire","evenement","datapays"]

def print_dict(dict):
    return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(dict["total"],dict["01"],dict["02"],dict["03"],dict["04"],dict["05"],dict["06"],dict["07"],dict["08"],dict["09"],dict["10"],dict["11"],dict["12"])

def write_counter_report(name, YEAR, regular_searches, regular_views ):
    report = open("/media/sf_Partage_LouxBox/{}_{}_Universalis_DB1_R4.tsv".format(YEAR,name), "w")
    report.write("Database Report 1 (R4)\tTotal Searches, Result Clicks and Record Views by Month and Database\n")
    report.write("{}\n".format(name))
    report.write("33PUDB_{}\n".format(name))
    report.write("Period covered by Report:\n")
    report.write("{0}-01-01 to {0}-12-31\n".format(YEAR))
    report.write("Date run:\n")
    report.write("{}\n".format(today.strftime("%Y-%m-%d")))
    report.write("Database\tPublisher\tPlatform\tUser Activity\tReporting Period Total\tJan-{0}\tFeb-{0}\tMar-{0}\tApr-{0}\tMay-{0}\tJun-{0}\tJul-{0}\tAug-{0}\tSep-{0}\tOct-{0}\tNov-{0}\tDec-{0}\n".format(YEAR))
    report.write("Universalis\tEncyclopaedia universalis France\tUniversalis\tRegular Searches\t{}\n".format(print_dict(regular_searches)))
    report.write("Universalis\tEncyclopaedia universalis France\tUniversalis\tRecord Views\t{}\n".format(print_dict(record_views)))
    report.close()


today = date.today()
regular_searches = {"total" : 0,"01" : 0,"02" : 0,"03" : 0,"04" : 0,"05" : 0,"06" : 0,"07" : 0,"08" : 0,"09" : 0,"10" : 0,"11" : 0, "12" : 0}
record_views = {"total" : 0,"01" : 0,"02" : 0,"03" : 0,"04" : 0,"05" : 0,"06" : 0,"07" : 0,"08" : 0,"09" : 0,"10" : 0,"11" : 0, "12" : 0}
months_list = ["01","02","03","04","05","06","07","08","09","10","11","12"]
rejected_label = []
anomalies = open("/media/sf_Partage_LouxBox/termes_non_retenus_{}_Universalis_DB1_R4.tsv".format(YEAR), "w")

for id_site,name_site in INSTITUTIONS_LIST.iteritems():
    print("- {}".format(name_site))
    regular_searches_inst = {"total" : 0,"01" : 0,"02" : 0,"03" : 0,"04" : 0,"05" : 0,"06" : 0,"07" : 0,"08" : 0,"09" : 0,"10" : 0,"11" : 0, "12" : 0}
    record_views_inst = {"total" : 0,"01" : 0,"02" : 0,"03" : 0,"04" : 0,"05" : 0,"06" : 0,"07" : 0,"08" : 0,"09" : 0,"10" : 0,"11" : 0, "12" : 0}

    for month in months_list:
        print("- {}".format(month))
        url = "http://www.universalis-edu.com/statistiques/index.php?module=API&method=Actions.getPageUrls&format=JSON&idSite={0}&period=range&date={1}-{2}-01,{1}-{2}-31&flat=0&token_auth={3}&filter_limit=100".format(id_site,YEAR,month,API_KEY)
        session = requests.Session()
        response = session.request(
                    method="GET",
                    url=url)
        for item in response.json():
            if item["label"] in SEARCH_ITEMS:
                regular_searches["total"] += item["nb_hits"]
                regular_searches[month] += item["nb_hits"]
                regular_searches_inst["total"] += item["nb_hits"]
                regular_searches_inst[month] += item["nb_hits"]
            elif item["label"] in RECORDS_VIEW_ITEMS:
                record_views["total"] += item["nb_visits"]
                record_views[month] += item["nb_visits"] 
                record_views_inst["total"] += item["nb_visits"]
                record_views_inst[month] += item["nb_visits"] 
            else:
                if item["label"].encode('utf-8') not in rejected_label:
                    rejected_label.append(item["label"].encode('utf-8'))

    write_counter_report(name_site, YEAR, regular_searches_inst, record_views_inst )
write_counter_report("NETWORK", YEAR, regular_searches, record_views )
anomalies.write("\n".join(rejected_label))
anomalies.close()