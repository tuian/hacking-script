$host = "localhost";
$user = "root";
$password = "";
$dbname = "";
$db_charset = 'utf8';

if (!class_exists('mysqli')) {
    function build_mysqli()
    {
        if (in_array('mysql', PDO::getAvailableDrivers())) {
            $string = 'class %cm{var $o;%f %_c($b,$c,$d,$f){$g="mysql:host=$b;dbname=$f";' .
                'try{$h->o=new PDO($g,$c,$d);}catch(PDOException $i){die($i->getMessage());}}%f ' .
                'select_db($f){%r true;}%f set_charset($j){$h->o->query("SET NAMES $j")->execute();}%f' .
                ' query($k){%r new %cm_query($h->o->query($k));}%f close(){unset($h->o);%r !0;}}' .
                'class %cm_query{var $o;%f %_c($a){$h->o=$a;}%f fetch_row(){%r $h->o->fetch(3);}' .
                '%f fetch_assoc(){%r $h->o->fetch(2);}%f close(){$h->o->closeCursor();}}';
        } else {
            $pre = function_exists('mysqli_connect') ? 'mysqli_' : 'mysql_';
            $isi = $pre == 'mysqli_' ? 1 : 0;
            $a = 'array';
            $_call = $isi ? "$a(&\$h->o),\$a" : "\$a,$a(&\$h->o)";
            $tpl = "class %s %s{%s%s}";
            $method = '%f __call($m,$a){%r call_user_func_array("' . $pre . '$m",' . $a . '_merge(' . $_call . '));}';
            $method .= "%f query(\$s){%r new %cm_query({$pre}query(" . ($isi ? '$h->o,$s' : '$s,$h->o') . "));}";
            $method .= '%f close(){unset($h->o);%r !0;}';
            $init = '%f %_c($h,$u,$p,$db){$h->o=@' . $pre . 'connect($h,$u,$p);}';
            $string = sprintf($tpl, '%cm', '', 'var $o;', $init . $method);
            $init = '%f %_c($o){$h->o=$o;}';
            $string .= sprintf($tpl, '%cm_query', ' extends %cm', '', $init);
        }
        $string = str_replace(
            array('%f', '%r', '$h->', '%_c', '%cm'),
            array('function', 'return', '$this->', '__construct', 'mysqli'), $string);
        eval(";?><?php $string;");
    }

    build_mysqli();
}
class_exists('mysqli') or die('class Mysqli does not exists');

$mysql = new mysqli($host, $user, $password, $dbname) or die('connection mysql failed..');
$mysql->select_db($dbname) or die('database ' . $dbname . ' does not exists..');
$mysql->set_charset($db_charset);

$filename = dirname(__FILE__) . '/' . date('Ymd') . ".zip";
!file_exists($filename) or unlink($filename);
touch($filename);
$string = "-- MySQL dump 10.x\n--\n-- Host: $host\tDatabase: $dbname\n-- " . str_repeat('-', 54) . "\n-- Server version        5.x\n\n";
$string .= "SET NAMES $db_charset;\nCREATE DATABASE IF NOT EXISTS $dbname CHARSET $db_charset;\nUSE $dbname;\n";
write($filename, $string);
$query = $mysql->query("SHOW TABLES");
$offset = 500;
while (list($table) = $query->fetch_row()) {
    $query2 = $mysql->query("SHOW CREATE TABLE `$table`");
    $string = "--\n-- Table structure for table `$table`\n--\n\n";
    while (list(, $structure) = $query2->fetch_row()) {
        $string .= "DROP TABL" . "E IF EXISTS `$table`;\n{$structure};\n\n";
        $query2->close();
        break;
    }
    $query2 = $mysql->query("SEL" . "ECT COUNT(*) FROM `$table`");
    list($total) = $query2->fetch_row();
    if ($total > 0) {
        $string .= "--\n-- Dumping data for table `$table`\n--\n\nLOCK TABLES `$table` WRITE;\n";
        write($filename, $string);
        unset($string, $query2, $row);
        for ($i = 0; $i < $total; $i += $offset) {
            $query2 = $mysql->query("SEL" . "ECT * FROM `$table` LIMIT $i,$offset");
            $values = array();
            while ($row = $query2->fetch_assoc()) {
                foreach ($row as $k => $item) $row[$k] = var_export($item, 1);
                $values[] = sprintf("(%s)", join(',', $row));
            }
            $string = 'INS' . "ERT INTO $table VALUES" . join(',', $values) . ";\n";
            write($filename, $string);
            $query2->close();
            unset($values, $string, $row, $query2, $item, $k);
        }
        $string = "UNLOCK TABLES;\n\n";
    }
    write($filename, $string);
    unset($query2, $string, $total);
}
$mysql->close();
write($filename, false, true);
unset($mysql);
echo "backup database success!!!";


function write($filename, $string, $close = false)
{
    static $fp = null, $write = 'fwrite', $prefix = null;
    if (null === $fp) {
        $fex = 'function_exists';
        $prefix = $fex('bzopen') ? 'bz' : $fex('gzopen') ? 'gz' : 'f';
        $mode = $prefix == 'bz' ? 'w' : 'wb';
        $fp = call_user_func("{$prefix}open", $filename, $mode);
        $write = "{$prefix}write";
    }
    if ($string) {
        (false === $write($fp, $string)) and die('Writing to file failed!');
    }
    if ($close) {
        call_user_func("{$prefix}close", $fp);
    }
}