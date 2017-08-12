<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>高精度IP地址定位服务</title>
</head>
<style>
  body {
    text-align: center;
  }

  .container, .container-fluid {
    text-align: center;
    width: 800px;
    display: inline-block;
  }
  img {
    /*width: 370px;*/
  }
  .ipt {
    height: 25px;
    padding: 0;
    margin: 0;
    border-radius: 3px;
    box-shadow: inset 0 1px 1px rgba(0,0,0,0.075);
    box-sizing: border-box;
  }
  .btn{
    height: 25px;
    background-color: #04c;
    border: 1px solid #04c;
    border-radius: 3px;
    vertical-align: top;
    box-sizing: border-box;
  }
  .btn-primary{
    color: #fff;
    text-shadow: 0 -1px 0 rgba(0,0,0,0.25);
    background-color: #006dcc;
  }
  pre{
    font-size: 14px;
    text-align: left;
  }
  .hou{
    margin-top: 10px;
    border:1px solid #ccc;
    border-radius:4px;
    background-color:#f5f5f5;
  }
  .hou-con{
    width: 500px;
    margin: auto;
  }

</style>
<body>
  <div class="container">
    <div class="container-fluid">
      <form action="ip.php" method="post">
      IP: <input type="text" name="ip" class="ipt"><br />
      <div class="hou">
      PC：<input type="radio" checked="checked" name="qterm" value="pc" /><br />
      Mobile：<input type="radio" name="qterm" value="mb" /><br />
      </div>
      <br />
      <input type="submit" value="提交" class="btn btn-primary">
      </form>
      <div class="hou">
        <?php
        include("Mobile_Detect.php");
        // error_reporting(E_ALL^E_NOTICE^E_WARNING);
        $error_info = array(
            '1'=>'服务器内部错误',
            '167'=>'定位失败',
            '101'=>'AK参数不存在'
,            '200'=>'应用不存在，AK有误请检查重试',
            '201'=>'应用被用户自己禁止',
            '202'=>'应用被管理员删除',
            '203'=>'应用类型错误',
            '210'=>'应用IP校验失败',
            '211'=>'应用SN校验失败',
            '220'=>'应用Refer检验失败',
            '240'=>'应用服务被禁用',
            '251'=>'用户被自己删除',
            '252'=>'用户被管理员删除',
            '260'=>'服务不存在',
            '261'=>'服务被禁用',
            '301'=>'永久配额超限，禁止访问',
            '302'=>'当天配额超限，禁止访问',
            '401'=>'当前并发超限，限制访问',
            '402'=>'当前并发和总并发超限'
        );
        function issucc(){

        }
        // 高精度IP定位 high accuracy IP location
        function  highacciploc($ip, $qterm){
            $tmp = explode('.',$ip);
            // 公网IP 判断
            if(filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE) && $tmp[0] != 127) {
                // IP->地址 查询和json结果解析
                $add_url ='http://api.map.baidu.com/highacciploc/v1?qcip='.$ip.'&qterm='.$qterm.'&ak=YIogecncCOvlq2oGgWqnYRUCWhKma8dY&coord=bd09ll&extensions=3';
                $add_json = file_get_contents($add_url);
                $res = json_decode($add_json, true);
                $error_code = $res["result"]["error"];

                // IP->地址 查询结果判断
                if($error_code == 161) {
                  $lng = $res['content']['location']['lng'];
                  $lat = $res['content']['location']['lat'];
                  $addr = $res["content"]["formatted_address"];
                  $business = $res['content']['business'];
                  $loc_time = $res['result']['loc_time'];
                  $radius = $res['content']['radius'];
                  $confidence = $res['content']['confidence'] * 100;
                  $area_code = $res['content']['address_component']['admin_area_code'];
                  // 静态地图
                  $img_url = 'http://api.map.baidu.com/staticimage?width=800&height=600&center='.$lng.','.$lat.'&zoom=18&markers='.$lng.','.$lat.'&markerStyles=l,A,0xff3322';
                  // 静态地图超链接，查看详细地址信息
                  $href_url = 'http://api.map.baidu.com/geocoder?address='.$addr.'&output=html&src=ysera';
                  /*
                  $href_url1 = 'http://api.map.baidu.com/marker?location='.$lat.','.$lng.'&title='.$ip.'&content='.$business.'&output=html&src=ysera';
                  $header = get_headers($href_url1,1);
                  $href_url = preg_match('/200/',$header[0]) ? $href_url1 : $href_url1;
                  */
                    echo '<pre>'.
                    'IP： '.$ip.'</br>'.
                    '定位半径： '.$radius.'m</br>'.
                    '定位可信度： '.$confidence.'%</br>'.
                    '纬度： '.$lat.'</br>'.
                    '经度： '.$lng.'</br>'.
                    '身份证前6位： '.$area_code.'</br>'.
                    '地址： '.$addr.'</br>'.
                    '定位时间： '.$loc_time.'</br>'.
                    '</pre>';
                    echo "<a href='".$href_url."' target='_blank'> "."<img src=".$img_url." /> </a>";
                    file_put_contents("location.log", date('Y-m-d H:i:s',time()).': '.$ip.' '.$addr.PHP_EOL, FILE_APPEND);
                }
                else {
                    echo '<pre>'.$GLOBALS['error_info'][$error_code].'<br /><br />以下是普通IP定位结果： <br /></pre>';
                    $city_url = 'http://api.map.baidu.com/location/ip?ip='.$ip.'&ak=YIogecncCOvlq2oGgWqnYRUCWhKma8dY';
                    $city_json = file_get_contents($city_url);
                    $city_res = json_decode($city_json, true);
                    $status = $city_res["status"];
                    if($status == 0){
                        $addr = $city_res["content"]["address"];
                        echo '<pre>'.
                        'IP： '.$ip.'</br>'.
                        '地址： '.$addr.'</br>'.
                        '</pre>';
                        file_put_contents("city.log", date('Y-m-d H:i:s',time()).': '.$ip.' '.$addr.PHP_EOL, FILE_APPEND);
                    }
                    else {
                      $message = $city_res["message"];
                      echo '<pre>'.$message.'</pre>';
                    }

                }
            }
            else{
                echo '<pre>请输入有效的公网IP地址！</pre>';
            }
        }
        // 区分自动调用和手动查询
        if(isset( $_POST['ip'])){
            $ip = $_REQUEST[ 'ip' ];
            $qterm = $_REQUEST['qterm'];
        }
        else{
            $detect = new Mobile_Detect();
            $ip = $_SERVER['REMOTE_ADDR'];
            $qterm = $detect->isMobile() ? 'mb' : 'pc';
        }
        highacciploc($ip, $qterm);
        ?>
      </div>
    </div>
  </div>
</body>
</html>
