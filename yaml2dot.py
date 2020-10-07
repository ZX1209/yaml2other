#!/usr/bin/env python3
import yaml

import logging as log

from jinja2 import Template

log.basicConfig(level=log.DEBUG)
log.debug("this is a demo massage")

yamlstr = """
node1:
    node11:
        node111:
        node112:
    node12:
    node13:
        node131:
        node132:
    node14:
"""

dot_temp_str = """
graph temp {
    rankdir = LR
{{ nodes_str }}
}
"""

obj_yaml = yaml.load(yamlstr)


def yamlobj2mydic(prefix="", yamlobj=None):
    if yamlobj is None:
        return None

    mydic = dict()
    for index, node in enumerate(yamlobj):
        # 构建当前节点
        curid = prefix + chr(97 + index)
        mydic.update(
            {
                curid: {
                    "__label": node,
                }
            }
        )

        # 递归构造字节点
        child_dic = yamlobj2mydic(prefix=curid, yamlobj=yamlobj[node])
        # 将字节点信息加入当前节点
        if child_dic is not None:
            mydic[curid].update(child_dic)

    return mydic


mydic = yamlobj2mydic(yamlobj=obj_yaml)
log.debug(mydic)


def mydic2nodes_str(level=1, mydic=None):
    if mydic is None:
        return ""

    tmpstr = ""
    for node in mydic:
        if node != "__label":
            node_list = [k for k in mydic[node] if k != "__label"]
            nodestr = (
                "    " * level + node + "[" + "label=" + mydic[node]["__label"] + "]"
            )

            if node_list != []:
                nodestr += " -- " + "{" + ",".join(node_list) + "}\n"
            else:
                nodestr += "\n"

            tmpstr += nodestr
            tmpstr += mydic2nodes_str(level=level + 1, mydic=mydic[node])
    return tmpstr


nodes_str = mydic2nodes_str(mydic=mydic)

t = Template(dot_temp_str)

print(t.render(nodes_str=nodes_str))
