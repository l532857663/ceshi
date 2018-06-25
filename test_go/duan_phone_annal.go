package main
import(
	"fmt"
	"net/http"
	"io/ioutil"
	// "strings"

	"encoding/xml"
)

type Hbase_resp struct {
	Row []Row_config `xml:"Row"`
}

type Row_config struct {
	XMLName xml.Name `xml:"Row"`
	Key string `xml:"key,attr"`

	Cell []Cell_config `xml:"Cell"`
}

type Cell_config struct {
	XMLName xml.Name `xml:"Cell"`
	Column string `xml:"column,attr"`
	Timestamp string `xml:"timestamp,attr"`
	Value string `xml:",innerxml"`
}

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

		data := new (Hbase_resp)
		xml.Unmarshal (body, data)
		fmt.Println (data)
}

func main(){
		url := "http://192.168.11.133:9900/dxy/123456"
		httpGet(url)
}
//curl -vi -X PUT -H "Accept: text/json" -H "Content-Type: text/json" -d '{"Row":[{"key":"cm93MQ==", "Cell": [{"column":"ZjE=", "$":"MTIzNDU2"}]}]}' "http://192.168.11.133:9900/t1/fakerow"
//		curl -vi -X PUT -H "Accept: text/xml" -H "Content-Type: text/xml" -d '<?xml version="1.0" encoding="UTF-8"?><TableSchema name="users"><ColumnSchema name="cf" /></TableSchema>' 'http://192.168.11.133:9900/t1/schema'
