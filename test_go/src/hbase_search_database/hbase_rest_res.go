/**
 * 文件功能：构造Hbase结构
 */

package hbase_search_database

import (
	//"fmt"
	"encoding/xml"
)

//查询结果框架 -----------------------------
type Hbase_resp_row struct {
	Row []Row_config `xml:"Row"`
	Table []Table_config `xml:"table"`
}
type Table_config struct {
	XMLName xml.Name `xml:"table"`
	Name string `xml:"name,attr"`
}
type Row_config struct {
	XMLName xml.Name `xml:"Row"`
	Key string `xml:"key,attr"`

	Cell []Cell_config `xml:"Cell"`
}
type Cell_config struct {
	XMLName xml.Name `xml:"Cell"`
	Column string `xml:"column,attr"`
	Timestamp string `xml:"timestamp,attr"`
	Value string `xml:",innerxml"`
	Timestamp_int64 int64
}

//插入数据json框架-------------------------
type Hbase_insert_json struct {
	Configs []map[string]string `json:"configs"`
	Datas []map[string]string `json:"datas"`
}

//插入数据xml框架 ------------------------
type Hbase_insert_config struct {
	XMLName xml.Name `xml:"CellSet"`
	Row []Row_set `xml:"Row"`
}
type Row_set struct {
	XMLName xml.Name `xml:"Row"`
	Key string `xml:"key,attr"`

	Cell []Cell_set `xml:"Cell"`
}
type Cell_set struct {
	XMLName xml.Name `xml:"Cell"`
	Column string `xml:"column,attr"`
	Value string `xml:",innerxml"`
}

//操作url结构------------------------------
type Hbase_url_config struct {
	Namespace string
	Tablename string
	Row string
	Family string
	Column string
	Value string
}

//scanner Json ----------------------------
type Hbase_scanner_json struct {
	Batch string `json:"batch,omitempty"`
	Begin_row string `json:"begin_row,omitempty"`
	End_row string `json:"end_row,omitempty"`
	Filter string `json:"filter,omitempty"`
}

//scanner XML ------------------------------
type Scanner_config struct {
	XMLName xml.Name `xml:"Scanner"`
	Batch string `xml:"batch,attr"`
	StartRow string `xml:"startRow,attr"`
	EndRow string `xml:"endRow,attr"`
	Filter string `xml:"filter"`
}

//filter模型设置-----------------------------
type Filter_json struct {
	Type string `json:"type,omitempty"`
	Value string `json:"value,omitempty"`
	Family string `json:"family,omitempty"`
	Op string `json:"op,omitempty"`
	Comparator *Comparator_json `json:"comparator,omitempty"`
}
type Comparator_json struct {
	Type string `json:"type,omitempty"`
	Value string `json:"value,omitempty"`
}
