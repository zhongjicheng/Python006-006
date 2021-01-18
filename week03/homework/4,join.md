题目：以下两张基于 id 列，分别使用 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果是什么?

Table1

id name

1 table1_table2

2 table1

Table2

id name

1 table1_table2

3 table2

# INNER JOIN
```
mysql> select table1.id, table1.name, table2.id, table2.name
    -> from table1
    -> inner join table2
    -> on table1.id = table2.id;
+----+---------------+----+---------------+
| id | name          | id | name          |
+----+---------------+----+---------------+
|  1 | table1_table2 |  1 | table1_table2 |
+----+---------------+----+---------------+
1 row in set (0.00 sec)
```

# LEFT JOIN
```
mysql> select table1.id, table1.name, table2.id, table2.name
    -> from table1
    -> left join table2
    -> on table1.id = table2.id;
+----+---------------+------+---------------+
| id | name          | id   | name          |
+----+---------------+------+---------------+
|  1 | table1_table2 |    1 | table1_table2 |
|  2 | table1        | NULL | NULL          |
+----+---------------+------+---------------+
2 rows in set (0.00 sec)

```

# RIGHT JOIN
```
mysql> select table1.id, table1.name, table2.id, table2.name
    -> from table1
    -> right join table2
    -> on table1.id = table2.id;
+------+---------------+----+---------------+
| id   | name          | id | name          |
+------+---------------+----+---------------+
|    1 | table1_table2 |  1 | table1_table2 |
| NULL | NULL          |  3 | table1        |
+------+---------------+----+---------------+
2 rows in set (0.00 sec)
```