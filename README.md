# sqlite_searcher
To search data with RegEx from sqlite3 DB Table.

# Usage
```
# ./check_dbfield.py -i example.db -r "&#[0-9]{1,5};"
>> 1 Tables found :
> TestTable
Keys[] Col[Head4] Data[&#11; ?]
Keys[] Col[Head4] Data[&#33321; ttttt]
```
