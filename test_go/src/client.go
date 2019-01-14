package main

import (
	"fmt"
	"time"
	"net/http"
	"io/ioutil"

	"encoding/json"
	"strings"
	"os/exec"
	"bufio"
	"io"
	"os"
//	"syscall"
)

var Addr string
var Port string
var Spider_path string

type conntent_obj struct {
	Error_msg string `json:"error_msg,omitempty"`
	Task_obj task_obj `json:"task_obj,omitempty"`
}

type task_obj struct {
	Task_rowkey string `json:"task_rowkey,omitempty"`
	User_rowkey string `json:"user_rowkey,omitempty"`
	Userid string `json:"info:userid,omitempty"`
	Module string `json:"module,omitempty"`
	Spider_module string `json:"spider_method,omitempty"`
	Email string `json:"info:email,omitempty"`
	Password string `json:"info:password,omitempty"`
	Receive_url string `json:"info:receive_url,omitempty"`
	Method string `json:"info:method,omitempty"`
}

//解析返回结果
func run_py(task_data task_obj) (ok bool) {
//	fmt.Println("the task data:", task_data)
	var parameter []string
	parameter = append(parameter, task_data.Userid)
	parameter = append(parameter, task_data.Spider_module)
	parameter = append(parameter, task_data.Email)
	parameter = append(parameter, task_data.Password)
	parameter = append(parameter, task_data.Receive_url)
//	fmt.Println("parameter:", parameter)
	cmd := exec.Command(Spider_path + "/spider_" + task_data.Method + ".py", parameter...)
//	cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
	fmt.Println("cmd str:", cmd)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("cmd python StdoutPipe error",err)
		ok = false
		return
	}
	cmd.Start()
	//启动定时器，监控py是否超时无回复
	timer := time.AfterFunc(time.Duration(30)*time.Minute, func () {
		if cmd.Process != nil {
			fmt.Println("py pid:", cmd.Process.Pid)
		//	syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
			cmd.Process.Kill()
		}
	})
	reader := bufio.NewReader(stdout)
	for {
		line, err := reader.ReadString('\n')
		if io.EOF == err || err != nil {
			fmt.Println("py over or err:", err)
			break
		}
		if strings.Compare(line, "") == 0 {
			fmt.Println("python line:", line)
			continue
		}
		//重置定时装置
		ok := timer.Reset(time.Duration(30)*time.Minute)
		if !ok {
			break
		}
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
func analysis_data(body []byte){
	data_obj := new(conntent_obj)
	err := json.Unmarshal(body, data_obj)
	if err != nil {
		fmt.Println("json Unmarshal error:", err)
		return
	}
//	fmt.Println("ask task json:", data_obj)
	if strings.Compare(data_obj.Error_msg, "get task ok") != 0 {
		fmt.Println("ask task error:", data_obj.Error_msg)
		return
	}
	//调用py程序
	var ok bool
	var post_str string
	var method string
	res := run_py(data_obj.Task_obj)
	if !res {
		time.Sleep(time.Duration (10) * time.Second)
		post_str = `?task_rowkey=` + data_obj.Task_obj.Task_rowkey + `&user_rowkey=` + data_obj.Task_obj.User_rowkey + `&module=` + data_obj.Task_obj.Module + `&method=` + data_obj.Task_obj.Method
		method = `/reduction_task` + post_str
		body, ok = conncet_go(Addr, Port, method)
		if !ok {
			return
		}
	}else{
		post_str = `?task_rowkey=` + data_obj.Task_obj.Task_rowkey + `&user_rowkey=` + data_obj.Task_obj.User_rowkey + `&module=` + data_obj.Task_obj.Module + `&method=` + data_obj.Task_obj.Method
		method = `/success_task` + post_str
		body, ok = conncet_go(Addr, Port, method)
		if !ok {
			return
		}
	}
	analysis_data(body)
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
	method := "/search_task"

	for {
		fmt.Println("Once Start")
		body, ok := conncet_go(Addr, Port, method)
		if !ok {
			fmt.Println("Once End")
			time.Sleep(set_time)
			continue
		}
		analysis_data(body)
		fmt.Println("Once End")
		time.Sleep(set_time)
	}
}
