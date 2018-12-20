package golang_mssql

import (
	"fmt"
	"database/sql"
	_ "github.com/denisenkom/go-mssqldb"
)

type Golang_mssql struct {
	Conn *sql.DB
}

func New_golang_mssql (ipaddr string, username string, password string, db_name string, db_port int) (ret *Golang_mssql) {
    connString := fmt.Sprintf("server=%s;database=%s;user id=%s;password=%s;port=%d;encrypt=disable", ipaddr, db_name, username, password, db_port)

	var my_db = new (Golang_mssql)
	var err error

    my_db.Conn, err = sql.Open("mssql", connString)
    if err != nil {
        fmt.Println("Open connection failed:", err.Error())
		panic("open db error\nipaddr:" + ipaddr + "\nusername:" + username + "\npassword:" + password + "\ndb_name:" + db_name)
    }
    err = my_db.Conn.Ping()
    if err != nil {
        fmt.Println("PING:",err.Error())
		panic ("connect db error\nipaddr:" + ipaddr + "\nusername:" + username + "\npassword:" + password + "\ndb_name:" + db_name)
    }

	ret = my_db
    return
}

func (self *Golang_mssql) Close () {
	self.Conn.Close ()
}
