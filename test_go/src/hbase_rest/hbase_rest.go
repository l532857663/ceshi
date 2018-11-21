package hbase_rest

import (
	"fmt"
	"net/http"
	"encoding/xml"
	"io/ioutil"
	"strings"
	"sync"
)

type Hbase_rest struct {
	Addr string
	Client *http.Client

	Mutex *sync.Mutex
	Flag *int
}

//查询结果框架
type Hbase_resp_row struct {
	Row []Row_config `xml:"Row"`
	Table []Table_config `xml:"table"`
}

type Table_config struct {
	XMLName xml.Name `xml:"table"`
	Name string `xml:"name,attr"`
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
	Timestamp_int64 int64
}

//scanner XML 
type Scanner_config struct {
	XMLName xml.Name `xml:"Scanner"`
	Batch string `xml:"batch,attr"`
	StartRow string `xml:"startRow,attr"`
	EndRow string `xml:"endRow,attr"`

	Filter string `xml:"filter"`
}

//filter模型设置
type Filter_json struct {
	Type string `json:"type,omitempty"`
	Value string `json:"value,omitempty"`
	Family string `json:"family,omitempty"`
	Op string `json:"op,omitempty"`
	Comparator *Comparator_json `json:"comparator,omitempty"`
}

type Comparator_json struct {
	Type string `json:"type,omitempty"`
	Value string `json:"value,omitempty"`
}

func New_hbase_rest (addr string, mutex *sync.Mutex, flag *int) (res *Hbase_rest) {
	res = new (Hbase_rest)

	res.Addr = addr
	res.Client = new (http.Client)
	res.Mutex = mutex
	res.Flag = flag

	return
}

func (self *Hbase_rest) Get_base (method string, url string, body string) (res Hbase_resp_row, resp *http.Response, ok bool) {
	req_body := strings.NewReader (body)
	req, err := http.NewRequest (method, url, req_body)
	if err != nil {
		ok = false
		return
	}
	req.Header.Set ("Accept", "text/xml")
	req.Header.Set ("Content-Type", "text/xml")

	resp, err = self.Client.Do (req)

	defer resp.Body.Close ()

	if resp.StatusCode != 200 {
		if resp.StatusCode != 201 {
				if resp.StatusCode != 204 {
				fmt.Println ("StatusCode error: ", resp.StatusCode)
				ok = false
				return
			}
		}
	}

	data_str, err := ioutil.ReadAll (resp.Body)
	if err != nil {
		fmt.Println ("read error")
		ok = false
		return
	}

	fmt.Println ("all body: ", string (data_str))

	if len (data_str) != 0 {
		err = xml.Unmarshal (data_str, &res)
		if err != nil {
			ok = false
			return
		}
	}

	ok = true
	return
}
