<?php
header("content-type:text/html;charset=utf-8");
/*
----------------------------------------
|在$link处修改对应数据库的用户名、密码 |
----------------------------------------
*/
$filename=substr(strrchr(__FILE__,'\\'),1); //windows系统
#Linux系统为：$filename=substr(strrchr(__FILE__,'/'),1);
$link=mysql_connect("localhost","root","root");
mysql_query("set names utf8");
if(empty($_GET)){
echo "<h3>所有数据库如下：</h3>";
$sql1="show databases";
$result1=mysql_query($sql1);
while($rel1=mysql_fetch_array($result1)){
echo $rel1[0]."&nbsp<a href={$filename}?db={$rel1[0]}>查看表</a><br />";
}
}
if(!empty($_GET['db'])){
$db=$_GET['db'];
echo "当前数据库：".$db;
echo "&nbsp&nbsp&nbsp&nbsp<a href='{$filename}'>返回上级</a><br />";
mysql_query("use $db");
$sql2="show tables";
$result2=mysql_query($sql2);
while($rel2=mysql_fetch_array($result2)){
echo "<br />".$rel2[0]."&nbsp&nbsp&nbsp<a href='{$filename}?db2={$db}&tb2={$rel2[0]}'>查看数据</a>";
}
}
if(!empty($_GET['tb2'])){
$db2=$_GET['db2'];
$tb2=$_GET['tb2'];
echo "当前数据库：<a href='{$filename}?db={$db2}'>".$db2."</a>>当前表".$tb2."<br /><br />";
mysql_query("use $db2");
$sql4="select * from $tb2";
$result4=mysql_query($sql4);
$count=mysql_num_fields($result4);
echo "<table border=1 cellpadding=3 cellspacing=0>";
echo "<tr>";
for($i=0;$i<$count;++$i){
echo "<td>".mysql_field_name($result4,$i)."</td>";
}
while($rel=mysql_fetch_array($result4)){
echo "<tr>";
for($i=0;$i<$count;++$i){
$field_name=mysql_field_name($result4,$i);
echo "<td>".$rel[$field_name]."</td>";
}
echo "</tr>";
}
echo "</tr>";
echo "</table>";
}
?>