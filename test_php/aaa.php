<?php

$a = "12h";
echo (int)$a*60;
echo "\n";

$aa = "3,192.168.11.1 6,114.114.114.114,8.8.8.8";
$arr = explode(" ",$aa);
var_dump($arr);
$gat = explode(",",$arr[0]);
$vaar = explode(",",$arr[0])[1];
var_dump($gat,$vaar);

?>
