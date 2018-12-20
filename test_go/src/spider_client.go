package main

import (
	"fmt"
	"time"
	"net/http"
	"io/ioutil"

	"os/exec"
	"bufio"
	"io"
	"os"
)

var Addr string
var Port string
var Spider_path string

//解析返回结果
func run_py(task_data string) (ok bool) {
//	fmt.Println("the task data:", task_data)
	var parameter []string
	parameter = append(parameter, task_data)
	parameter = append(parameter, "qazxsw31154@gmail.com")
	parameter = append(parameter, "1q2w#E$R")
	parameter = append(parameter, "http://192.168.201.110:4444/receive")
//	fmt.Println("parameter:", parameter)
	cmd := exec.Command(Spider_path + "/spider_twitter.py", parameter...)
	fmt.Println("cmd str:", cmd)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("cmd python StdoutPipe error",err)
		ok = false
		return
	}
	cmd.Start()
	reader := bufio.NewReader(stdout)
	for {
		line, err2 := reader.ReadString('\n')
		if err2 != nil || io.EOF == err2 {
			break
		}
		fmt.Println(line)
	}
	err = cmd.Wait()
	if err != nil {
		fmt.Println("cmd python Wait error",err)
		ok = false
		return
	}
	ok = true
	return
}

//解析数据
func analysis_data(row_key, target_str string){
	//调用py程序
	var ok bool
	var method string
	res := run_py(target_str)
	if !res {
		time.Sleep(time.Duration (10) * time.Second)
		method = "/reduction_task?row_key=" + row_key
		_, ok = conncet_go(Addr, Port, method)
		if !ok {
			return
		}
	}else{
		method = `/success_task?row_key=` + row_key
		_, ok = conncet_go(Addr, Port, method)
		if !ok {
			return
		}
	}
}

//连接server
func conncet_go(addr, port, method string) (res []byte, ok bool) {
	fmt.Println("content go method:", method)
	resp, err := http.Get("http://" + addr + ":" + port + method)
	if err != nil {
		fmt.Println("conncet_go get error:", err)
		ok = false
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("conncet_go resp error:", err)
		ok = false
		return
	}
	fmt.Println("the resp body:", string(body))
	res = body
	ok = true
	return
}

func main() {
	if len(os.Args) != 5 {
		fmt.Println("输入参数有误！IP地址、端口、间隔时间。eg:./client /root 127.0.0.1 2103 5s")
		return
	}
	fmt.Println("Start")
	Spider_path = os.Args[1]
	Addr = os.Args[2]
	Port = os.Args[3]
	set_time, err := time.ParseDuration(os.Args[4])
	if err != nil {
		fmt.Println("输入参数有误！IP地址、端口、间隔时间。eg:./client /root 127.0.0.1 2103 5s")
		return
	}

	target_id := map[string]string {
		"1545186105" : "chingtsedallas",
		"1545186215" : "KatzeGato1",
		"1545186264" : "i9GARbXstQsKePj",
		"1545186279" : "A404411",
		"1545186297" : "bless_miles",
		"1545186313" : "niuhuabiao",
		"1545186330" : "ak47dealer",
		"1545186345" : "WilderMohn",
		"1545186366" : "YuCheng99",
		"1545186380" : "exoticgamora",
		"1545186396" : "baotong1932",
		"1545186409" : "papa_pahoo",
		"1545186421" : "hrw_chinese",
		"1545186433" : "ChenYun",
		"1545186444" : "Kenn_Zou",
		"1545186455" : "CaoChangqing",
		"1545186474" : "datomen",
		"1545186486" : "Yehuosi",
		"1545186496" : "xzs233",
		"1545186509" : "YyFKar2QyU5YD3N",
		"1545186520" : "L5d",
	}

	for key, value := range target_id {
		fmt.Println("Once Start")
		fmt.Println("key value:", key, value)
		analysis_data(key, value)
		fmt.Println("Once End")
		time.Sleep(set_time)
	}
}
