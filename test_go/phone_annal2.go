package main
import(
	"fmt"
	"net/http"
	"io/ioutil"
	"strings"

)


//发起GET请求

func httpGet(url []string){

	for _, v := range url {
		client := &http.Client{}
		req, err := http.NewRequest("GET", v, nil)
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
		fmt.Println("sss: ",resp.Location())
		respBody, err := ioutil.ReadAll(resp.Body)
        if err != nil {
                fmt.Println(err.Error)
                return
        }

        fmt.Println(string(respBody))
}

func main(){

		// 查询语句
		url2 := "http://192.168.11.133:9900/call_phone_number_base:15093191339/scanner"
//		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner batch="100"><filter> { "type": "PrefixFilter", "value": "1528436400" } </filter></Scanner>`
		body := `<?xml version="1.0" encoding="UTF-8"?><Scanner batch="100"><filter> { "type": "PrefixFilter", "value": "MTUyODQzNjQwMA==" } </filter></Scanner>`
		httpDO("PUT", url2, body)
}
//curl -vi -X PUT -H "Accept: text/json" -H "Content-Type: text/json" -d '{"Row":[{"key":"cm93MQ==", "Cell": [{"column":"ZjE=", "$":"MTIzNDU2"}]}]}' "http://192.168.11.133:9900/t1/fakerow"
//		curl -vi -X PUT -H "Accept: text/xml" -H "Content-Type: text/xml" -d '<?xml version="1.0" encoding="UTF-8"?><TableSchema name="users"><ColumnSchema name="cf" /></TableSchema>' 'http://192.168.11.133:9900/t1/schema'
