from db import mysql_conn
from datetime import datetime
import sys
import json

if len(sys.argv) > 1:
    if sys.argv[1] == 'all':
        data_query = '%'
    else:
        data_query = sys.argv[1]

else:
    data_query = datetime.now().strftime('%Y-%m-%d')

my_conn = mysql_conn()
fields = 'calldate, src, dst, channel, dstchannel, lastapp, billsec, disposition, accountcode, userfield'
query = "SELECT {} FROM cdr WHERE calldate like '{}%' and accountcode != ''".format(fields, data_query)
result = my_conn.query(query)
result_list = []

for (calldate, src, dst, channel, dstchannel, lastapp, billsec, disposition, accountcode, userfield) in result:
    print(calldate, src, dst, channel, dstchannel, lastapp, billsec, disposition, accountcode, userfield)
    result_list.append(
        {
            'calldate' : calldate.strftime('%Y-%m-%d %H:%M:%S'),
            'src' : src,
            'dst' : dst, 
            'channel' : channel,
            'dstchannel' : dstchannel,
            'lastapp' : lastapp,
            'billsec' : billsec,
            'disposition' : disposition,
            'accountcode' : accountcode,
            'userfield' : userfield
        }
    )

#Gravando dados no JSON
with open('json/cdr_{}.json'.format(data_query), 'w') as arquivo:
    arquivo.write(
        json.dumps(result_list)
    )
