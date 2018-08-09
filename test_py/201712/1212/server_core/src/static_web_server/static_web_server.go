package static_web_server

import (
	// "fmt"
	"net/http"
	"strconv"
	"strings"

	"wifilz_server_config"
	"wifilz_server"
	"static_web_server/send_static_res"
)

type static_web_server struct {
	config wifilz_server_config.Server_config
}

var _static_web_server static_web_server

func init () {
	wifilz_server.Wifilz_server = append (wifilz_server.Wifilz_server, &_static_web_server)
}

func (self static_web_server) Check (server_name string) (ok bool) {
	// fmt.Println (server_name)
	if strings.Compare (server_name, "static_web_server") == 0 {
		ok = true
	} else {
		ok = false
		return
	}

	return
}

func (self *static_web_server) Start (config wifilz_server_config.Server_config) {
	self.config = config

	err := http.ListenAndServe (":" + strconv.Itoa (self.config.Port), &_static_web_server)
	if err != nil {
		panic ("static_web_server ListenAndServe error")
	}
}

func (self *static_web_server) ServeHTTP (w http.ResponseWriter, req *http.Request) {
	// fmt.Println (self.config)
	send_static_res.Send (self.config.Res_path, w, req)
}
