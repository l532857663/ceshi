package wifilz_web_server

import (
	"fmt"
	"net/http"
	"strconv"
	"strings"

	"wifilz_server_config"
	"wifilz_server"
	"wifilz_web_server/web_database"
)

type wifilz_web_server struct {
	config wifilz_server_config.Server_config
}

var _wifilz_web_server wifilz_web_server

func init () {
	wifilz_server.Wifilz_server = append (wifilz_server.Wifilz_server, &_wifilz_web_server)
}

func (self wifilz_web_server) Check (server_name string) (ok bool) {
	if strings.Compare (server_name, "wifilz_web_server") == 0 {
		ok = true
	} else {
		ok = false
		return
	}

	return
}

func (self *wifilz_web_server) Start (config wifilz_server_config.Server_config) {
	self.config = config

	err := http.ListenAndServe (":" + strconv.Itoa (self.config.Port), &_wifilz_web_server)
	if err != nil {
		panic ("wifilz_web_server ListenAndServe error")
	}
}

func (self *wifilz_web_server) ServeHTTP (w http.ResponseWriter, req *http.Request) {
	web_func , ok := web_database.Web_database[req.URL.Path]
	if (!ok) {
		w.WriteHeader (http.StatusNotFound)
		fmt.Fprintf (w, "找不到文件：%s", req.URL.Path)
		return
	}

	web_func (w, req)
}
