import pandas as pd
import csv
import pytest
import os
from datetime import datetime
import zipcode
import BeautifulSoup


def get_zipcode_info(in_zip):
    parsed_zip = in_zip[0:5]
    zip = zipcode.isequal(parsed_zip)
    data = {}
    print zip
    data["zip"] = zip.zip
    data["city"] = zip.city
    data["state"] = zip.state
    return data


def load_itunes_report(file):
    data = pd.read_csv(
        file,
        sep="\t",
        header=0,
        parse_dates=["Download Date"],
        index_col=None,
        )
    return data


def update_svg_map(file):
    svg = open(file, 'r').read()
    soup = BeautifulSoup.BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])


def parse_folder_for_itunes_reports(folder):
    filelist = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt") and file.startswith("iTunesTrendingReport-"):
                filelist.append(file)
    return filelist


def load_itunes_reports_from_dir(folder):
    out_files = parse_folder_for_itunes_reports(folder)
    data_array = []
    for file in out_files:
        data = load_itunes_report(file)
        data_array.append(data)
    all_data = pd.concat(data_array)
    print all_data.groupby("Track Name").size()


def main():
    load_itunes_reports_from_dir(r"./Reports")

if __name__=="__main__":
    main()