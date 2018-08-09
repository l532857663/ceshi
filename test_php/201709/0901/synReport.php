<?php
include_once("./client_ip1.php");
$synObj = new syn_Report();
$synObj->mac_sign='E4_F4_C6_FF_86_D3_';
$synObj->makeReport();
/*
$mac_sign = $synObj->mac_sign;
$conn = mysqli_connect("127.0.0.1","root","123456","syn_090117");
$query = 'select report_data from `'.$mac_sign.'wifilz_syn_report`';
$rsObj = $conn->query($query);
if($rsObj){
		while($rs = $rsObj->fetch_row()){
				$dataList[] = $rs[0];
		}
}*/
$path = "./synR/*.txt"; 
	foreach(glob($path) as $afile){ 
		$dataList[] = $afile;
	} 
$dataList = array_reverse($dataList);
$strName = '<div style="float:right">';
foreach($dataList as $v){
		$strName .="<p>".$v."</p>"; 
		$myF = fopen($v,"r+");
		$strHTML .= fgets($myF)."<hr />";
		fclose($myF);
}
$strName .= "</div>";

	echo $strName;
echo $strHTML;
?>
