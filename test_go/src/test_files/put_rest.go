package test_files

import (
	"fmt"

	"strings"
	"hbase_search_database"

	"encoding/json"
)

func Put_rest_func(Hrest *hbase_search_database.Hbase_rest) {
	var res bool
	res = Hrest.Set_url_put ()
	if !res {
		fmt.Println("put url set error!")
		return
	}
	fmt.Println("put url:", Hrest.Url)

	Hrest.Set_method_put()
	fmt.Println("put method:", Hrest.Method)

	put_data_json := new (hbase_search_database.Hbase_insert_json)
	err := json.Unmarshal([]byte(Put_data), &put_data_json)
	if err != nil {
		fmt.Println("json Marshal error:", err)
		return
	}
	res = Hrest.Set_data_put(put_data_json)
	if !res {
		fmt.Println("put data set error!")
		return
	}

	res_data := new (hbase_search_database.Hbase_resp_row)
	res_str := Hrest.Start(res_data)
	if strings.Compare(res_str, "error") == 0 {
		fmt.Println("put database error")
		return
	}
	fmt.Println(res_str)

	fmt.Println("put database OK")
}
