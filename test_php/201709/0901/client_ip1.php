<?php
/*
$myfile = fopen("./file.txt",'r');
$content = fread($myfile,18);
fclose($myfile);
 */

class syn_Report{
		public $mac_sign;
		//链接数据库
		public function sql_info($query){
				$conn = mysqli_connect("127.0.0.1","root","123456","syn_090117");
				if($conn->connect_error){
						die("连接错误是:".$conn->connect_error);
				}
				$rsObj = $conn->query($query);
				mysqli_close($conn);
				return $rsObj;
		}

		public function makeReport(){
				//路由下的设备列表、设备IP以及记录数量
				$queryMac = 'select client_src_mac,count(*) from `'.$this->mac_sign.'wifilz_client_ip_info` group by client_src_mac';

				//不同目的MAC地址的列表以及个数;
				$query= 'select client_dest_mac,count(*) from `'.$this->mac_sign.'wifilz_client_ip_info` group by client_dest_mac';
				//不同目的IP地址的列表以及个数;
				$query1 = 'select client_dest_ip,count(*) from `'.$this->mac_sign.'wifilz_client_ip_info` group by client_dest_ip';
				//不同目的端口的列表及个数;
				$query2 = 'select client_dest_port,count(*) from `'.$this->mac_sign.'wifilz_client_ip_info` group by client_dest_port';

				$rsObjMac = $this->sql_info($queryMac);

				$rsObj = $this->sql_info($query);
				$rsObj1 = $this->sql_info($query1);
				$rsObj2 = $this->sql_info($query2);

				//$queryMac Src_MAC\Src_IP
				while($rs = $rsObjMac->fetch_row()){
						$src_macList[] = $rs;
				}
				//	var_dump($src_macList);
				$massSum = 0;//数据记录总数
				foreach($src_macList as $v){
						$queryIp = 'select client_src_ip from `'.$this->mac_sign.'wifilz_client_ip_info` where client_src_mac="'.$v[0].'"';
						$rsObjIp = $this->sql_info($queryIp);
						$rs[0] = ($rsObjIp->fetch_row())[0];
						$rs[1] = $rsObjIp->num_rows;
						$src_ipList[]=$rs;

						$massSum += $v[1];
				}
				//	var_dump($src_ipList);
				//****************************************
				//$query Dest_MAC----------------------
				while($rs = $rsObj->fetch_row()){
						$dest_macList[] = $rs;	
				}
				//var_dump($dest_macList);
				//$query1 Dest_IP-------------------
				while($rs = $rsObj1->fetch_row()){
						$dest_ipList[] = $rs;	
				}
				//var_dump($dest_ipList);
				//$query2 Dest_PORT-----------------
				while($rs = $rsObj2->fetch_row()){
						$dest_portList[] = $rs;	
				}
				//var_dump($dest_portList);
				//****************************************
				//相同目的端口的IP列表以及个数;
				//$query3 PORT->IP------------------
				foreach($dest_portList as $v){
						$query3 = 'select client_src_ip,client_dest_ip from `'.$this->mac_sign.'wifilz_client_ip_info` where client_dest_port="'.$v[0].'"';
						$rsObj3 = $this->sql_info($query3);
						$j = 'Sport_'.$v[0];
						$k = 'Dport_'.$v[0];
						$m = 'SDP_'.$v[0];
						$arr = array();
						while($rs = $rsObj3->fetch_row()){
								$arr['Src'][] = $rs[0];
								$arr['Dest'][] = $rs[1];
								$arr['SDP'][] = $rs[0].'->'.$rs[1].":".$v[0];
						}
						$src_ipPort[$j] = array_count_values($arr['Src']);
						$dest_ipPort[$k] = array_count_values($arr['Dest']);
						$sdp_List[$m] = array_count_values($arr['SDP']);
				}

				//  var_dump($src_ipPort);
				//	var_dump($dest_ipPort);
				//	var_dump($sdp_List);
				/*
				 * $massSum			数据记录总数
				 * $src_macList[]	路由下设备源MAC目录
				 * $src_ipList[] 	路由下设备对应源IP～
				 * $dest_macList[]
				 * $dest_ipList[]	路由下设备目的IP～
				 * $dest_portList[]	路由下设备对应目的PORT～
				 * $src_ipPort[$j]、例$j='Sport_22';每个端口的源IP～
				 * $dest_ipPort[$k]、例$k='Dport_22';每个端口的目的IP～
				 * $sdp_List[$m]、例$m='SDP_22';设备访问～
				 */

						$strHTML = '<h3>syn握手数据表</h3><h4>数据库总数据量为：'.$massSum.' 条</h4><table border=1>';
				//--------------------------------
			//	$strA ='';$strB = '';
				$str1 = '<td>';
				foreach($src_macList as $k=>$v){
						$str1 .= $v[0].' | '.$src_ipList[$k][0].' : '.$v[1].'条<br />';
				//		$strA .= '"name":"'.$v[0].'","y":'.$v[1].'|---fgx---|';
				}
//				var_dump($strA);
/*				foreach($dest_portList as $val){
						$strB .= '"name":"'.$val[0].'端口","y":'.$val[1].'|---fgx---|';

				}
				 */


				$str1 .= '</td>';
				//--------------------------------
				$strHTML .= '<tr><td>设备下连接的MAC、IP及数量:</td>'.$str1.'</tr>';
				//--------------------------------
				$str2 = '';$str3 = '';$str4 = '';$str5 = '';
				foreach($dest_portList as $val){
						if($val[0]!="80" && $val[0]!="443"){
								$str2 .= '<tr><td>源IP:</td><td>';
								foreach($src_ipPort['Sport_'.$val[0]] as $k=>$v){
										$str2 .= $k.'有'.$v.'条<br />';
								}
								$str2 .='</td></tr><tr><td>目的PORT:</td><td>PORT:'.$val[0].' | '.$val[1].'条数据</td></tr><tr><td>目的IP:</td><td>';
								foreach($dest_ipPort['Dport_'.$val[0]] as $k=>$v){
										$str2 .= $k.'有'.$v.'条<br />';
								}
								$str2 .='</td></tr>';

								$str4 .='<tr><td>设备访问'.$val[0].'端口目录:有'.$val[1].'条数据</td><td>';
								foreach($sdp_List['SDP_'.$val[0]] as $k=>$v){
										$str4 .= $k.'有'.$v.'条<br />';
								}
								$str4 .'</td>';

						}else{
								$str3 .= '<tr><td>源IP:</td><td>';
								foreach($src_ipPort['Sport_'.$val[0]] as $k=>$v){
										$str3 .= $k.'有'.$v.'条<br />';
								}
								$str3 .='</td></tr><tr><td>目的PORT:</td><td>PORT:'.$val[0].' | '.$val[1].'条数据</td></tr><tr><td>目的IP:</td><td>';
								foreach($dest_ipPort['Dport_'.$val[0]] as $k=>$v){
										$str3 .= $k.'有'.$v.'条<br />';
								}
								$str3 .='</td></tr>';

								$str5 .= '<tr><td>设备访问'.$val[0].'端口目录:有'.$val[1].'条数据</td><td>';
								foreach($sdp_List['SDP_'.$val[0]] as $k=>$v){
										$str5 .= $k.'有'.$v.'条<br />';
								}
								$str5 .'</td>';

								}
				}
				//--------------------------------
				$strHTML .= $str4.$str2.$str5.$str3.'</table>';
$dateA = date("YmdHis",time());
$myF = fopen("./synR/synReport_".$dateA.".txt","w+");
fwrite($myF,$strHTML);
fclose($myF);
				$queryINTO = "INSERT INTO `".$this->mac_sign."wifilz_syn_report` (report_text,report_data) VALUES ('','synReport_".$dateA."')";
//		var_dump($queryINTO);
				$this->sql_info($queryINTO);
				//echo $strHTML;
		}
}
/*
$synObj = new syn_Report();
$synObj->mac_sign='E4_F4_C6_FF_86_D3_';
$synObj->makeReport();
				 */				 
?>
