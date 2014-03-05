# readexcel
#import MySQLdb
import xlrd
import os

#settings
filename=r'\ProductToBeImported\2014-01-29\00264 .xlsx'
#settings end

print('Read Excel Begin ')
workbook = xlrd.open_workbook(os.path.dirname(os.path.realpath(__file__))+filename)
worksheet = workbook.sheet_by_index(0)
num_rows = worksheet.nrows - 1
num_cells = worksheet.ncols - 1
curr_row = 0
l=[]
while curr_row < num_rows:
    curr_row += 1
    row = worksheet.row(curr_row)
    #print ('Row:', curr_row)
    curr_cell = -1
    r=()
    singleL=[]
    while curr_cell < num_cells:
        curr_cell += 1
        if curr_cell not in (2,3,4,5,8,9):
            continue
        #index in list 26,27,28,29,30
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        cell_type = worksheet.cell_type(curr_row, curr_cell)
        cell_value = worksheet.cell_value(curr_row, curr_cell)
        #print ('    ', cell_type, ':', cell_value)
        singleL.append(cell_value)
    r=tuple(singleL)
    l.append(r)
print('Read Excel End.TotalLines:'+str(len(l)))
ntscodes=[t[-1]  for t in  l]

conn=mysql.connector.connect(host='192.168.1.44',user='root',passwd='exDr97K4NDct37dw',db='magento17')
cursor=conn.cursor()
query='''
SELECT DISTINCT p.ntscode AS sku
-- ,pa.NameForWeb  -- 2
-- ,CONCAT(pa.Specification,'<br/>', pa.ProductDescription) -- specification
,REPLACE(REPLACE(p.PriceOfFactory,'￥',''),',','')  -- 4
,p.PriceOfFactory
,s.englishname
,p.modelnumber
 ,CONCAT('42,',m2.cateid_website,',',m1.cateid_website)
, l.ProductDescription
, ''         -- description
,'' -- seo
,''
,''
,CONCAT('/', p.ntscode,'.jpg')
,CONCAT('/', p.ntscode,'.jpg')
,CONCAT('/',p.ntscode,'.jpg')
,1
,10000
,1
,0
,'Catalog,Search'
,CONCAT('/',p.ntscode,'.jpg')
,255
,'default'
,'asia'
,'simple'
,'default'
,0
 -- ,CONCAT( pa.Parameter,';',pa.Material)  -- 3
FROM   ntsbase2.product p 
   INNER JOIN  ntsbase2.productlanguage l
    ON p.Id=l.Product_id  AND l.language='en'
   RIGHT JOIN CategoryMap m1
        ON p.categorycode=m1.cateid_ntsbase
 RIGHT JOIN CategoryMap m2
        ON LEFT(p.categorycode,2)=m2.cateid_ntsbase
    
   INNER JOIN ntsbase2.supplier s
      ON p.suppliercode=s.code
      
    INNER JOIN ntsbase2.productimage i
        ON p.id=i.product_id
    where p.ntscode in ({0})
'''
#query='select * from ntsbase2.product where ntscode in ("09.002.0026400001")'
query=query.format(', '.join('"'+item+'"' for item in ntscodes))
cursor.execute(query)
result=cursor.fetchall()
print('Query Result length:'+str(len(result)))
print('Prepare data to be insert')

rr=zip(l,result)
newlist=[]
for row in l:
    newrow=[]
    for row2 in result:
        if row2[0]==row[5]:
           newrow=row2+row
           
    newlist.append(newrow)
print('Prepare complete.total lines:'+str(len(newlist)))
#print(newlist)
insertQuery='''INSERT INTO  magento17.data_import 
        (sku, -- 1
NAME,            -- 2
    specification,-- 3 
    price,  -- 4
    special_price, -- 5 
    manufacturer, -- 6
    model,   -- 7 
    category_ids, 
    short_description, 
     description,-- 10 
    meta_title,  
    meta_keyword, 
    meta_description, 
    image, 
    small_image, -- 15
    thumbnail, 
    is_in_stock, 
    qty, 
    STATUS, 
    tax_class_id, -- 20
    visibility, 
    gallery, 
    sort_order, 
    store, 
    websites,  -- 25
    TYPE, 
    attribute_set, 
    weight,
    parameter -- 29
    )
    values(
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s,%s,
    %s,%s,%s,%s)
'''
print('Data insert begin, please wait..')
cursor.executemany(insertQuery,[(item[0],
                                 item[28],
                                 item[29]+'<br/>'+item[30],
                                 item[1],
                                 item[2],

                                 item[3],
                                 item[4],
                                 item[5],
                                 item[6],
                                 item[7],

                                 item[8],
                                 item[9],
                                 item[10],
                                 item[11],
                                 item[12],

                                 item[13],
                                 item[14],
                                 item[15],
                                 item[16],
                                 item[17],

                                 item[18],
                                 item[19],
                                 item[20],
                                 item[21],
                                 item[22],

                                 item[23],
                                 item[24],
                                 item[25],
                                 item[26]+';'+item[27]
                                
                                 ) for item in newlist])
conn.commit()
print('Data insert complete. Task complete. total insert :'+str(len(newlist)))
cursor.close()
conn.close()
print('OK')



