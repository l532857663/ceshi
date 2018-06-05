<?php

class Socket_communication {
    private $timeout = 10;
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

    public function startServer(){
        $this->master = socket_create_listen($this->port);
        if(!$this->master){
            throw new \ErrorException("listen {$this->port} fail !");
        }
        self::$connectPool[] = $this->master;
        while(true){
            $readFds = self::$connectPool;
            echo "ceshi\n";
            @socket_select( $readFds, $writeFds, $e = null, $this->timeout );
            echo "ceshi1\n";
            var_dump($readFds);
            $pid = pcntl_fork();
            if($pid == -1){
                die("Process open error");
            }else if($pid == 0){
                if(end($readFds)){
                    $socket = socket_accept(end($readFds));
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
        while(true){
            $bytes = @socket_recv($socket, $buffer, 2048, 0);
            if($bytes == 0){
            }
        }
    }



}

$Port = 7000;
new Socket_communication($Port);
?>
