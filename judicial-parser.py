import xml.etree.ElementTree as ET
import csv
from os import path

import requests


PDF_URL_PATTERN = 'http://cjc.ny.gov/Determinations/{}/{}'
XML_URL = 'http://www.scjc.state.ny.us/Determinations/determination_list.xml'


def fetch_data():
    """Check if XML file exists locally, download if not."""
    if not path.isfile('judges.xml'):
        r = requests.get(XML_URL)

        with open('judges.xml', 'w') as f:
            for block in r.iter_content(1024):
                f.write(block)


def handle_none(node):
    try:
        return node.text
    except AttributeError:
        return ''


def parse_data():
    tree = ET.parse('j.xml')
    root = tree.getroot()

    with open('judges.csv', 'w') as f:

        headers = ['last', 'rest', 'judge_title', 'judge_type', 'court',
                   'court_simple', 'court_co', 'result', 'status',
                   'determination', 'determination_year', 'page_link', 'pdf_link',
                   'annual_report_year', 'report_page_no']

        writer = csv.DictWriter(f, fieldnames=headers)

        writer.writeheader()

        for judge in root:
            alph = handle_none(judge.find('Alphabetical_List'))
            court = handle_none(judge.find('Court'))
            court_co = handle_none(judge.find('Court_County_Location'))
            result = handle_none(judge.find('Result'))
            filename = handle_none(judge.find('Determination_File_name'))
            report_page_no = handle_none(
                judge.find('Page_Number_Of_Annual_x0020_Report')
            )
            annual_report_year = handle_none(
                judge.find('Year_of_Annual_Report')
            )
            status = handle_none(judge.find('Status'))
            determination_year = handle_none(
                judge.find('Year_of_Determination')
            )
            rest_name = handle_none(
                judge.find('Name_Last_First')
            ).split(',')[1].strip()
            lname = handle_none(
                judge.find('Name_Last_First')
            ).split(',')[0].strip()
            court_simple = handle_none(judge.find('Court_Simple'))
            judge_title = handle_none(judge.find('Judicial_Title'))
            determination = handle_none(judge.find('Determination'))
            judge_type = handle_none(judge.find('Judge_Type'))
            link = handle_none(judge.find('Link'))
            link_to_pdf = PDF_URL_PATTERN.format(alph, filename)

            writer.writerow({
                'last': lname,
                'rest': rest_name,
                'court': court,
                'court_simple': court_simple,
                'court_co': court_co,
                'result': result,
                'status': status,
                'determination': determination,
                'determination_year': determination_year,
                'judge_title': judge_title,
                'judge_type': judge_type,
                'page_link': link,
                'pdf_link': link_to_pdf,
                'annual_report_year': annual_report_year,
                'report_page_no': report_page_no
            })


if __name__ == '__main__':
    fetch_data()
    parse_data()
