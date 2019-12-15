# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import xlwt
from datetime import datetime
import chardet

style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

wb = xlwt.Workbook()
ws = wb.add_sheet('A Test Sheet')

ws.write(0, 0, 'id')
ws.write(0, 1, 'name')

fileRead = open("./log/20191214/201912141252-feixi.log" , 'r')
# fencoding = chardet.detect(fileRead.read())
# print fencoding

i = 1
for line in fileRead.readlines():
        ws.write(i, 0, i)
        # line.encode('utf-8')
        # ws.write(i, 1, line.encode('utf-8'))
        i = i + 1


fileRead.close()

# ws.write(0, 0, 1234.56, style0)
# ws.write(1, 0, datetime.now(), style1)
# ws.write(2, 0, 1)
# ws.write(2, 1, 1)
# ws.write(2, 2, xlwt.Formula("A3+B3"))

wb.save('xx.xls')