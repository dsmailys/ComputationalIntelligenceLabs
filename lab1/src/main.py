import csv
import os.path
from CampaignDetails import CampaignDetails

data_list = []

dataFile = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Clothing_Store.txt'))
with open(dataFile, 'rb') as csv_file:
    reader = csv.reader(csv_file)
    next(reader, None)  # Skip the header.
    # Unpack the row directly in the head of the for loop.
    for name in reader:
        data_list.append(CampaignDetails(name))