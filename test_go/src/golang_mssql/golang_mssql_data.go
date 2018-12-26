package golang_mssql

import (
	"fmt"
	"database/sql"
//	"database/sql/driver"
	_ "github.com/denisenkom/go-mssqldb"
)

type Golang_mssql_data struct {
	//数据库链接标识
	Conn *sql.DB
	//要查询的query
	Query_sql string
	//要输入的数据
	Columns_filter []string
	//实际输入的数据
	Columns_data map[string]string
}

func (self *Golang_mssql_data) data_filter () (filter_data_arr []interface{}) {
	//数据整理，过滤
	for _, key := range self.Columns_filter {
		filter_data_arr = append(filter_data_arr, self.Columns_data[key])
	}
	fmt.Println("data_filter/filter_data_arr:", filter_data_arr)
	return
}

func (self *Golang_mssql_data) Do_select () (res []map[string]string, err error) {
	//查询sql语句
	query_str := self.Query_sql
	//sql语句对应占位符数据
	parameters := self.data_filter ()

	fmt.Println(query_str, parameters)

	tx,_ := self.Conn.Begin()
	defer tx.Commit()

	rows, err := tx.Query(query_str, parameters...)
	defer rows.Close ()
	if err != nil {
		fmt.Println ("golang_mssql/Comply->query: ", err)
		return
	}

	columns, err := rows.Columns ()
	if err != nil {
		fmt.Println ("golang_mssql/Comply->cols: ", err)
		return
	}

	//获取字段数据
	values := make ([]sql.RawBytes, len (columns))
	scanArgs := make ([]interface{}, len (values))
	for i := range values {
		scanArgs[i] = &values[i]
	}
	fmt.Println("scanArgs:",scanArgs)

	//获取值数据
	for rows.Next () {
		err = rows.Scan (scanArgs...)
		tmp_res := make(map[string]string)

		var value string
		for row, col := range values {
			if col == nil {
				value = "NULL"
			} else {
				value = string(col)
			}
			tmp_res[columns[row]] = value
		}
		res = append(res, tmp_res)
	}
	return
}

func (self *Golang_mssql_data) Do_controller () (ok bool, err error) {
	ok = true
	return
}
