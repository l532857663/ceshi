/**
* 文件功能：直接通过rest访问操作hbase数据库
*/
package hbase_search_database

import (
	"fmt"
	"net/http"
	"encoding/xml"
	"io/ioutil"
	"strings"
	"sync"

//	"reflect"
)

type Hbase_rest struct {
	Client *http.Client

	Addr string
	Body string
	Url string
	Method string

	Url_config interface{}

	Mutex *sync.Mutex
	Flag *int
}

func New_hbase_rest (addr string, mutex *sync.Mutex, flag *int) (res *Hbase_rest) {
	res = new (Hbase_rest)

	res.Addr = addr
	res.Client = new (http.Client)
	res.Mutex = mutex
	res.Flag = flag

	return
}

func (self *Hbase_rest) Start (res interface{}) (err_str string) {
//	fmt.Println("ceshi---------------")
	req_body := strings.NewReader (self.Body)
	req, err := http.NewRequest (self.Method, self.Url, req_body)
	if err != nil {
		err_str = "error"
		return
	}
	req.Header.Set ("Accept", "text/xml")
	req.Header.Set ("Content-Type", "text/xml")
	fmt.Println("req:", req)

	resp, err := self.Client.Do (req)

	defer resp.Body.Close ()


	// 404 NOT FOUND 查询条件无结果，返回404
	if resp.StatusCode == 404 {
		fmt.Println ("data_str not found")
		err_str = "empty"
		return
	}

	// 200 OK
	if resp.StatusCode != 200 {
	// 201 CREATED
		if resp.StatusCode != 201 {
	// 204 NO CONTENT
			if resp.StatusCode != 204 {
				fmt.Println ("StatusCode error: ", resp.StatusCode)
				err_str = "error"
				return
			}
		}
	}

	data_str, err := ioutil.ReadAll (resp.Body)
	if err != nil {
		fmt.Println ("read error")
		err_str = "error"
		return
	}

	fmt.Println ("hbase data_res_str: ", string (data_str))
	//scan扫描，第一次返回结果集
	if strings.Compare(res.(string), "Scanner") == 0 {
		fmt.Println("the type is Scanner")
		err_str = resp.Header["Location"][0]
		return
	}

	//插入数据成功返回空
	if strings.Compare (string (data_str), "") == 0 {
		fmt.Println ("data_str not found")
		err_str = "empty"
		return
	}

	//查询数据结果转义返回
	err = xml.Unmarshal (data_str, res)
	if err != nil {
		fmt.Println("data_res xml Unmarshal error", err)
		err_str = "error"
		return
	}

	err_str = "success"
	return
}
