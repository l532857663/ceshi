package main
import(
	"fmt"
	"net/http"
	"io/ioutil"

	"strings"
)


//发起GET请求
func httpGet(url string){

		client := &http.Client{}
		req, err := http.NewRequest("GET", url, nil)
		if err != nil {
				fmt.Println(err.Error)
				return
		}
		req.Header.Set("Accept", "text/xml")

//		fmt.Println("请求: ",req)
		resp, err := client.Do(req)

		defer resp.Body.Close()
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
				fmt.Println(err.Error)
				return
		}

		fmt.Println(string(body))
}

func httpDO(method string, url string, strAll string){
		client := &http.Client{}
		body := strings.NewReader(strAll)
		req, err := http.NewRequest(method, url, body)
		if err != nil {
                fmt.Println(err.Error)
                return
        }
        req.Header.Set("Accept", "text/xml")
        req.Header.Set("Content-Type", "text/xml")

		fmt.Println("请求: ",req)
        resp, err := client.Do(req)

        defer resp.Body.Close()
		fmt.Println("回应: ",resp)
		respBody, err := ioutil.ReadAll(resp.Body)
        if err != nil {
                fmt.Println(err.Error)
                return
        }

        fmt.Println(string(respBody))

		scanner_id := resp.Header["Location"][0]
		fmt.Println(scanner_id)
		httpGet(scanner_id)
}

func main(){
		/*
		url := []string {"http://192.168.11.133:9900/dxy/123456/timestamp:123123", "http://192.168.11.133:9900/dxy/123456/timestamp:124124"}
		httpGet(url)
		url1 := "http://192.168.11.133:9900/t1/fakerow"
		body := `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><CellSet><Row key="cm93MQ=="><Cell column="ZjE6bmFtZQ==">MTIzNDU2</Cell></Row></CellSet>`
		httpDO("PUT", url1, body)
*/
		//删表
//		url2 := "http://192.168.11.133:9900/t1/schema"
//		httpDO("DELETE", url2, "")
		//建表
//		body := `<?xml version="1.0" encoding="UTF-8"?><TableSchema name="t1"><ColumnSchema name="f1" /></TableSchema>`
//		httpDO("PUT", url2, body)
//		url2 := "http://192.168.11.133:9900/call_phone_number_base:15093191339/scanner"
		url2 := "http://192.168.11.133:9900/call_phone_number_base:15093191339/scanner"
/*		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner startRow="MTUyODI0MzIwMA==" endRow="MTUyODQxNjAwMA=="><filter>{
			"type": "ValueFilter",
			"op": "EQUAL",
			"family": "aW5mbw==",
			"qualifier": "b3RoZXJfbnVtYmVy",
			"comparator": {
				"type": "BinaryComparator",
				"value": "MTUwMTE1NjIyOTM="
			}
		}</filter></Scanner>`
*/		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner startRow="MTUyODI0MzIwMA==" endRow="MTUyODI0MzIwMA==">
			<filter>{
				"type": "ValueFilter",
				"op": "EQUAL",
				"family": "aW5mbw==",
				"qualifier": "b3RoZXJfbnVtYmVy",
				"comparator": {
					"type": "BinaryComparator",
					"value": "MTg1MTU4OTk4ODM="
				}
			}</filter></Scanner>`
//		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner startRow="MTUyODMyOTYwMA==" endRow="MTUyODQxNjAwMA=="></Scanner>`
		// body := `<?xml version="1.0" encoding="UTF-8"?><Scanner><filter> { "type": "PrefixFilter", "value": "MTUyODQzNjQwMA==" } </filter></Scanner>`
//		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner><filter> { "type": "ValueFilter","op":"=", "value": "NjM2ODgxNjE=" } </filter></Scanner>`
//		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner><filter> { "type": "ValueFilter","op":"=", "value": "YmluYXJ5OjYzNjg4MTYx" } </filter></Scanner>`
//		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner><filter> { "type": "ValueFilter","op":"=", "value": "binary:63688161" } </filter></Scanner>`
//		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner><filter> { "type": "ValueFilter", "value": "=, 'binary:63688161'" } </filter></Scanner>`
		// body := `<?xml version="1.0" encoding="UTF-8"?><Scanner><filter> { "type": "ValueFilter", "value": "=, binary:63688161" } </filter></Scanner>`
		httpDO("PUT", url2, body)

}
//curl -vi -X PUT -H "Accept: text/json" -H "Content-Type: text/json" -d '{"Row":[{"key":"cm93MQ==", "Cell": [{"column":"ZjE=", "$":"MTIzNDU2"}]}]}' "http://192.168.11.133:9900/t1/fakerow"
//		curl -vi -X PUT -H "Accept: text/xml" -H "Content-Type: text/xml" -d '<?xml version="1.0" encoding="UTF-8"?><TableSchema name="users"><ColumnSchema name="cf" /></TableSchema>' 'http://192.168.11.133:9900/t1/schema'
