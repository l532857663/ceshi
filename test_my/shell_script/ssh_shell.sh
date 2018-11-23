#!/usr/bin/expect

spawn ssh ry@192.168.201.105
expect {
	"*yes/no*" {
		send "yes\r\n"
		exp_continue
	}
	"*password*" {
		send "renyuan\r\n"
	}
}
interact
