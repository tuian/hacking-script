# coding=utf-8

TEMPLATE_html = """
<html>
<head>
<title>WVSearch Report</title>
<style>
    body {width:960px; margin:auto; margin-top:10px; background:rgb(200,200,200);}
    p {color: #666;}
    h2 {color:#002E8C; font-size: 1em; padding-top:5px;}
</style>
</head>
<body>
<p>Welcome to use the Wooyun Vulnerabilities Search. *<b> WVSearch </b>*</p>
<p>Current Search was finished in ${cost_min} min ${cost_seconds} seconds.</p>
<P><b>${total_name}</b> vulnerabilities match the requirements of searching in total.</p>
${content}
</body>
</html>
"""

TEMPLATE_result = """
 <li class="high"><a href="${url}" target="_blank">${name}</a></li>
"""
