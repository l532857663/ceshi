package test_files

import (
	"fmt"
	"hbase_search_database"
)

func (self *hbase_search_database.Hbase_rest) Put_api_func (table_name string, put_data map[string]map[string]string) {
	res := Hrest.Put_data_api(table_name, put_data)
	if !res {
		fmt.Println("put api insert error")
	}

	fmt.Println("put database OK")
}
