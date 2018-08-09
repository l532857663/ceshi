package send_static_res

import (
	"fmt"
	"net/http"
	"io"
	"os"
	"strings"
	"path"
)

func Send (res_path string, w http.ResponseWriter, req *http.Request) {
	// fmt.Println (res_path + req.URL.Path)
	if strings.Compare ("/", req.URL.Path) == 0{
		req.URL.Path = "/index.go"
	}

	// fmt.Println (path.Clean (res_path + req.URL.Path)[0:len (path.Clean (res_path))])
	if strings.Compare (path.Clean(res_path), path.Clean (res_path + req.URL.Path)[0:len (path.Clean(res_path))]) != 0 {
		fmt.Fprintf (w, "fuck you")
		return
	}

	file, err := os.Open (res_path + req.URL.Path)
	if err != nil {
		w.WriteHeader (http.StatusNotFound)
		fmt.Fprintf (w, "找不到文件：%s", req.URL.Path)
		return
	}

	defer file.Close ()

	io.Copy (w, file)
}
