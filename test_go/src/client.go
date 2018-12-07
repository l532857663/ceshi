package main

import (
	"fmt"
	"time"
	"net/http"
	"io/ioutil"

	"encoding/json"
	"strings"
	"os/exec"
)

type conntent_obj struct {
	Error_msg string `json:"error_msg,omitempty"`
	Task_obj task_obj `json:"task_obj,omitempty"`
}

type task_obj struct {
	Status string `json:"ceshi:status,omitempty"`
	Userid string `json:"ceshi:userid,omitempty"`
	Email string `json:"ceshi:email,omitempty"`
	Password string `json:"ceshi:password,omitempty"`
	Receive_url string `json:"ceshi:receive_url,omitempty"`
}

//解析返回结果
func run_py(task_data task_obj) {
	fmt.Println("the task data:", task_data)
	var parameter []string
	parameter = append(parameter, task_data.Userid)
	parameter = append(parameter, task_data.Email)
	parameter = append(parameter, task_data.Password)
//	parameter = append(parameter, task_data.Receive_url)
	fmt.Println("asdasdsad", parameter)
	cmd := exec.Command("/home/w123/git_my/mytest/test_py/spider/spider_twitter.py", parameter...)
	fmt.Println("cmd str:", cmd)
	err := cmd.Run()
	if err != nil {
		fmt.Println("cmd python run error", err)
		return
	}
}

//从server任务池取任务
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
	//解析数据
	data_obj := new(conntent_obj)
	err = json.Unmarshal(body, data_obj)
	if err != nil {
		fmt.Println("json Unmarshal error:", err)
		return
	}
	fmt.Println("ask task json:", data_obj)
	if strings.Compare(data_obj.Error_msg, "get task ok") != 0 {
		fmt.Println("ask task error:", data_obj.Error_msg)
		return
	}
	fmt.Println("ask task json data:", data_obj.Task_obj)
	fmt.Println("ask task json data:", data_obj.Task_obj.Status)
	fmt.Println("ask task json data:", data_obj.Task_obj.Email)
	//调用py程序
	run_py(data_obj.Task_obj)
}

func main() {
	fmt.Println("Start")
	var set_time time.Duration
	set_time = 5
	addr := "192.168.11.133"
	port := "8848"
	method := "/search_task"
	conncet_go(addr, port, method)
	for {
		time.Sleep(set_time * 1000000000)
	}
}
