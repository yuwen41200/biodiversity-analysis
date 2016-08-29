#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

html_beginning = '''<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.11.0/bootstrap-table.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
    </head>
    <body>
        <table data-toggle="table" data-pagination="true">
            <thead>
                <tr>
                    <th data-sortable="true">id</th>
                    <th data-sortable="true">family</th>
                    <th data-sortable="true">taxonRemarks</th>
                    <th data-sortable="true">scientificName</th>
                    <th data-sortable="true">vernacularName</th>
                    <th data-sortable="true">previousIdentifications</th>
                    <th data-sortable="true">individualCount</th>
                    <th data-sortable="true">occurrenceRemarks</th>
                    <th data-sortable="true">modified</th>
                    <th data-sortable="true">eventRemarks</th>
                    <th data-sortable="true">institutionCode</th>
                    <th data-sortable="true">eventDate</th>
                    <th data-sortable="true">recordedBy</th>
                    <th data-sortable="true">rightsHolder</th>
                    <th data-sortable="true">municipality</th>
                    <th data-sortable="true">rights</th>
                    <th data-sortable="true">decimalLongitude</th>
                    <th data-sortable="true">decimalLatitude</th>
                    <th data-sortable="true">fieldNotes</th>
                    <th data-sortable="true">identificationVerificationStatus</th>
                    <th data-sortable="true">recordNumber</th>
                    <th data-sortable="true">materialSampleID</th>
                    <th data-sortable="true">locationRemarks</th>
                    <th data-sortable="true">associatedReferences</th>
                    <th data-sortable="true">associatedMedia</th>
                    <th data-sortable="true">basisOfRecord</th>
                    <th data-sortable="true">language</th>
                    <th data-sortable="true">continent</th>
                    <th data-sortable="true">country</th>
                    <th data-sortable="true">countryCode</th>
                </tr>
            </thead>
            <tbody>
'''

html_ending = '''            </tbody>
        </table>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.11.0/bootstrap-table.min.js"></script>
    </body>
</html>
'''


def generate(input_path, output_path):
    """
    Generate an HTML web page from a CSV file.

    :param input_path: Path of input (CSV) file.
    :param output_path: Path of output (HTML) file.
    :return: None.
    """

    with open(input_path, newline='') as input_file:
        rows = csv.reader(input_file)
        next(rows, None)
        with open(output_path, 'w') as output_file:
            output_file.write(html_beginning)
            for row in rows:
                output_file.write('                <tr>\n')
                for no, column in enumerate(row):
                    if no < 23:
                        output_file.write('                    <td>' + column + '</td>\n')
                    else:
                        output_file.write('                    <td><a href="' + column + '" target="_blank">' + column + '</a></td>\n')
                output_file.write('                    <td>HumanObservation</td>\n')
                output_file.write('                    <td>zh-Hant-TW</td>\n')
                output_file.write('                    <td>Asia</td>\n')
                output_file.write('                    <td>Taiwan</td>\n')
                output_file.write('                    <td>TW</td>\n')
                output_file.write('                </tr>\n')
            output_file.write(html_ending)
