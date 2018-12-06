package main

import (
	"fmt"
	"time"
	"net/http"
	"io/ioutil"
)

func conncet_go(addr, port, method string) {
	fmt.Println("content go start")
	resp, err := http.Get("http://" + addr + ":" + port + method)
	if err != nil {
		fmt.Println("conncet_go get error:", err)
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("conncet_go resp error:", err)
		return
	}
	fmt.Println("the resp body:", string(body))
}

func main() {
	fmt.Println("Start")
	var set_time time.Duration
	set_time = 5
	addr := "192.168.11.133"
	port := "8848"
	method := "/search_task"
	for {
		conncet_go(addr, port, method)
		time.Sleep(set_time * 1000000000)
	}
}
