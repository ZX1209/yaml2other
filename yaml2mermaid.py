#!/usr/bin/env python3
import yaml
import logging as log
from jinja2 import Template

log.basicConfig(level=log.DEBUG)


yamlstr = """
node1:
    node11:
        node111:
            node1111:
            node1112:
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


class MMNode:
    def __init__(self, id, label, children=None, level=1):
        """__init__
        children should be the type of a list
        """
        self.id = id
        self.label = label
        self._children = [] if children is None else children
        self.level = level

    @property
    def children_ids(self):
        """chlidren_ids"""
        if self.has_children():
            return [i.id for i in self._children]
        else:
            return []

    @property
    def children(self):
        """children"""
        return self._children

    @children.setter
    def children(self, values):
        """set children
        values should be MMNode List
        """
        self._children = values

    def has_children(self):
        """has_children"""
        return len(self.children) > 1

    def indent_str(self):
        return "    " * self.level

    def attr_to_str(self):
        """to_str"""
        return f'{self.id}["{self.label}"]'

    def to_str(self):
        tmp_str = ""
        for node in self.children:
            tmp_str += self.indent_str() + self.attr_to_str()
            tmp_str += " --- "
            tmp_str += node.attr_to_str()
            tmp_str += "\n"

            tmp_str += node.to_str()

        return tmp_str


class MMData:
    def __init__(self, dictobj=None, prefix=""):
        """__init__
        dictobj should be yaml dict
        """
        self.dictobj = dictobj
        self.tran_data()

    def tran_data(self):
        """tran_data"""

        def yamlobj2MMNode(prefix="", yamlobj=None, level=0):
            if yamlobj is None:
                return []

            tmpnodes = []
            for index, node in enumerate(yamlobj):
                # 构建当前节点
                curid = prefix + chr(97 + index)
                tmpnode = MMNode(id=curid, label=node, level=level)

                # 递归构造字节点
                tmpnode.children = yamlobj2MMNode(
                    prefix=curid, yamlobj=yamlobj[node], level=level + 1
                )
                tmpnodes.append(tmpnode)

            return tmpnodes

        self.nodes = yamlobj2MMNode(yamlobj=self.dictobj)

    def to_str(self):
        """to_str"""

        tmp_str = ""
        for line in self.nodes:
            tmp_str += line.to_str()
        return tmp_str


def tran_yaml_str2mermaid_str(yaml_str):
    yaml_obj = yaml.load(yaml_str)
    if yaml_obj is not None and type(yaml_obj) == dict:
        dd = MMData(yaml_obj)
        return dd.to_str()
    else:
        return ""


if __name__ == "__main__":
    print(tran_yaml_str2mermaid_str(yamlstr))
