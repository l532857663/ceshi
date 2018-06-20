package main
import(
	"fmt"
	"net/http"
	"io/ioutil"
)

//发起GET请求
func httpDo(url string){
		client := &http.Client{}
		req, err := http.NewRequest("DELETE", url, nil)
		if err != nil {
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

func main(){
		url := "http://192.168.11.133:9900/t1/schema"
		//	httpGet(url)
		httpDo(url)
}
