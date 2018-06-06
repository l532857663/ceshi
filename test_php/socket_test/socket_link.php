<?php

class Socket_communication {
    private $timeout = 10;
	private $handShake = False;
	private $userLogin = False;
	private $master;
    private $port;
    private $i = 0;
    private static $connectPool = [];

    public function __construct($port = 0){
        if(empty($port)){
            die("Not add port\n");
        }
        $this->port = $port;
        $this->startServer();
    }

    //握手信息
	protected function doHandShake($socket, $buffer){ 
		list($resource, $host, $origin, $key) = $this->getHeaders($buffer);
		$upgrade = "HTTP/1.1 101 Switching Protocol\r\n"
			. "Upgrade: websocket\r\n" 
			. "Connection: Upgrade\r\n"
			. "Sec-WebSocket-Accept: "
			. $this->calcKey($key)
			. "\r\n\r\n";
		socket_write($socket, $upgrade, strlen($upgrade));
        $this->handShake = True;
        return True;
	}
	private function getHeaders($req){
		$r = $h = $o = $key = null;
		if(preg_match("/GET (.*) HTTP/" , $req, $match)){
			$r = $match[1];
		}
		if (preg_match("/Host: (.*)\r\n/" , $req, $match)){
			$h = $match[1];
		}
		if (preg_match("/Origin: (.*)\r\n/" , $req, $match)){
			$o = $match[1];
		}
		if(preg_match("/Sec-WebSocket-Key: (.*)\r\n/", $req, $match)){
			$key = $match[1];
		}
		return [$r, $h, $o, $key];
	}
	private function calcKey($key){ 
		$accept = base64_encode(sha1($key . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11', true));
		return $accept;
	}
	public function frame($buffer){
		$len = strlen($buffer);
		if ($len <= 125){
			return "\x81" . chr($len) . $buffer;
		}else if ($len <= 65535){
			return "\x81" . chr(126) . pack("n", $len) . $buffer;
		}else{
			return "\x81" . chr(127) . pack("xxxxN", $len) . $buffer;
		}
    }

    //编码转换
	private function decode($buffer){
		$len = $masks = $data = $decoded = null;
		$len = ord($buffer[1]) & 127;
		if ($len === 126){
			$masks = substr($buffer, 4, 4); $data = substr($buffer, 8);
		}else if ($len === 127){
			$masks = substr($buffer, 10, 4); $data = substr($buffer, 14);
        }else{
            $masks = substr($buffer, 2, 4);
			$data = substr($buffer, 6);
		}
        for ($index = 0; $index < strlen($data); $index++){
            $decoded .= $data[$index] ^ $masks[$index % 4];
        }
		return $decoded;
	}

    //关闭清除链接
	protected function disConnect($socket){ 
        $index = array_search($socket, self::$connectPool);
		socket_close($socket);
		if ($index >= 0){
			array_splice( self::$connectPool, $index, 1 );
		} 
	} 

    public function startServer(){
        $this->master = socket_create_listen($this->port);
        if(!$this->master){
            throw new \ErrorException("listen {$this->port} fail !");
        }
        self::$connectPool[] = $this->master;
        while(True){
            $readFds = self::$connectPool;
            @socket_select( $readFds, $writeFds, $e = null, $this->timeout );
            $pid = pcntl_fork();
            if($pid == -1){
                die("Process open error");
            }else if($pid == 0){
                if(end($readFds)){
                    $socket = socket_accept(end($readFds));
                    if($socket < 0){
                        die("Clint connect error");
                    }
                    array_push(self::$connectPool, $socket);
                    $this->keeplink($socket);
                }
                die();
            }else{
                sleep(1);
                continue;
            }
        }
        echo "over\n";
    }

    protected function keeplink($socket){
        while(True){
        var_dump($this->handShake);
            $bytes = @socket_recv($socket, $buffer, 2048, 0);
            if($bytes == 0){
                echo "over2\n";
                $this->userLogin = False;
				$re = $this->disConnect($socket);
				if(!$re){
					break;
				}
			}else{
				if(!$this->handShake){
					$this->doHandShake($socket, $buffer);
				}else{
					$buffer = $this->decode($buffer);
					$this->parseMessage($buffer, $socket);
				}
            }
            echo "over1\n";
        }
    }

    public function parseMessage($message, $socket){
        $message = json_decode( $message, true );
        if($this->userLogin){
        }else{
            $username = $message['userNM'];
            $password = $message['passWD'];
            $htmlname = $message['htmlNM'];
        }

    }

    //回传函数
	public function send( $client, $msg ){
		//$msg = $this->frame( json_encode( $msg ) ); 
		$msg = $this->frame($msg); 
		$return = socket_write( $client, $msg, strlen($msg) ); 
		return $return;
	} 

}

$Port = 7000;
new Socket_communication($Port);
?>
