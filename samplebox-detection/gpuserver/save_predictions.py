#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree, objectify

def root(folder, filename, width, height):
    E = objectify.ElementMaker(annotate=False)
    return E.annotation(
            E.folder(folder),
            E.filename(filename),
            E.source(
                E.database('Unknown'),
                ),
            E.size(
                E.width(width),
                E.height(height),
                E.depth(3),
                ),
            E.segmented(0)
            )

def instance_to_xml(class_label, xmin, ymin, xmax, ymax):
    E = objectify.ElementMaker(annotate=False)

    return E.object(
            E.name(class_label),
            E.bndbox(
                E.xmin(xmin),
                E.ymin(ymin),
                E.xmax(xmax),
                E.ymax(ymax),
                ),
            )

if __name__=="__main__":
    annotation = root("folder", "filename", 640, 480)
    label1 = instance_to_xml("wasabi_snack", 34, 45, 100, 100)
    label2 = instance_to_xml("butter_bisuco", 34, 45, 100, 100)    
    annotation.append(label1)
    annotation.append(label2)
    etree.ElementTree(annotation).write("{}.xml".format("temp2"))


