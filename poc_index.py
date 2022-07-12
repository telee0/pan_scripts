"""

Script to process POC index for Google Data Studio feed

written by Terence <telee@paloaltonetworks.com>

[20220125]

"""

import csv


in_file_name = 'POC Reports Data Set 2022012501'

in_file = open(in_file_name + '.csv', 'r')
out_file = open(in_file_name + '_processed.csv', 'w', newline='')

countries = {
    "cn": "China",
    "hk": "Hong Kong",
    "us": "United States",
    "anz": "ANZ"
}

country_codes = {
    "australia": "AU",
    "australia and new zealand": "ANZ",
    "china": "CN",
    "france": "FR",
    "hong kong": "HK",
    "india": "IN",
    "indonesia": "ID",
    "italy": "IT",
    "japan": "JP",
    "macao": "MO", "macau": "MO",
    "malaysia": "MY",
    "philippines": "PH",
    "singapore": "SG",
    "thailand": "TH",
    "taiwan": "TW",
    "united states": "US",
    "vietnam": "VN"
}


r = csv.reader(in_file, delimiter=',', quotechar='"')
w = csv.writer(out_file, delimiter=',', quotechar='"')

# in_file.__next__()

poc_count = 0

keywords = set()

for poc in r:
    if poc[0] == '':
        continue  # skip blank lines or lines with no POC number

    # hardcoded indexes as i++ not available in python

    poc_number = poc[0]
    devices = poc[1]
    os_versions = poc[2]
    tester = poc[3]
    industry = poc[4]
    feature_list = poc[5]
    url = poc[6]
    approved_date = poc[7]
    delivery_date = poc[8]
    poc_engineer = poc[9]
    systems_engineer = poc[10]
    account_team = poc[11]
    country_code = ""

    device_list = devices.split('/')

    if os_versions.lower() == 'n/a':
        os_version_list = [os_versions]
    else:
        os_version_list = os_versions.split('/')


    #
    # convert feature lines into a set of keywords
    #

    features = feature_list.split(',')
    for feature in features:
        keywords.add(feature.strip())

    #
    #
    #

    se_list = systems_engineer.split('/')

    if len(se_list) > 1 and account_team == "":
        systems_engineer = se_list[0].strip()
        account_team = se_list[1].strip()
        country = countries.get(account_team.lower())
        if country:
            account_team = country
        else:
            country = account_team
        poc[10] = systems_engineer
        poc[11] = account_team

    # print(f"country = {country}, country_code = {country_code}")

    country_code = country_codes.get(account_team.lower())
    poc.append(country_code)

    device_type = ''

    for device in device_list:
        device = device.strip()

        if device.lower().startswith("pa"):
            device_type = 'PA'              # NGFW
        elif device.lower().startswith("vm"):
            device_type = "VM"              # VM series
        elif device.lower().startswith("sd-wan"):
            device_type = "SD-WAN"          # SD-WAN (Prisma SD-WAN or PAN-OS SD-WAN)
        elif device[:1].isdigit():
            device = device_type + '-' + device

        for os_version in os_version_list:
            os_version = os_version.strip()

            # print(f"{device}:{os_version}")

            poc[1] = device
            poc[2] = os_version

            # print(poc)
            w.writerow(poc)

    # print(device_list)
    print()

    poc_count = poc_count + 1


print(f"\nNumber of rows: {poc_count}")
print("list of the keywords\n", keywords)
for keyword in sorted(keywords):
    print(keyword)