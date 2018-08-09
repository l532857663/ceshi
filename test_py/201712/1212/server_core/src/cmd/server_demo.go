package main

import (
	"fmt"
	"net/http"
	// "io"
	// "os"
)

type WebTest map[string]func (*http.Request)

func (self WebTest) ServeHTTP (w http.ResponseWriter, req *http.Request) {
}

func main () {
	tester := new (WebTest)
	err := http.ListenAndServe (":8888", tester)
	if err != nil {
		fmt.Println ("ListenAndServe: ", err)
	}
}
