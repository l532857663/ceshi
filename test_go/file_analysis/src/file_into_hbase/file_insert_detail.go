package file_into_hbase

import (
	"fmt"
	"net/http"
	"strings"
)

func insert_data (cmd_str string, url string) {
	if cmd_str != "" && url != ""{
		client := &http.Client{}
		body := strings.NewReader(cmd_str)
		req, err := http.NewRequest("PUT", url, body)
		if err != nil {
			fmt.Println(err.Error)
			return
		}
		req.Header.Set("Accept", "text/xml")
		req.Header.Set("Content-Type", "text/xml")

		fmt.Println("请求: ",req)
		resp, err := client.Do(req)
		if err != nil {
			fmt.Println(err.Error)
			return
		}
		resp.Body.Close ()

		fmt.Println (resp)
	}
}
