
#!/usr/bin/env python3

import cgi
import pymysql
import cgitb
import json
from decimal import Decimal
from string import Template

# Print content type
print("Content-type: text/html\n\n")



cgitb.enable()
form = cgi.FieldStorage()

def connect_database(database, username, password):
    connection = pymysql.connect(
        host='bioed.bu.edu',
        user=username,
        password=password,
        db=database,
        port=4253
    )
    cursor = connection.cursor()
    return connection, cursor

def execute_query(cursor, query):
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except pymysql.Error as e:
        print(f"Error executing query: {query}")
        print(f"Error message: {e}")
        results = None
    return results

def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")



connection, cursor = connect_database("Team_7", "saumyapo", "saumyapo")

vcf_table = ""

if form:
    # Retrieve form data
    tagid = form.getvalue("tagid")
    scaffoldid = form.getvalue("scaffoldid")
    location = form.getlist("location")
    mortality = form.getlist("mortality")
    year = form.getlist("year_array")
    ecological_vol = form.getvalue("eco_vol_val")
    ln_ecological_vol = form.getvalue("ln_eco_vol_val")
    allele_freq = form.getvalue("allele_freq_val")
    length = form.getvalue("length_val")
    width = form.getvalue("width_val")
    height = form.getvalue("height_val")
    counts = form.getvalue("count")
    averages = form.getvalue("average")
    groupbys = form.getvalue("groupby")
    vcf = form.getvalue("vcf")
    order_by = form.getvalue("order_by")
    
    # For genotype distribution graphs
    scaffold_graph = form.getvalue("scaffold_graph")
    geno_graph = form.getvalue("geno_graph")

    # For line graph
    line_tagid = form.getvalue("line_tagid")

    # Data Modifications
    # Year, Location, ... (checkbox filters) come in as a string 
    # separated by colons, turn this into a python list to iterate over
    if year:
        year = year[0].split(':')
    
    if location:
        location = location[0].split(':')
    
    if mortality:
        mortality = mortality[0].split(':')


    # If form is for graph
    bar_query = ""
    if scaffold_graph:
        bar_query += "SELECT location, count(GT) FROM vcf join y2018 on vcf.CORAL_id = y2018.tagid WHERE CHROM = '" + scaffold_graph + "' AND GT "
        if geno_graph == "Homozygous Alt":
            bar_query += "= '1/1' "
        if geno_graph == "Homozygous Ref":
            bar_query += "= '0/0' "
        if geno_graph == "Heterozygous":
            bar_query += "= '0/1' "
        
        bar_query += " GROUP BY location"


        try:
            # Execute the query
            results = execute_query(cursor, bar_query)
            #print('')
            
            
            plot_data = [list(item) for item in results]
            y_axis = 'Number of ' + str(geno_graph) + ' Individuals'
            plot_data.insert(0,['Location',y_axis])
            plot_data_tuple = tuple(plot_data)

            print(json.dumps(plot_data_tuple))
            
        except pymysql.Error as e:
            error_message = f'<p style="color:red;">Error executing query: {e}</p>'

    ##line graph 
    elif line_tagid:
        line_query = ""
        line_query = 'SELECT year, eco_volume FROM (SELECT *, 2015 as year From y2015 WHERE tagid = %s UNION SELECT *, 2016 as year From y2016 WHERE tagid = "' + str(line_tagid) + '" UNION SELECT *, 2017 as year From y2017 WHERE tagid = "' + str(line_tagid) + '" UNION SELECT *, 2018 as year From y2018 WHERE tagid = "' + str(line_tagid) + '") as y group by year'

        try:
            # Execute the query
            cursor.execute(line_query,[line_tagid])
                    
            results = cursor.fetchall()
            
            plot_data = [list(item) for item in results]
            plot_data.insert(0,['Volume of coral','Year'])
            plot_data_tuple = tuple(plot_data)

            print(json.dumps(plot_data_tuple))
            
        except pymysql.Error as e:
            error_message = f'<p style="color:red;">Error executing query: {e}</p>'


    
    else:
        ####Shortcomings of the query - the groupby doesnt specify the alive and dead within the groupby mortality
        zquery = ""
        for i in year: 
        #select statement
            zquery += "SELECT *, " 
            if groupbys != "None":
                if counts == "Yes":
                    zquery += " count(" + groupbys + '), '
                if averages != "None":
                    zquery += "avg(" + averages + '), ' 
            zquery += "'" + i + "' as year FROM y" + i 
            #conditional for joining vcf
            if vcf == "Yes":
                zquery += " JOIN vcf on vcf.CORAL_ID = y" + i + ".tagid"

            #sliders are always added to query
            zquery += " WHERE (eco_volume < " + str(ecological_vol) + " OR eco_volume is NULL) AND (ln_eco_volume < " + str(ln_ecological_vol) + " OR ln_eco_volume is NULL) AND (length_cm < " + str(length) +  " OR length_cm is NULL) AND (width_cm < " + str(width) + " OR width_cm is NULL) AND (height_cm < " + str(height) + " OR height_cm is NULL)"


            #only uses vcf slider if vcf is yes to not create error
            if vcf == "Yes":
                zquery += " AND AF < " + allele_freq

            #filters
            #if tagid != "":
            if tagid:
                zquery += " AND tagid = %s"

            #if scaffoldid != "":
            if scaffoldid:
                zquery += " AND CHROM = %s"

            if len(location) > 0:
                zquery += " AND location in ("
                for j in location:
                    zquery +="'" + j + "', "
                zquery = zquery[:-2]
                zquery += ")"

            if len(mortality) > 0:
                zquery += " AND alive_status REGEXP '"
                for k in mortality:
                    zquery += k + "|"
                zquery = zquery[:-1]
                zquery += "'"

            #groupby filters

            if groupbys != "None":
                zquery += " GROUP BY " + groupbys


            zquery += " UNION "
        zquery = zquery[:-6]

        zquery += " ORDER BY " + order_by



        try:
            # Execute the query
            #results = execute_query(cursor, zquery)
            
            if tagid and scaffoldid:
                tslist = []
                for i in range(len(year)):
                    tslist.append(tagid)
                    tslist.append(scaffoldid)
                cursor.execute(zquery,tslist)
            else:
                if tagid:
                    cursor.execute(zquery,[tagid for i in range(len(year))])
                elif scaffoldid:
                    cursor.execute(zquery,[scaffoldid for i in range(len(year))])
                else:
                    cursor.execute(zquery)
                    
                    
            results = cursor.fetchall()
            print('')
            print(json.dumps(results, default=decimal_serializer))
            
        except pymysql.Error as e:
            error_message = f'<p style="color:red;">Error executing query: {e}</p>'

cursor.close() 
connection.close()



# Print HTML content including query results
# print(vcf_table)


###avg volume by year and (location) could select the specific location instead of having it all in once
#line graph?


"""
SELECT avg(eco_volume), year
FROM(
SELECT *, 2015 as year
From y2015 
WHERE tagid = line_tagid
UNION
SELECT *, 2016 as year
From y2016 
WHERE tagid = line_tagid
UNION
SELECT *, 2017 as year
From y2017
WHERE tagid = line_tagid
UNION
SELECT *, 2018 as year
From y2018
WHERE tagid = line_tagid
) as y
group by year
"""

"""
# If form is for graph
    line_query = ""
    line_query = 'SELECT eco_volume, year FROM (SELECT *, 2015 as year From y2015 WHERE tagid = "' + str(line_tagid) + '" UNION SELECT *, 2016 as year From y2016 WHERE tagid = "' + str(line_tagid) + '" UNION SELECT *, 2017 as year From y2017 WHERE tagid = "' + str(line_tagid) + '" UNION SELECT *, 2018 as year From y2018 WHERE tagid = "' + str(line_tagid) + '") as y group by year'


        try:
            # Execute the query
            results = execute_query(cursor, line_query)
            print('')

            
            plot_data = [list(item) for item in results]
            plot_data.insert(0,['Volume of coral','Year'])
            plot_data_tuple = tuple(plot_data)

            print(json.dumps(plot_data_tuple))
            
        except pymysql.Error as e:
            error_message = f'<p style="color:red;">Error executing query: {e}</p>'

"""
