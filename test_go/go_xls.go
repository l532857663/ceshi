package main

import (
		"fmt"
		"encoding/base64"
		"time"
		"strconv"
		"strings"
		"io/ioutil"

		"net/http"

		"github.com/360EntSecGroup-Skylar/excelize"
)

var hbase_host = "http://192.168.11.133:9900"
var hbase_table_name = "dxy"
var time_format = "2006-01-02 15:04:05"

func get_data (row []string, timestamp string) (res string) {
		res = "{'type': '"
		res += row[13]
		res += "', 'host_number': '"
		res += row[2]
		res += "', 'host_city': '"
		res += row[3]
		res += "', 'other_number': '"
		res += row[0]
		res += "', 'other_city': '"
		res += row[4]
		res += "', 'talk_time': '"
		res += row[1]
		res += "', 'talk_city': '"
		res += row[7]
		res += "', 'host_imsi': '"
		res += row[5]
		res += "', 'host_imei': '"
		res += row[6]
		res += "', 'bureau_number': '"
		res += row[8]
		res += "', 'station_lac': '"
		res += row[9]
		res += "', 'station_cell_id': '"
		res += row[10]
		res += "', 'station_longitude': '"
		res += row[11]
		res += "', 'station_latitude': '"
		res += row[12]
		res += "', 'timestamp': '"
		res += timestamp
		res += "'}"

		return
}

func main(){

		loc, err := time.LoadLocation ("Local")
		if err != nil {
				panic (err)
		}

		xlsx, err := excelize.OpenFile("test.xlsx")
		if err != nil {
				fmt.Println(err)
				return
		}

		sheelName := xlsx.GetSheetName(1)
		rows := xlsx.GetRows(sheelName)
		for row_num, row := range rows {
				if row_num == 0 {
						continue
				}

				cmd_str := "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><CellSet><Row key=\""

				cmd_str += base64.StdEncoding.EncodeToString ([]byte (row[2]))

				cmd_str += "\"><Cell column=\""

				get_time, err := time.ParseInLocation (time_format, row[14], loc)
				if err != nil {
						panic (err)
				}

				cmd_str += base64.StdEncoding.EncodeToString ([]byte ("timestamp:" + strconv.FormatInt (get_time.Unix () - get_time.Unix () % 600, 10)))

				cmd_str += "\">" + base64.StdEncoding.EncodeToString ([]byte (get_data (row, strconv.FormatInt (get_time.Unix (), 10)))) + "</Cell></Row></CellSet>"

				fmt.Println(cmd_str)

				url := hbase_host + "/" + hbase_table_name + "/fakerow"

				client := &http.Client{}
				body := strings.NewReader(cmd_str)
				req, err := http.NewRequest("PUT", url, body)
				if err != nil {
						fmt.Println(err.Error)
						return
				}
				req.Header.Set("Accept", "text/xml")
				req.Header.Set("Content-Type", "text/xml")

				fmt.Println("请求: ",req)
				resp, err := client.Do(req)
				if err != nil {
						panic (err)
				}

				defer resp.Body.Close()
				fmt.Println("回应: ",resp)
				respBody, err := ioutil.ReadAll(resp.Body)
				if err != nil {
						fmt.Println(err.Error)
						return
				}

				fmt.Println(string(respBody))

		}
}
