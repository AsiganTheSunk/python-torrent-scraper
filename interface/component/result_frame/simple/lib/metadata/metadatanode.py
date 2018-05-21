#!/usr/bin/python
from metadata.metadata import Metadata

class MetadataNode:
    def __init__(self, basename, identifier, metadata=Metadata()):
        self.identifier = identifier
        self.basename = basename
        self.parent_basename = None
        self.children = []
        self.metadata = metadata

    def set_children(self, children):
        self.children = children

    def get_children(self):
        return self.children

    def get_identifier(self):
        return self.identifier

    def get_metadata(self):
        return self.metadata

    def set_basename(self, basename):
        self.basename = basename

    def set_parent_basename(self, parent_basename):
        self.parent_basename = parent_basename

    def add_child(self, child):
        '''
        This function adds a new child to node children
        :param child:
        :return:
        '''
        self.children.append(child)

    def remove_child(self, child_basename):
        '''
        This function removes a child with basename from node children
        :param child_basename:
        :return:
        '''
        new_child_list = []
        for item in self.children:
            if item.basename != child_basename:
                new_child_list.append(item)
        self.set_children(new_child_list)
        return self.children
