package main

import(
	"fmt"
//	"log"

	"encoding/json"
)

type Source_json struct {
	Weixin string `json:"weixin,omitempty"`
	Webnew string `json:"webnew,omitempty"`
}

type Sendtype_json struct {
	Email string `json:"email,omitempty"`
	Phonenumber string `json:"Phonenumber,omitempty"`
}

type Alertset struct {
	Switch string `json:"switch,omitempty"`
	Source Source_json
	Sendtype Sendtype_json
}

func ceshi() {
	tmp_data := map[string]string {
		"alertset_condition" : `{
			"switch" : "true",
			"source" : {
				"weixin" : "true",
				"webnew" : "true"
			},
			"sendtype" : {
				"email" : "ceshi@163.com"
			}
		}`,
	}

	tmp_obj := new(Alertset)
	err := json.Unmarshal([]byte(tmp_data["alertset_condition"]), tmp_obj)
	if err != nil {
		fmt.Println("json 解析错误", err)
		return
	}

	fmt.Println(tmp_obj)

	/*
	var column_arr []string
	var value_arr []string
	var set_arr []string

	for name, value := range tmp_data["alertset_condition"] {
		fmt.Println(name, value)
		column_arr = append(column_arr, name)
		value_arr = append(value_arr, value)
		set_arr = append(set_arr, name + `='` + value + `'`)
	}
		*/
}

func main() {
	fmt.Println("START")
	ceshi()
	tmp_source := map[string]string {
		"weixin" : "true",
		"webnew" : "true"
	}
	tmp_sendtype := map[string]string {
	}
	tmp_json := map[string]interface{} {
			"switch" : "true",
			"source" : tmp_source,
			"sendtype" : tmp_sendtype,
		},
	}
	fmt.Println("END")
}
