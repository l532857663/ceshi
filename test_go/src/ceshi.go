package main

import (
	"fmt"
	"time"
)

func main () {
	fmt.Println("START")
//	qiepian()
//	dingshi()
	byte2string()
	fmt.Println("END")
}

func say_hi () {
	fmt.Println("Hello")
	fmt.Println("time:", time.Now())
}

/*
切片追加到切片
*/
func qiepian() {
	fmt.Println("qiepian")
	var aa []string
	bb := make(map[string][]string)
	bb["b1"] = []string{
		"asdasd",
		"asdadw",
	}
	bb["c1"] = []string{
		"asdasd1",
		"asdadw1",
	}
	fmt.Println("aa:", aa)
	for _, obj := range bb {
		fmt.Println(obj)
		aa = append(aa, obj...)
	}
	fmt.Println("aa:", aa)
}

/*
定时执行函数
*/
func dingshi() {
	fmt.Println("dingshi")
	timer := time.AfterFunc(time.Duration(5)*time.Second, say_hi)
	fmt.Println("timer:", timer)
	fmt.Println("start time:", time.Now())
	for {
		ok := timer.Reset(time.Duration(5)*time.Second)
		if !ok {
			break
		}
		fmt.Println("sleep")
		time.Sleep(time.Duration(20)*time.Second)
	}
	fmt.Println("time1:", time.Now())
}

/*
byte跟string转换
*/
func byte2string() {
	fmt.Println("byte2string")
}
