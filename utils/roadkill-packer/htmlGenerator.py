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
'''

html_ending = '''            </tbody>
        </table>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.11.0/bootstrap-table.min.js"></script>
    </body>
</html>
'''

with open('input.csv', newline='') as input_file:
    rows = csv.reader(input_file)
    with open('output.html', 'w') as output_file:
        output_file.write(html_beginning)
        is_first_line = True
        for row in rows:
            if is_first_line:
                output_file.write('                <tr>\n')
                for column in row:
                    output_file.write('                    <th data-sortable="true">' + column + '</th>\n')
                output_file.write('                </tr>\n')
                output_file.write('            </thead>\n')
                output_file.write('            <tbody>\n')
                is_first_line = False
            else:
                output_file.write('                <tr>\n')
                for column in row:
                    output_file.write('                    <td>' + column + '</td>\n')
                output_file.write('                </tr>\n')
        output_file.write(html_ending)
