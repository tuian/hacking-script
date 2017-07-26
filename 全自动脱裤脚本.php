

1,先给目标表减肥 (目的是把无用的字段去掉，减小体积）       

CREATE TABLE user4 AS SELECT uid,name,email,members_pass FROM ips_members;

<?php
$sqlserver = 'localhost';
$sqluser = 'root';
$sqlname = 'test';
$sqlpass = 'root';
 
$con = mysql_connect($sqlserver,$sqluser,$sqlpass);
if($con == false){
        echo '连接数据库失败';exit;
}
 
if(mysql_select_db($sqlname,$con) == false){
        echo '打开数据库失败';exit;
}
mysql_query("set names 'utf-8'");
 
$selectnum = isset($_GET['selectnum'])?$_GET['selectnum']:0;
$startloc = isset($_GET['startloc'])?$_GET['startloc']:0;
$ifgoon = isset($_GET['ifgoon'])?$_GET['ifgoon']:1;
 
if(!empty($selectnum)&&!empty($ifgoon)){
         
        if(!($startloc)){
                $resultallnum = mysql_query("select count(*) as total from testdb");
                $allnum = mysql_fetch_array($resultallnum);
                $allnum = $allnum['total'];
                $ifgoon = ceil($allnum/$selectnum);
        }
        $sql = "select * from testdb order by id limit ".$startloc . ",".$selectnum;
        $result = mysql_query($sql);
        while($row = mysql_fetch_array($result))
        {
                if(strpos($row['testtext'], 'from91') === false){
                        echo $row['id'] . "--->" . $row['testtext'];
                        echo "<br />";
                        file_put_contents('D:/www/all.txt',implode(' ',$row)."\r\n",FILE_APPEND);
                }
        }
 
        $ifgoon = $ifgoon-1;
        if($ifgoon>0){
                $startloc = $startloc + $selectnum;
                $locurl = "http://localhost/test.php?selectnum=".$selectnum."&startloc=".$startloc."&ifgoon=".$ifgoon;
                echo $locurl;
                echo "<SCRIPT LANGUAGE='JavaScript'>";
                echo "location.href='".$locurl."'";
                echo "</SCRIPT>";
        }
}
 
 
?>
 
<form action="http://localhost/test.php" method="get">
查询条数：<input type="text" name="selectnum" value="" />
<input type="submit" value="提交" />
</form>