package main

import (
	"fmt"
	"os"
	"help"
	"wifilz_server_config"
	"wifilz_server"
	_ "static_web_server"
	_ "wifilz_web_server"
)

func main () {
	defer func () {
		if err := recover (); err != nil {
			fmt.Println (err)
			help.Help ()
		}
	} ()

	if (len (os.Args) != 2) {
		panic ("args len not 2")
	}

	config := new (wifilz_server_config.Wifilz_server_config)
	config.Parse (os.Args[1])
	// fmt.Println (config)

	for num, server_config := range config.Server {
		for mode_num, server_mode := range wifilz_server.Wifilz_server {
			if server_mode.Check (server_config.Mode) == true {
				if (num + 1) == len (config.Server) {
					// fmt.Println (num + 1)
					// fmt.Println (config.Server)
					server_mode.Start (server_config)
				} else {
					// fmt.Println (num + 1)
					// fmt.Println (config.Server)
					go server_mode.Start (server_config)
					break
				}
			}
			if (mode_num + 1) == len (wifilz_server.Wifilz_server) == true {
				panic ("server mode not found: " + server_config.Mode)
			}
		}
	}
	panic ("error")
}
