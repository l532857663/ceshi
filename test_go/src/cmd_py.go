package main

import (
	"fmt"

	"os/exec"
	"bufio"
	"io"
	"os"
	"strings"
	"time"
	"syscall"
)

func run_py() {
	userid := "awdawd"
	email := "error"
	password := "qweqwe"
	receive_url := "asdasdqwe\n"
	var parameter []string
	parameter = append(parameter, userid)
	parameter = append(parameter, email)
	parameter = append(parameter, password)
	parameter = append(parameter, receive_url)
	fmt.Println("asdasdsad", parameter)
	cmd := exec.Command("/home/w123/git_my/mytest/test_py/spider/ceshi.py", parameter...)
	cmd.SysProcAttr = &syscall.SysProcAttr{Setpgid: true}
	fmt.Println("cmd str:", cmd)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("cmd python StdoutPipe error",err)
		return
	}
	cmd.Start()
	fmt.Println("cmd pid:", cmd.Process.Pid)
	fmt.Println("start time:", time.Now())

	timer := time.AfterFunc(time.Duration(20)*time.Second, func () {
		if cmd.Process != nil {
			fmt.Println("py pid:", cmd.Process.Pid)
			syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
//			cmd.Process.Kill()
		}
	})

	fmt.Println("time2:", time.Now())
	reader := bufio.NewReader(stdout)
	for {
		line, err2 := reader.ReadString('\n')
		if err2 != nil || io.EOF == err2 {
			fmt.Println ("aaa:", err2)
			break
		}
		if strings.Compare(line, "error\n") == 0 {
			fmt.Println("the py is error")
			res := timer.Stop()
			fmt.Println("Stop:", res)
			break
		}

		ok := timer.Reset(time.Duration(20)*time.Second)
		if !ok {
			break
		}

		fmt.Println(line)
	}
	fmt.Println("cmd pid3:", cmd.Process.Pid)
	fmt.Println("time3:", time.Now())
	err = cmd.Wait()
	if err != nil {
		fmt.Println("cmd python Wait error",err)
		return
	}
	fmt.Println("end time:", time.Now())

	fmt.Println("End")
}

func main() {
	fmt.Println("Start")
	if len(os.Args) != 4 {
		fmt.Println("输入参数有误！IP地址、端口、间隔时间。eg:./client 127.0.0.1 2103 5")
		return
	}
	fmt.Println("argv", os.Args[1])
	run_py()
}
