


PCT_COUNTRIES = [
  {"name": "Albania", "code": "AL"},
  {"name": "Argentina", "code": "AR"},
  {"name": "Andorra", "code": "AD"},
  {"name": "Austria", "code": "AT"},
  {"name": "Belarus", "code": "BY"},
  {"name": "Belgium", "code": "BE"},
  {"name": "Bosnia and Herzegovina", "code": "BA"},
  {"name": "Bulgaria", "code": "BG"},
  {"name": "Canada", "code": "CA"},
  {"name": "Croatia", "code": "HR"},
  {"name": "Cyprus", "code": "CY"},
  {"name": "Czech Republic", "code": "CZ"},
  {"name": "Denmark", "code": "DK"},
  {"name": "Estonia", "code": "EE"},
  {"name": "Finland", "code": "FI"},
  {"name": "France", "code": "FR"},
  {"name": "Germany", "code": "DE"},
  {"name": "Greece", "code": "GR"},
  {"name": "Hungary", "code": "HU"},
  {"name": "Iceland", "code": "IS"},
  {"name": "Ireland", "code": "IE"},
  {"name": "Italy", "code": "IT"},
  {"name": "Japan", "code": "JP"},
  {"name": "Korea, Democratic People's Republic of", "code": "KP"},
  {"name": "Korea, Republic of", "code": "KR"},
  {"name": "Kosovo", "code": "XK"},
  {"name": "Latvia", "code": "LV"},
  {"name": "Liechtenstein", "code": "LI"},
  {"name": "Lithuania", "code": "LT"},
  {"name": "Luxembourg", "code": "LU"},
  {"name": "Malta", "code": "MT"},
  {"name": "Moldova", "code": "MD"},
  {"name": "Monaco", "code": "MC"},
  {"name": "Montenegro", "code": "ME"},
  {"name": "Netherlands", "code": "NL"},
  {"name": "North Macedonia", "code": "MK"},
  {"name": "Norway", "code": "NO"},
 {"name": "Pakistan", "code": "PK"},
  {"name": "Poland", "code": "PL"},
  {"name": "Portugal", "code": "PT"},
  {"name": "Romania", "code": "RO"},
  {"name": "Russia", "code": "RU"},
  {"name": "San Marino", "code": "SM"},
  {"name": "Serbia", "code": "RS"},
  {"name": "Slovakia", "code": "SK"},
  {"name": "Slovenia", "code": "SI"},
  {"name": "Spain", "code": "ES"},
  {"name": "Sweden", "code": "SE"},
  {"name": "Switzerland", "code": "CH"},
  {"name": "Taiwan", "code": "TW"},
  {"name": "Ukraine", "code": "UA"},
  {"name": "United Kingdom", "code": "GB"},
  {"name": "Vatican City (Holy See)", "code": "VA"}
]

import csv


# Specify the path and filename for the CSV file
csv_file_path = './countries.csv'

# Write the country data to the CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['name', 'code']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(PCT_COUNTRIES)