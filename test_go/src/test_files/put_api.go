package test_files

import (
	"fmt"
	"hbase_search_database"
)

func Put_api_func(Hrest *hbase_search_database.Hbase_rest) {
	res := Hrest.Put_data_api(Put_data)
	if !res {
		fmt.Println("put api insert error")
	}

	fmt.Println("put database OK")
}
