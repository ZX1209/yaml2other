#!/usr/bin/env python3
import yaml
import logging as log
from jinja2 import Template

log.basicConfig(level=log.DEBUG)


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


class DotNode:
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
        values should be DotNode List
        """
        self._children = values

    def has_children(self):
        """has_children"""
        return len(self.children) > 1

    def attr_to_str(self):
        """to_str"""
        return "    " * self.level+self.id + "[" + "label=" + self.label + "]"

    def link_to_str(self):
        """to_str"""
        if self.has_children():
            return "    " * self.level + self.id+" -- " + "{" + ",".join(self.children_ids) + "}"
        else:
            return ""

    def def_str(self):
        """def_str
        """
        tmpstr = self.attr_to_str() + "\n"
        for node in self.children:
            tmpstr += node.def_str()
        return tmpstr

    def link_str(self):
        """def_str
        """
        if self.has_children():
            tmpstr = self.link_to_str() + "\n"
            for node in self.children:
                tmpstr += node.link_str()
            return tmpstr
        else:
            return ""


class DotData:
    def __init__(self, dictobj=None, prefix=""):
        """__init__
        dictobj should be yaml dict
        """
        self.dictobj = dictobj
        self.tran_data()

    def tran_data(self):
        """tran_data"""

        def yamlobj2DotNode(prefix="", yamlobj=None, level=0):
            if yamlobj is None:
                return []

            tmpnodes = []
            for index, node in enumerate(yamlobj):
                # 构建当前节点
                curid = prefix + chr(97 + index)
                tmpnode = DotNode(id=curid, label=node, level=level)

                # 递归构造字节点
                tmpnode.children = yamlobj2DotNode(
                    prefix=curid, yamlobj=yamlobj[node], level=level + 1
                )
                tmpnodes.append(tmpnode)

            return tmpnodes

        self.nodes = yamlobj2DotNode(yamlobj=self.dictobj)

    def to_str(self):
        """to_str"""
        def_str = ""
        link_str = ""
        for node in self.nodes:
            def_str += node.def_str() + "\n"
            link_str += node.link_str()
        return def_str + link_str


def tran_yaml_str2dot_str(yaml_str):
    yaml_obj = yaml.load(yaml_str)
    dd = DotData(yaml_obj)
    return dd.to_str()


if __name__ == "__main__":
    print(tran_yaml_str2dot_str(yamlstr))
