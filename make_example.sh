#!/bin/bash

echo "PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE TestTable ( Head1 INT, Head2 TEXT, Head3 TEXT, Head4 TEXT, Head5 TEXT );
INSERT INTO TestTable VALUES(1,'John','This is Test Text1','Where is &#11; ?','Test3');
INSERT INTO TestTable VALUES(2,'Sam','This is Test Text1','&#33321; ttttt','Test4');
COMMIT;" |sqlite3 example.db

