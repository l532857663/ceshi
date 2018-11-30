package main

import (
	"fmt"
)

func main () {
	a := "a"
	f (a)

	fmt.Println ("out:", a)

	m := map[string]string {
		"aa": "aaa",
	}

	ff (m)

	fmt.Println ("out:", m)
}

func f (data string) {
	data += "b"
	fmt.Println ("in:", data)
}

func ff (data map[string]string) {
	data["bb"] = "bbb"
	fmt.Println ("in:", data)
}
