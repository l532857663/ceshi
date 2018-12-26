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
	parameter = append(parameter, "http://" + Addr + ":4455/receive")
//	fmt.Println("parameter:", parameter)
	cmd := exec.Command(Spider_path + "/spider_twitter.py", parameter...)
	fmt.Println("cmd str:", cmd)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fmt.Println("cmd python StdoutPipe error",err)
		ok = false
		return
	}
	fmt.Println("cmd 1")
	cmd.Start()
	fmt.Println("cmd 2")
	reader := bufio.NewReader(stdout)
	fmt.Println("cmd 3")
	for {
		line, err2 := reader.ReadString('\n')
		if err2 != nil || io.EOF == err2 {
			break
		}

		fmt.Println(line)
	}
	fmt.Println("cmd 4")
	err = cmd.Wait()
	if err != nil {
		fmt.Println("cmd python Wait error",err)
		ok = false
		return
	}
	fmt.Println("cmd 5")
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
		"1545186105" : "chingtsedallas",	//?
		/*
		avatar_url is empty
name is empty
user_id is 824086394385510400
screen_name is chingtsedallas
tweets_count is empty
following_count is empty
followers_count is empty
likes_count is empty
sent_url:
Traceback (most recent call last):
  File "/root/spider_twitter.py", line 863, in get_user_information
    self.analysis_user_information(html)
  File "/root/spider_twitter.py", line 849, in analysis_user_information
    avatar = self.get_pictrue_imag(avatar_url)
  File "/root/spider_twitter.py", line 296, in get_pictrue_imag
    content = self.opener.open(request)
  File "/usr/lib/python2.7/urllib2.py", line 421, in open
    protocol = req.get_type()
  File "/usr/lib/python2.7/urllib2.py", line 283, in get_type
    raise ValueError, "unknown url type: %s" % self.__original
ValueError: unknown url type:
unknown url type:
		*/
		"1545186215" : "KatzeGato1",		//OK
		"1545186264" : "i9GARbXstQsKePj",	//没ID
		/*
https://twitter.com/i9GARbXstQsKePj
---------------analysis user information start----------------
avatar_url is https://pbs.twimg.com/profile_images/1047544970419175425/PPIpEDqn_400x400.jpg
name is 余额不足
user_id is empty
screen_name is empty
tweets_count is empty
following_count is empty
followers_count is empty
likes_count is empty
sent_url: https://pbs.twimg.com/profile_images/1047544970419175425/PPIpEDqn_400x400.jpg
		*/
		"1545186279" : "A404411",			//OK
		"1545186297" : "bless_miles",		//OK
		"1545186313" : "niuhuabiao",		//没ID
/*name is 自然的最美
user_id is empty
screen_name is empty
tweets_count is empty
following_count is empty
followers_count is empty
likes_count is empty
sent_url: https://pbs.twimg.com/profile_images/864356040514523136/JLnLXrnk_400x400.jpg
*/
		"1545186330" : "ak47dealer",		//OK

		"1545186345" : "WilderMohn",		//OK
		"1545186366" : "YuCheng99",			//有问题
//HTTPError: HTTP Error 404: Not Found
//HTTP Error 404: Not Found
		"1545186380" : "exoticgamora",		//没ID
		"1545186396" : "baotong1932",		//OK
		"1545186409" : "papa_pahoo",		//OK
		"1545186421" : "hrw_chinese",		//OK
		"1545186433" : "ChenYun",			//OK

		"1545186444" : "Kenn_Zou",			//OK
		"1545186455" : "CaoChangqing",		//OK
		"1545186474" : "datomen",			//OK
		"1545186486" : "Yehuosi",			//OK
		"1545186496" : "xzs233",			//OK
		"1545186509" : "YyFKar2QyU5YD3N",	//有问题
		/*
		https://twitter.com/YyFKar2QyU5YD3N
---------------analysis user information start----------------
avatar_url is empty
name is empty
user_id is 1054272756152291328
screen_name is YyFKar2QyU5YD3N
tweets_count is empty
following_count is empty
followers_count is empty
likes_count is empty
sent_url:
Traceback (most recent call last):
  File "/root/spider_twitter.py", line 863, in get_user_information
    self.analysis_user_information(html)
  File "/root/spider_twitter.py", line 849, in analysis_user_information
    avatar = self.get_pictrue_imag(avatar_url)
  File "/root/spider_twitter.py", line 296, in get_pictrue_imag
    content = self.opener.open(request)
  File "/usr/lib/python2.7/urllib2.py", line 421, in open
    protocol = req.get_type()
  File "/usr/lib/python2.7/urllib2.py", line 283, in get_type
    raise ValueError, "unknown url type: %s" % self.__original
ValueError: unknown url type:
unknown url type:
		*/
		"1545186520" : "L5d",				//
		/*
		avatar_url is https://pbs.twimg.com/profile_images/1058078122464153600/-FR6SpkZ_400x400.jpg
name is Humanrights for China e.V.
user_id is empty
screen_name is empty
tweets_count is empty
following_count is empty
followers_count is empty
likes_count is empty
sent_url: https://pbs.twimg.com/profile_images/1058078122464153600/-FR6SpkZ_400x400.jpg
		*/
	}

	for key, value := range target_id {
		fmt.Println("Once Start")
		fmt.Println("key value:", key, value)
		analysis_data(key, value)
		fmt.Println("Once End")
		time.Sleep(set_time)
	}
}
