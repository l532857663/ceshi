package file_into_hbase

import (
	"fmt"
	"net/http"
	"strings"
)

func create_table(name string) {
	//判断表是否存在
	resp, err := http.Get (Global_data.Host + "/" + name + "/schema")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("bank_data:",resp)

	if resp.StatusCode == 200 {
	}else if resp.StatusCode == 404 {
		//建表
		data := "<?xml version=\"1.0\" encoding=\"UTF-8\"?><TableSchema name=\"bank_transaction_flow:" + name + "\"><ColumnSchema name=\"info\" /></TableSchema>"
		url := Global_data.Host + "/" + name + "/schema"

		client := &http.Client{}
		body := strings.NewReader(data)
		req, err := http.NewRequest("PUT", url, body)
		if err != nil {
			fmt.Println(err.Error)
			return
		}
		req.Header.Set("Accept", "text/xml")
		req.Header.Set("Content-Type", "text/xml")

		fmt.Println("create_table请求: ",req)
		fmt.Println("data: ",data)
		resp, err = client.Do(req)
		if err != nil {
			panic (err)
		}
		resp.Body.Close ()
	} else {
		panic ("resp StatusCode error")
	}
}
