package hbase_rest

import (
	"fmt"

	"encoding/json"
	"encoding/base64"
	"strings"
)

func Map2xml (tmp_part, tmp_map map[string]string) (tmp_row *Row_config){
	tmp_row = new (Row_config)
	tmp_row.Key = base64.StdEncoding.EncodeToString ([]byte (tmp_part["key"] + tmp_map[tmp_part["value"]]))

	for name, value := range tmp_map {
		tmp_cell := new (Cell_config)
		tmp_cell.Column = base64.StdEncoding.EncodeToString ([]byte (name))
		tmp_cell.Value = base64.StdEncoding.EncodeToString ([]byte (value))

		tmp_row.Cell = append (tmp_row.Cell, *tmp_cell)
	}

	return
}

func Json2string (json_obj interface{}) (json_str string) {
	json_byte, err := json.Marshal(json_obj)
	if err != nil {
		fmt.Println("json Marshal error", err)
		return
	}
	json_str = string(json_byte)
	return
}

func Get_filter (tmp_json map[string]string) (tmp_filter_json *Filter_json) {
	filter_tmp := map[string]string {
		"Type" : "",
		"Value" : "",
		"Op" : "",
		"Comparator_Type" : "",
		"Comparator_Value" : "",
	}
	Comparator_class := map[string]string {
		"BinaryComparator" : "base64",
		"SubstringComparator" : "string",
		"RegexStringComparator" : "string",
	}

	for name, _ := range filter_tmp {
		ss, ok := tmp_json[name]
		if !ok {
			continue
		}
		filter_tmp[name] = ss
	}

	tmp_filter_json = new(Filter_json)
	tmp_filter_json.Type = filter_tmp["Type"]
	tmp_filter_json.Value = base64.StdEncoding.EncodeToString([]byte (filter_tmp["Value"]))
	tmp_filter_json.Op = filter_tmp["Op"]

	tmp_comparator_json := new(Comparator_json)
	tmp_comparator_json.Type = filter_tmp["Comparator_Type"]
	if strings.Compare(Comparator_class[filter_tmp["Comparator_Type"]], "base64") == 0 {
		tmp_comparator_json.Value = base64.StdEncoding.EncodeToString([]byte (filter_tmp["Comparator_Value"]))
	}else if strings.Compare(Comparator_class[filter_tmp["Comparator_Type"]], "string") == 0 {
		tmp_comparator_json.Value = filter_tmp["Comparator_Value"]
	}else{
		fmt.Println("not find the Comparator_Type")
	}

	tmp_filter_json.Comparator = tmp_comparator_json

	return
}
