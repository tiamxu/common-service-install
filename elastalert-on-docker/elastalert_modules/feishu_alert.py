#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: aaron
@contact: hi121073215@gmail.com
@date: 2021-10-18
@version: 0.0.0
@license:
@copyright:
"""

import json
import requests
import time

from elastalert.alerts import Alerter, DateTimeEncoder
from elastalert.util import elastalert_logger, EAException
from requests.exceptions import RequestException


class FeishuAlert(Alerter):
    # 定义必需的配置选项
    required_options = frozenset(
        ['feishualert_botid', "feishualert_title", "feishualert_body"])

    def __init__(self, rule):
        # 调用父类的初始化方法
        super(FeishuAlert, self).__init__(rule)
        # 获取飞书机器人的URL，若未配置则使用默认值
        self.url = self.rule.get(
            "feishualert_url", "https://open.feishu.cn/open-apis/bot/v2/hook/")
        # 获取飞书机器人的ID
        self.bot_id = self.rule.get("feishualert_botid", "")
        # 获取告警标题
        self.title = self.rule.get("feishualert_title", "")
        # 获取告警内容模板
        self.body = self.rule.get("feishualert_body", "")
        # 获取跳过告警的时间区间配置
        self.skip = self.rule.get("feishualert_skip", {})

        # 验证配置是否有效
        if self.bot_id == "" or self.title == "" or self.body == "":
            raise EAException("Configure botid|title|body is invalid")

    def get_info(self):
        # 返回告警类型信息
        return {
            "type": "FeishuAlert"
        }

    def get_rule(self):
        # 返回规则对象
        return self.rule

    def alert(self, matches):
        # 获取当前时间的时分秒格式字符串
        now = time.strftime("%H:%M:%S", time.localtime())

        # 检查是否在跳过告警的时间区间内
        if "start" in self.skip and "end" in self.skip:
            if self.skip["start"] <= now and self.skip["end"] >= now:
                print("Skip match in silence time...")
                return

        # 设置请求头，指定内容类型为JSON
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }

        # 构建飞书富文本消息体
        body = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh-CN": {
                        "title": self.title,
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": "你的小可爱上线了！"
                                }
                            ]
                        ]
                    }
                }
            }
        }

        # 如果有匹配的数据
        if len(matches) > 0:
            try:
                # 设置告警时间
                self.rule["feishualert_time"] = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime())
                # 合并匹配数据和规则数据
                merge = dict(**matches[0], **self.rule)
                # 格式化告警内容
                full_text = self.body.format(**merge)
                # 更新富文本消息体中的文本内容
                body["content"]["post"]["zh-CN"]["content"][0][0]["text"] = full_text[:500]

                full_title = self.title.format(**merge)
                #formatted_title = '<h2 style="color:red;">{}</h2>'.format(full_title)
                body["content"]["post"]["zh-CN"]["title"] = full_title
                #body["content"]["post"]["zh-CN"]["title"] = formatted_title
            except Exception as e:
                # 记录告警内容格式化错误日志
                elastalert_logger.error(f"Error formatting alert body: {e}")

        try:
            #print("Full alert content111:", body["content"]["post"]["zh-CN"]["content"][0][0]["text"])

            url = self.url + self.bot_id
            #print("url:", url)
            #print("data:", json.dumps(body))
            #print("headers:", headers)
            # 发送POST请求到飞书机器人
            res = requests.post(data=json.dumps(body), url=url, headers=headers)
            # 检查请求是否成功
            res.raise_for_status()
            result = res.json()
            if result.get("code") and result["code"] != 0:
                print(result["msg"])
                return
            print("消息发送成功.")
        except KeyError as ke:
            elastalert_logger.error(f"KeyError occurred: {str(ke)}")
        except TypeError as te:
            elastalert_logger.error(f"TypeError occurred: {str(te)}")
        except RequestException as e:
            # 如果请求失败，抛出异常
            raise EAException("Error request to feishu: {0}".format(str(e)))
        except Exception as e:
            # 捕获其他未知异常
            elastalert_logger.error(f"Unexpected error occurred: {str(e)}")
