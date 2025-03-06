# filename: generate_csv_report.py

import pandas as pd
import os

def generate_html():
    # Get CSV files in the current working directory
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the current directory.")
        return

    # Initial load with the first CSV file
    initial_csv = csv_files[0]
    df = pd.read_csv(initial_csv, quotechar='"')

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSV Report Viewer</title>
        <style>
            body {{
                background-color: #121212;
                color: #E0E0E0;
                font-family: Arial, sans-serif;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
            th {{
                cursor: pointer;
                background-color: #333333;
            }}
            tr:nth-child(even) {{
                background-color: #1E1E1E;
            }}
            tr:nth-child(odd) {{
                background-color: #282828;
            }}
            #searchInput {{
                margin-bottom: 10px;
                padding: 8px;
                width: 100%;
                box-sizing: border-box;
            }}
        </style>
    </head>
    <body>
    
    <h2>CSV Report Viewer</h2>

    <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search...">

    <label for="csvSelect">Select CSV File:</label>
    <select id="csvSelect" onchange="loadCSV(this.value)">
    {''.join(f'<option value="{file}">{file}</option>' for file in csv_files)}
    </select>

    <table id="dataTable">
        <thead>
            <tr>
                {"".join(f"<th onclick='sortTable({i})'>{col}</th>" for i, col in enumerate(df.columns))}
            </tr>
        </thead>
        <tbody>
            {"".join("<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>" for row in df.values)}
        </tbody>
    </table>

    <script>
    function sortTable(columnIndex) {{
        var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
        table = document.getElementById("dataTable");
        switching = true;
        dir = "asc"; 
        while (switching) {{
            switching = false;
            rows = table.rows;
            for (i = 1; i < (rows.length - 1); i++) {{
                shouldSwitch = false;
                x = rows[i].getElementsByTagName("TD")[columnIndex];
                y = rows[i + 1].getElementsByTagName("TD")[columnIndex];
                if (dir == "asc") {{
                    if (isNumeric(x.innerHTML) && isNumeric(y.innerHTML)) {{
                        if (parseFloat(x.innerHTML) > parseFloat(y.innerHTML)) {{
                            shouldSwitch = true;
                            break;
                        }}
                    }} else {{
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {{
                            shouldSwitch = true;
                            break;
                        }}
                    }}
                }} else if (dir == "desc") {{
                    if (isNumeric(x.innerHTML) && isNumeric(y.innerHTML)) {{
                        if (parseFloat(x.innerHTML) < parseFloat(y.innerHTML)) {{
                            shouldSwitch = true;
                            break;
                        }}
                    }} else {{
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {{
                            shouldSwitch = true;
                            break;
                        }}
                    }}
                }}
            }}
            if (shouldSwitch) {{
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                switchcount++;      
            }} else {{
                if (switchcount == 0 && dir == "asc") {{
                    dir = "desc";
                    switching = true;
                }}
            }}
        }}
    }}

    function isNumeric(value) {{
        return !isNaN(parseFloat(value)) && isFinite(value);
    }}

    function loadCSV(fileName) {{
        fetch(fileName)
            .then(function(response) {{ return response.text(); }})
            .then(function(data) {{
                var lines = data.split('\\n');
                var headers = lines[0].split(',');
                var table = document.getElementById('dataTable');
                var newThead = document.createElement('thead');
                var newTbody = document.createElement('tbody');

                var headerRow = document.createElement('tr');
                for (var i = 0; i < headers.length; i++) {{
                    var cell = document.createElement('th');
                    cell.innerHTML = headers[i];
                    cell.setAttribute('onclick', 'sortTable(' + i + ')');
                    headerRow.appendChild(cell);
                }}
                newThead.appendChild(headerRow);
                
                for (var i = 1; i < lines.length; i++) {{
                    var regex = /("([^"]*)")|([^,]+)/g;
                    var cells = [];
                    var match;

                    while ((match = regex.exec(lines[i])) !== null) {{
                        if (match[2] !== undefined) {{
                            cells.push(match[2]); // Quoted value
                        }} else if (match[3] !== undefined) {{
                            cells.push(match[3]); // Unquoted value
                        }}
                    }}

                    var row = document.createElement('tr');
                    for (var j = 0; j < cells.length; j++) {{
                        var cell = document.createElement('td');
                        cell.innerHTML = cells[j];
                        row.appendChild(cell);
                    }}
                    newTbody.appendChild(row);
                }}
                table.innerHTML = '';
                table.appendChild(newThead);
                table.appendChild(newTbody);
            }})
            .catch(function(error) {{
                console.error('Error loading CSV:', error);
            }});
    }}

    function searchTable() {{
        var input, filter, table, tr, td, cell, i, j, txtValue;
        input = document.getElementById("searchInput");
        filter = input.value.toLowerCase();
        table = document.getElementById("dataTable");
        tr = table.getElementsByTagName("tr");

        for (i = 1; i < tr.length; i++) {{
            tr[i].style.display = "none";
            td = tr[i].getElementsByTagName("td");
            for (j = 0; j < td.length; j++) {{
                if (td[j]) {{
                    cell = td[j].textContent || td[j].innerText;
                    if (cell.toLowerCase().indexOf(filter) > -1) {{
                        tr[i].style.display = "";
                        break;
                    }}
                }}
            }}
        }}
    }}
    </script>

    </body>
    </html>
    """

    # Save the HTML content to a file
    with open('csv_report_viewer.html', 'w') as f:
        f.write(html_content)

    print("HTML report viewer generated and saved as 'csv_report_viewer.html'")

generate_html()