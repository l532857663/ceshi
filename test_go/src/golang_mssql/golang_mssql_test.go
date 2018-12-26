package golang_mssql

import (
	"testing"
	"fmt"
)

func Test_golang_mssql_data (t *testing.T) {
	My_db := New_golang_mssql("192.168.11.134", "sa", "sa123", "ku2sdsd", 1433)

	My_db_data := new (Golang_mssql_data)
	My_db_data.Conn = My_db.Conn
	My_db_data.Query_sql = "select top 10 * from ?"

	tmp_filters := []string {
		"table_name",
	}
	tmp_datas := map[string]string {
		"table_name" : "admin",
	}

	My_db_data.Columns_filter = tmp_filters
	My_db_data.Columns_data = tmp_datas

	res, err := My_db_data.Do_select ()
	if err != nil {
		fmt.Println("error is:", err)
		return
	}

	fmt.Println("res:", res)
}
