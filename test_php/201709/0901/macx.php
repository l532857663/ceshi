<?php 
include_once "../../php/client_ip.php";
$myfile = fopen("../../php/file.txt",'r'); $content = fread($myfile,18); fclose($myfile); 
if(!empty($POST['flage']) && $POST['flage']=='begin'){
	$synObj = new syn_Report;
	$synObj->mac_sign = $content;
	$synObj->makeReport();
}
 
?> 
<style type="text/css">
input{
 border: 1px solid #B1B1B1;
 border-radius: 3px;
 line-height:15px;
}
</style>
<div class="main-title"><p>连接跟踪</p></div> 
<div class="ym-content"> 
 <div class="ym-btn"> 

<button class="btn btn-success" id="data_main" style="margin-bottom:0.5rem;" onclick="synMAKE()">生成syn数据报表</button>
<button class="btn btn-primary btn-sm btn_bottom" onclick="soket()"><i class="icon-loop2"></i>&nbsp;更新数据</button> 
 <div style="display: inline-block;margin-left: 2rem;font-size: 16px;font-weight: bold;">当前终端设备：总计<p style="color: red;display: inline-block;" id="macx_connt"></p>条</div> 
 <button type="button" class="btn btn-primary" data-toggle="modal" data-target=".macx_chaxun_modal">多级查询</button> 
 <a href="/wifilz_data/php/delete_database.php?del_macx=<?php echo $content?>"><button class="btn" style="color: #000;">删除数据</button></a>
 </div> 
 <!--遮罩层和进度条--> 
 <div id="shades"></div> 
 <div id="jindu"> 
 <p>数据正在加载中... 请稍候!</p> 
 <div class="progress"> 
 <div id="shu" class="progress-bar" role="progressbar" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100" style="width: 0;"> 
 
 </div> 
 
 </div> 
 <div id="connt" style="display: inline-block;float: right; margin-top: -1.5rem;margin-right: 0.5rem"></div> 
 <button class="btn jindu_close" onclick="document.getElementById('shades').style.display='none';document.getElementById('jindu').style.display='none';">关闭</button> 
 </div> 
 <!--主体内容--> 
 
 <div id="sj_mac"> 
 
 </div> 
 <div id="piecharts"> 
 
 </div> 
 <div id="container"></div>

 <!--分页--> 
 <nav style="margin-left: 115rem"> 
 <ul class="pagination" id="sj_page_id"> 
 </ul> 
 </nav><!--分页结束--> 
 
</div> 

<!--scoket连接--> 
<script>
function synMAKE(){
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open ("get","/wifilz_data/tpl/sxsb/macx.php?flage=BEGIN");
	xmlhttp.send ();
}
function soket(){ 
		var db = openDatabase('ceshi02', '1.0', 'ceshi01', 5 * 1024 * 1024); 
		db.transaction(function (tx) { 
		   tx.executeSql('DROP TABLE IF EXISTS `<?php echo $content; ?>wifilz_syn_report`'); 
		soket1 ();
		});
}
function soket1 () { 
		ws = new WebSocket('ws://192.168.250.1:4444'); 

		ws.onopen = function () { 
				var mag = '{"name" : "wifilz","user" : "<?php echo $content; ?>wifilz_syn_report"}'; 
				ws.send(mag); 
		};  
		var iss = '0'; 
		var count = 0;  
		var flage = 0;
		ws.onmessage = function (wifilz_syn_report) { 
				var data = $.parseJSON(wifilz_syn_report.data); 
				var wifilz_syn_report = data; 
				var db = openDatabase('ceshi02', '1.0', 'ceshi01', 5 * 1024 * 1024); 

				db.transaction(function (tx) { 
						tx.executeSql('CREATE TABLE IF NOT EXISTS `<?php echo $content; ?>wifilz_syn_report`(report_id unique, report_text, report_data, report_date)'); 
						if(flage ==1){
								tx.executeSql('INSERT INTO `<?php echo $content; ?>wifilz_syn_report` (report_id,report_text,report_data,report_date) VALUES (?, ?, ?, ?)', [wifilz_syn_report.report_id, wifilz_syn_report.report_text, wifilz_syn_report.report_data, wifilz_syn_report.report_time]); 
						}
						flage = 1;
						if (iss=='0') { 
								count = wifilz_syn_report.nums; 
								document.getElementById("connt").innerHTML=count; 
						}	

						document.getElementById("shu").innerHTML=iss; 
						var baifen = Math.ceil(iss/count*100)+ '%'; 
						document.getElementById("shu").style.width = baifen; 
						iss ++; 
						if((iss-1)==count ){  
								document.getElementById('shades').style.display='none'; 
								document.getElementById('jindu').style.display='none'; 
								window.location.reload();
						}
				}); 
		}; 
				document.getElementById('shades').style.display='block'; 
				document.getElementById('jindu').style.display='block';
}
</script>

 
<!--highcharts图形展示--> 
<script> 
function showReport(){
var reportText,dataList,dataSa = new Array();
var db = openDatabase('ceshi02', '1.0', 'ceshi01', 5 * 1024 * 1024);
db.transaction(function (tx) { 
		tx.executeSql('select * from `<?php echo $content; ?>wifilz_syn_report` order by rowid desc limit 1',[],function (tx,results){
				reportText = results.rows.item(0).report_text;
				dataList = results.rows.item(0).report_data;
				document.getElementById('sj_mac').innerHTML = reportText;
		},null); 
});
}
showReport();
/*
// 饼状图 

		var dataChan = new Array();
				dataChan[0] = {'name':'00:cf:e0:1e:eb:35','y':537604};
	dataChan[1] = {'name':'38:d5:47:ab:13:d8','y':1};
 makehigh(dataChan);

 function makehigh(dataC) { 
 $('#piecharts').highcharts({ 
 chart: { 
 plotBackgroundColor: null, 
 plotBorderWidth: null, 
 plotShadow: false 
 }, 
 title: { 
 text: '设备数据图形展示:'
 }, 
 tooltip: { 
 headerFormat: '{series.name}<br>', 
 pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>' 
 }, 
 plotOptions: { 
 pie: { 
 allowPointSelect: true, 
 cursor: 'pointer', 
 dataLabels: { 
 enabled: true, 
 format: '<b>{point.name}</b>: {point.percentage:.1f} %', 
 style: { 
 color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black' 
 } 
 } 
 } 
 }, 
 series: [{ 
 type: 'pie', 
 name: '路由下设备MAC占比', 
 data: dataC 
 }] 
 }); 
 } 

 //柱状图
 $(function () {
		 $('#container').highcharts({
		 chart: {
		 type: 'column'
 },
		 title: {
		 text: '堆叠柱形图'
 },
		 xAxis: {
		 categories: ['苹果', '橘子', '梨', '葡萄', '香蕉']
 },
		 yAxis: {
		 min: 0,
				 title: {
				 text: '水果消费总量'
 			},
			 stackLabels: {
		 		enabled: true,
					 style: {
					 fontWeight: 'bold',
						 color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
 				}
 			}			
 		},
		 legend: {
		 align: 'right',
				 x: -30,
				 verticalAlign: 'top',
				 y: 25,
				 floating: true,
				 backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
				 borderColor: '#CCC',
				 borderWidth: 1,
				 shadow: false
 		},
		 tooltip: {
		 formatter: function () {
				 return '<b>' + this.x + '</b><br/>' +
						 this.series.name + ': ' + this.y + '<br/>' +
						 '总量: ' + this.point.stackTotal;
		 }
 	},
		 plotOptions: {
		 column: {
		 stacking: 'normal',
				 dataLabels: {
				 enabled: true,
						 color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
						 style: {
						 textShadow: '0 0 3px black'
		 }
		 }
		 }
		 },
		 series: [{
				 name: '小张',
						 data: [5, 3, 4, 7, 2]
		 }, {
		 name: '小彭',
				 data: [2, 2, 3, 2, 1]
		 }, {
		 name: '小潘',
				 data: [3, 4, 4, 2, 5]
		 }]
 });
 });
*/
</script> 
<script> 
 
 
 // 分页展示 
 function fenyesj(value=1) { 
 document.getElementById("sj_page_id").innerHTML = ""; 
 document.getElementById("sj_mac").innerHTML = ""; 
 var db = openDatabase('ceshi02', '1.0', 'ceshi01', 5 * 1024 * 1024); 
 db.transaction(function(tx){
 	}); 
 } 
 
 
  
fenyesj();
</script> 

