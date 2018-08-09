<?php 
$myfile = fopen("../../php/file.txt",'r'); 
$content = fread($myfile,18); 
fclose($myfile); 
?> 
<div class="main-title"><p>上线设备数据</p></div> 
<div class="sxsj-content"> 
 <div class="ht-tab lf sxsbsj_sj" style="height: auto;"> 
 
 <div class="ht-tab-tit"><i class="icon-browser" style="font-size: 2rem"></i></div> 
 <ul id="sxsbsj_con" class="tab_lf" style="margin-top: 30px;margin-left: 10px; line-height: 20px;"> 
 <!--<li><span>设备mac</span><b>1223333</b></li>--> 
 <!--<li><span>手机号：</span><b>123123123123</b><br/><b>123112332</b></li>--> 
 <!--<li><span>QQ号：</span><b>4564456<br/>12324645</b></li>--> 
 <!--<li><span>IMSI：</span><b>1321321321<br/>54664521312321</b></li>--> 
 <!--<li><span>IMEI：</span><b>21132132213<br/>45431221312</b></li>--> 
 </ul> 
 <div class="input-group" style="margin: 1rem"> 
 <!--<label ng-controller="ctrl.select.basic">--> 
 <!--<select class="form-control" ng-model="vm.value" ng-options="city.label for city in vm.cities">--> 
 <!--<option value="">&#45;&#45; 请选择查询方式 &#45;&#45;</option>--> 
 <!--</select></label>--> 
 <label> 
 <select name="" id="kws" style="border: 1px solid #CCCCCC;padding: 0.3rem;"> 
 <option value="">请选择查询方式</option> 
 <option value="phone_num"> 手机号 </option> 
 <option value="qq_number"> QQ号 </option> 
 <option value="imei"> IMEI </option> 
 <option value="imsi"> IMSI </option> 
 </select> 
 </label> 
 <input type="text" class="form-control" id="kvs"> 
 </div><!-- /input-group --> 
 <button id="iosNo" class="btn btn-primary lf" style="margin-left: 1rem" onclick="scbb()"><i class="icon-file-text2"></i>&nbsp;生成数据报告</button> 
 <button class="btn btn-success btn-sm rt" style="margin-right: 2rem;margin-bottom: 1rem" data-toggle="modal" data-target="#myModal" onclick='ceshi()'>详情</button> 
 </div> 
 <div class="sxsj-right lf sxsbsj_sj"> 
 <div id="piecharts"></div> 
 </div> 
 
</div> 
 
 
<!-- 模态框（Modal） --> 
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true"> 
 <div class="modal-dialog"> 
 <div class="modal-content" style="overflow: auto"> 
 <div class="modal-header"> 
 <!-- <button type="button" class="close" data-dismiss="modal" aria-hidden="true"> 
 &times; 
 </button>--> 
 <button class="btn rt close_top" onclick="document.getElementById('close-id').click();">关闭</button> 
 <h4 class="modal-title" id="myModalLabel"> 
 标题 
 </h4> 
 </div> 
 <div class="modal-body" id="zhan"> 
 
 
 </div> 
 <div class="modal-footer"> 
 <button type="button" id="close-id" class="btn btn-default" data-dismiss="modal">关闭 
 </button> 
 <!--<button type="button" class="btn btn-primary">--> 
 <!--提交更改--> 
 <!--</button>--> 
 </div> 
 </div><!-- /.modal-content --> 
 </div><!-- /.modal --> 
</div> 
 
<script> 
var u = navigator.userAgent; 
var isAndroid = u.indexOf('Android') > -1 || u.indexOf('Adr') > -1; 
var isiOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/); 
if(isiOS==true){ 
document.getElementById("iosNo").style.display="none"; 
} 
 
 
 var Request = new UrlSearch(); //实例化 
 var sMac = Request.client_mac; 
 var query = "select * from `<?php echo $content;?>wifilz_big_data_main` where data_src_mac='" + sMac + "'"; 
 sql_info(query); 
 //数据库操作 
 function sql_info(query) { 
 var db = openDatabase("ceshi02", "1.0", "Test DB", 2 * 1024 * 1024); 
 db.transaction(function (tx) { 
 tx.executeSql(query, [], function (tx, results) { 
 var dataList = new Array(); 
 var len = results.rows.length, i; 
 for (i = 0; i < len; i++) { 
 var dataS = new Array(); 
 var dataArr = new Array(); 
 for (var j in results.rows.item(i)) { 
 if (results.rows.item(i)[j]) { 
 dataS[j] = results.rows.item(i)[j]; 
 } 
 if (dataS[j] != "NULL") { 
 dataArr[j] = dataS[j]; 
 dataList[i] = dataArr; 
 } 
 } 
 } 
 if (i == len) { 
 makecao(dataList, len); 
 } 
 }, null); 
 }); 
 } 
 
 function makecao(dataList, len) { 
 var coon = " <li>设备MAC：<b>" + sMac + "</b></li> "; 
 var pli = "", qli = "", eli = "", sli = ""; 
 for (var i = 0; i < len; i++) { 
 if (typeof(dataList[i].phone_num) != "undefined") { 
 pli += "<b>" + dataList[i].phone_num + "</b><br/>"; 
 } else { 
 pli += ""; 
 } 
 if (typeof(dataList[i].qq_number) != "undefined") { 
 qli += "<b>" + dataList[i].qq_number + "</b><br/>"; 
 } else { 
 qli += ""; 
 } 
 if (typeof(dataList[i].imsi) != "undefined") { 
 sli += "<b>" + dataList[i].imsi + "</b><br/>"; 
 } else { 
 sli += ""; 
 } 
 if (typeof(dataList[i].imei) != "undefined") { 
 eli += "<b>" + dataList[i].imei + "</b><br/>"; 
 } else { 
 eli += ""; 
 } 
 } 
 if (pli != "") { 
 coon += "<li><span>手机号：</span>" + pli + "</li>"; 
 } 
 if (qli != "") { 
 coon += "<li><span>QQ号：</span>" + qli + "</li>"; 
 } 
 if (sli != "") { 
 coon += "<li><span>IMSI：</span>" + sli + "</li>"; 
 } 
 if (eli != "") { 
 coon += "<li><span>IMEI：</span>" + eli + "</li>"; 
 } 
 document.getElementById("sxsbsj_con").innerHTML += coon; 
 } 
 
 //获取提交查询栏的变量 
 function ceshi() { 
 var kword = document.getElementById("kws").value; 
 var kval = document.getElementById("kvs").value; 
 makeMain(sMac, kword, kval,'<?php echo $content;?>'); 
 } 
 
 // 获取地址栏中参数 
 function UrlSearch() { 
 var name, value; 
 var str = location.href; //取得整个地址栏 
 var num = str.indexOf("?"); 
 str = str.substr(num + 1); //取得所有参数 stringvar.substr(start [, length ] 
 
 var arr = str.split("&"); //各个参数放到数组里 
 for (var i = 0; i < arr.length; i++) { 
 num = arr[i].indexOf("="); 
 if (num > 0) { 
 name = arr[i].substring(0, num); 
 value = arr[i].substr(num + 1); 
 this[name] = value; 
 } 
 } 
 } 
 
 function fake_click(obj) { 
 var ev = document.createEvent("MouseEvents"); 
 ev.initMouseEvent( 
 "click", true, false, window, 0, 0, 0, 0, 0 
 , false, false, false, false, 0, null 
 ); 
 obj.dispatchEvent(ev); 
 } 
 function scbb(){ 
 function export_raw(name, data) { 
 var urlObject = window.URL || window.webkitURL || window; 
 
 var export_blob = new Blob([data]); 
 
 var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a") 
 save_link.href = urlObject.createObjectURL(export_blob); 
 save_link.download = name; 
 fake_click(save_link); 
 } 
 var test=document.getElementById('zhan').innerHTML; 
 export_raw('test.html', test); 
 } 
 
</script> 
<script> 
 // 饼状图 
 
 $(function () { 
 var db = openDatabase('ceshi02', '1.0', 'ceshi01', 5 * 1024 * 1024); 
 db.transaction(function (tx) { 
 var allnum = 0; 
 /* tx.executeSql('SELECT count(*) from wifilz_big_data_info where data_src_mac="' + sMac + '"', [], function (tx, rsas) { 
 allnum = rsas.rows[0]['count(*)']; 
 });*/ 
 tx.executeSql('SELECT data_channel_0,count(data_channel_0) from `<?php echo $content;?>wifilz_big_data_info` where data_src_mac="'+sMac+'" group by data_channel_0', [], function (tx, rsa) { 
 var len = rsa.rows.length; 
 var dataChan=new Array; 
 for(var i=0;i<len;i++) 
 { 
 allnum+=rsa.rows.item(i)['count(data_channel_0)']; 
 } 
 for(var i= 0;i<len;i++) 
 { 
 var dataStr=rsa.rows.item(i).data_channel_0; 
 var dataA=(rsa.rows.item(i)['count(data_channel_0)'])/allnum*100; 
 var dataSA={'name':dataStr,'y':dataA}; 
 dataChan[i]=dataSA; 
 } 
 makehigh(dataChan); 
 
 
 }); 
 }); 
 function makehigh(dataC) { 
 $('#piecharts').highcharts({ 
 chart: { 
 plotBackgroundColor: null, 
 plotBorderWidth: null, 
 plotShadow: false 
 }, 
 title: { 
 text: '所属公司分类比' 
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
 name: '浏览器访问量占比', 
 data: dataC 
 }] 
 }); 
 } 
 }); 
</script> 


