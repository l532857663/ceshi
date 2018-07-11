package main

import (
	"file_into_hbase"
	"os"
)

func main() {
	if len (os.Args) == 3 {
		file_into_hbase.Start (os.Args[1], os.Args[2])
	}else{
		panic("args len not 3")
	}

}
