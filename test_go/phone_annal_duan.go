package main
import(
	"fmt"
	"net/http"
	"io/ioutil"
	"strings"

)

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

        fmt.Println(resp.Header["Location"][0])

		client = &http.Client{}
		req, err = http.NewRequest("GET", resp.Header["Location"][0], nil)
		if err != nil {
				fmt.Println(err.Error)
				return
		}
		req.Header.Set("Accept", "text/xml")

		fmt.Println("请求: ",req)
		resp, err = client.Do(req)

		defer resp.Body.Close()
		respBody, err = ioutil.ReadAll(resp.Body)
		if err != nil {
				fmt.Println(err.Error)
				return
		}
        fmt.Println(string(respBody))
}

func main(){
		// 查询语句
		url2 := "http://192.168.11.133:9900/call_phone_number_base:15093191339/scanner"
		// body := `<?xml version="1.0" encoding="UTF-8"?><Scanner batch="100"><filter>{"type":"PrefixFilter","value":"MTUyODQzODgwMA=="}</filter></Scanner>`
		// body := `<?xml version="1.0" encoding="UTF-8"?><Scanner batch="100"><filter>{"type":"ValueFilter","latestVersion": true,"op":"EQUAL","value":"YmluYXJ5OjE1Mjg0MzEwMzM="}</filter></Scanner>`
		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner batch="100"><filter>{
			"type": "SingleColumnValueFilter", 
			"op": "EQUAL", 
			"ifMissing": true, 
			"family": "aW5mbw==", 
			"qualifier": "dGFsa190aW1l", 
			"comparator": {
				"type": "BinaryComparator", 
				"value": "MTE="
			}
		}</filter></Scanner>`

		/*
		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner batch="100"><filter>{
			"type": "PrefixFilter", 
			"value":"MTUyODQzODgwMA==" 
		}</filter></Scanner>`
		*/

		fmt.Println ("body:", body)
		// body := `<?xml version="1.0" encoding="UTF-8"?><Scanner batch="100"><filter>"(TimestampsFilter(1529950163450,1529950163470))"</filter></Scanner>`
		httpDO("PUT", url2, body)
}
//curl -vi -X PUT -H "Accept: text/json" -H "Content-Type: text/json" -d '{"Row":[{"key":"cm93MQ==", "Cell": [{"column":"ZjE=", "$":"MTIzNDU2"}]}]}' "http://192.168.11.133:9900/t1/fakerow"
//		curl -vi -X PUT -H "Accept: text/xml" -H "Content-Type: text/xml" -d '<?xml version="1.0" encoding="UTF-8"?><TableSchema name="users"><ColumnSchema name="cf" /></TableSchema>' 'http://192.168.11.133:9900/t1/schema'
