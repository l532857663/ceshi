/**
 * 文件功能：
 */

/**
 * 包功能：
 */
package wifilz_server

import (
	"wifilz_server_config"
)

type wifilz_server interface {
	Check (server_name string) (ok bool)
	Start (config wifilz_server_config.Server_config)
}

var Wifilz_server []wifilz_server
