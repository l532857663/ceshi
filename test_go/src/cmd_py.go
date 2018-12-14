package main

import (
	"fmt"

	"os/exec"
	"bufio"
	"io"
	"os"
)

func run_py() {
	userid := "awdawd"
	email := "qseqse"
	password := "qweqwe"
	receive_url := "asdasd"
	var parameter []string
	parameter = append(parameter, userid)
	parameter = append(parameter, email)
	parameter = append(parameter, password)
	parameter = append(parameter, receive_url)
	fmt.Println("asdasdsad", parameter)
	cmd := exec.Command("/home/w123/git_my/mytest/test_py/spider/ceshi.py", parameter...)
	fmt.Println("cmd str:", cmd)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("cmd python StdoutPipe error",err)
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
		return
	}

	fmt.Println("End")
}


func main() {
	fmt.Println("Start")
	if len(os.Args) != 4 {
		fmt.Println("输入参数有误！IP地址、端口、间隔时间。eg:./client 127.0.0.1 2103 5")
		return
	}
	fmt.Println("argv", os.Args[1])
//	run_py()
}
