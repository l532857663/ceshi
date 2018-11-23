/**
 * 文件功能：测试代码，整个包的功能测试
 */

package hbase_search_database

import (
	"testing"
	"fmt"
	"sync"

	"strings"
	"hbase_search_database/test_file"
)

func Test_Fuck (t *testing.T) {
	var mutex sync.Mutex
	var flag int
	Hrest := New_hbase_rest ("http://192.168.201.112:9900", &mutex, &flag)

	Get_test_func(Hrest)
}

