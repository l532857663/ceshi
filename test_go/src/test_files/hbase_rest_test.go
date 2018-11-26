package test_files

import (
	"testing"
//	"fmt"
	"sync"

//	"strings"
	"hbase_search_database"
)

func Test_get_data (t *testing.T) {
	var mutex sync.Mutex
	var flag int
	Hrest := hbase_search_database.New_hbase_rest ("http://192.168.201.112:9900", &mutex, &flag)

//	Get_test_func(Hrest)
//	Put_test_func(Hrest)
	Scan_test_func(Hrest)
}

