/**
 * 文件功能：
 */

/**
 * 包功能：
 */
package wifilz_server_config

import (
	// "fmt"
	"encoding/xml"
	"io/ioutil"
)

type Wifilz_server_config struct {
	Server []Server_config `xml:"server"`
}

type Server_config struct {
	Name string `xml:"name"`
	Mode string `xml:"mode"`
	Port int `xml:"port"`
	Max_connect int `xml:"max_connect"`
	Timeout int `xml:"timeout"`
	Mysql_parm Mysql_parm_config `xml:"mysql_parm"`
	Res_path string `xml:"res_path"`
}

type Mysql_parm_config struct {
	IpAddr string `xml:"ip"`
	Username string `xml:"username"`
	Password string `xml:"password"`
	DbName string `xml:"db_name"`
}

func (self *Wifilz_server_config) Parse (config_path string){
	content, err := ioutil.ReadFile (config_path)
	if err != nil {
		panic ("can't found config file")
	}

	err = xml.Unmarshal (content, &self)
	if err != nil {
		panic ("parse xml fail")
	}
	// fmt.Println (self)
}
