#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# author t0ols

import config
import discuz

if __name__ == '__main__':
    try:
        my_account = discuz.Discuz()  # 实例化对象
        my_account.login(config.USERNAME, config.PASSWORD, config.QUESTIONID, config.ANSWER)  # 从配置文件中把相关参数传过去
        for item in my_account.getDomain():
            my_account.cha(item)
            my_account.check()
    except Exception as e:
        print e
