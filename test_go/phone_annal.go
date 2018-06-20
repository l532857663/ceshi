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

/**
 *发起PUT请求，添加数据
 */
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
}

func main(){
		url := "http://192.168.11.133:9900/dxy/schema"
		httpGet(url)
		url1 := "http://192.168.11.133:9900/t1/fakerow"
		body := `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><CellSet><Row key="cm93MQ=="><Cell column="ZjE=">MTIzNDU2</Cell></Row></CellSet>`
		httpDO("PUT", url1, body)

		//删表
//		url2 := "http://192.168.11.133:9900/t1/schema"
//		httpDO("DELETE", url2, "")
		//建表
//		body := `<?xml version="1.0" encoding="UTF-8"?><TableSchema name="t1"><ColumnSchema name="f1" /></TableSchema>`
//		httpDO("PUT", url2, body)
}
//curl -vi -X PUT -H "Accept: text/json" -H "Content-Type: text/json" -d '{"Row":[{"key":"cm93MQ==", "Cell": [{"column":"ZjE=", "$":"MTIzNDU2"}]}]}' "http://192.168.11.133:9900/t1/fakerow"
//		curl -vi -X PUT -H "Accept: text/xml" -H "Content-Type: text/xml" -d '<?xml version="1.0" encoding="UTF-8"?><TableSchema name="users"><ColumnSchema name="cf" /></TableSchema>' 'http://192.168.11.133:9900/t1/schema'
