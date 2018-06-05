<?php

$data_arr = array();
$myF = fopen("./scan_result.txt","r");
while(!feof($myF)){
    $str = fgets($myF);//逐行读取。如果fgets不写length参数，默认是读取1k。
    $data_arr[] = $str;
}
fclose($myF);
$data_all = array();
$data_main = array();
echo "BEGIN\n";
foreach ($data_arr as $val){
    $re_str = "/^BSS (.{17}).?/";
    if(preg_match($re_str,$val,$match)){
        $data_main["MAC"] = $match[1];
    }
    $re_str = "/signal: (-.*)dBm.*/";
    if(preg_match($re_str,$val,$match)){
        $data_main["SIGNAL"] = $match[1];
    }
    $re_str = "/\tSSID: (.*)\s*/";
    if(preg_match($re_str,$val,$match)){
        $data_main["SSID"] = $match[1];
    }
    $re_str = "/primary channel: (\d*)\s*/";
    if(preg_match($re_str,$val,$match)){
        $data_main["CHANNEL"] = $match[1];
        switch($match[1]){
        case 42: $data_main["CHANNEL"] = "5.21 / 42";break;
        case 50: $data_main["CHANNEL"] = "5.21 / 50";break;
        case 58: $data_main["CHANNEL"] = "5.29 / 58";break;
        case 152: $data_main["CHANNEL"] = "5.76 / 152";break;
        case 160: $data_main["CHANNEL"] = "5.8 / 160";break;
        case 36: $data_main["CHANNEL"] = "5.18 / 36";break;
        case 40: $data_main["CHANNEL"] = "5.2 / 40";break;
        case 44: $data_main["CHANNEL"] = "5.22 / 44";break;
        case 48: $data_main["CHANNEL"] = "5.24 / 48";break;
        case 52: $data_main["CHANNEL"] = "5.26 / 52";break;
        case 56: $data_main["CHANNEL"] = "5.28 / 56";break;
        case 60: $data_main["CHANNEL"] = "5.3 / 60";break;
        case 64: $data_main["CHANNEL"] = "5.32 / 64";break;
        case 149: $data_main["CHANNEL"] = "5.745 / 149";break;
        case 153: $data_main["CHANNEL"] = "5.765 / 153";break;
        case 157: $data_main["CHANNEL"] = "5.785 / 157";break;
        case 161: $data_main["CHANNEL"] = "5.805 / 161";break;
        case 165: $data_main["CHANNEL"] = "5.825 / 165";break;
        default: $data_main["CHANNEL"] = "5.825 / 165";break;
        }
    }
    if(count($data_main) == 4){
        $data_all[] = $data_main;
        $data_main = [];
    }
}
echo "END\n";
var_dump($data_all);
?>
