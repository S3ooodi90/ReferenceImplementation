#-*- coding: utf-8 -*-
import sys
from uuid import uuid4

import xmind
from xmind.core import workbook, saver
from xmind.core.topic import TopicElement

from generate import xsdHeader, xsdMetadata, xsdDM, xsdEntry

def main(xmindfile):
    w = xmind.load(xmindfile) # load an existing file or create a new workbook if nothing is found
    indent = 2
    padding = ('').rjust(indent)
    dmid = str(uuid4())
    entryid = str(uuid4())
    xsdStr = xsdHeader()
    
    sheet = w.getPrimarySheet() 
    root = sheet.getRootTopic()
    print(root.getTitle())
    topics = root.getSubTopics()
    for topic in topics:
        title = topic.getTitle()
        print(title)
        
        if title == 'Entry':
            xsdStr = getEntry(topic, xsdStr, entryid, indent)
                    
        elif title == 'Metadata':
            md = []
            md.append(dmid)
            
            mdTopics = topic.getSubTopics()
            for mdTopic in mdTopics:
                print(padding.rjust(indent + 4) + mdTopic.getTitle())
                if mdTopic.getTitle() == 'description':
                    description = mdTopic.getSubTopics()[0].getTitle()
                print(padding.rjust(indent + 6) + mdTopic.getSubTopics()[0].getTitle())
                md.append(mdTopic.getSubTopics()[0].getTitle())
            xsdStr += xsdMetadata(md)    
            xsdStr += xsdDM([dmid, entryid, description, "Missing URI definition."])
            
        elif title == 'Project Name':
            print(padding.rjust(indent + 4) + topic.getSubTopics()[0].getTitle())
            
        elif title == 'RM Version':
            print(padding.rjust(indent + 4) + topic.getSubTopics()[0].getTitle())
            
    xsdStr += "\n</xs:schema>\n"
    
    return(dmid, xsdStr)


def getEntry(topic, xsdStr, entryid, indent):
    padding = ('').rjust(indent)
    dataClusterId = str(uuid4())
    data = [entryid, "Missing URI definition.", dataClusterId]
    xsdStr += xsdEntry(data, indent)
    
    for entryTopic in topic.getSubTopics():
        entryTopicTitle = entryTopic.getTitle()
        xsdStr += "<!-- " + padding.rjust(indent + 2) + entryTopicTitle + " -->\n"
        if entryTopicTitle == "label":
            xsdStr += "<!-- " + padding.rjust(indent + 4) + entryTopic.getSubTopics()[0].getTitle() + " -->\n"
        elif entryTopicTitle == "entry-language":
            xsdStr += "<!-- " + padding.rjust(indent + 4) + entryTopic.getSubTopics()[0].getTitle() + " -->\n"
        elif entryTopicTitle == "entry-encoding":
            xsdStr += "<!-- " + padding.rjust(indent + 4) + entryTopic.getSubTopics()[0].getTitle() + " -->\n"
        elif entryTopicTitle == "current-state":
            if entryTopic.getSubTopics():
                xsdStr += "<!-- " + padding.rjust(indent + 4) + entryTopic.getSubTopics()[0].getTitle() + " -->\n"
        elif entryTopicTitle == "(List of participations)":
            parts = entryTopic.getSubTopics()
            if parts:
                for part in parts:
                    xsdStr += entryParticipations(part, indent)
            else:
                xsdStr += "<!-- " + padding.rjust(indent + 4) + "No Participations." + " -->\n"
        elif entryTopicTitle == "(List of audits)":
            audits = entryTopic.getSubTopics()
            if audits:
                for audit in audits:
                    xsdStr += entryAudits(audit, indent)
            else:
                xsdStr += "<!-- " + padding.rjust(indent + 4) + "No audits." + " -->\n"
        elif entryTopicTitle == "(List of links)":
            links = entryTopic.getSubTopics()
            if links:
                for link in links:
                    xsdStr += entryLinks(link, indent)
            else:
                xsdStr += "<!-- " + padding.rjust(indent + 4) + "No Links." + " -->\n"
        elif entryTopicTitle == "(The data entry point)":
            xsdStr += dataCluster(entryTopic, dataClusterId, xsdStr, indent)
            
        elif entryTopicTitle == "attestation":
            xsdStr += entryAttestation(entryTopic, indent)
        elif entryTopicTitle == "subject":
            xsdStr += entrySubject(entryTopic, indent)
        elif entryTopicTitle == "provider":
            xsdStr += entryProvider(entryTopic, indent)
        elif entryTopicTitle == "protocol":
            xsdStr += entryProtocol(entryTopic, indent)
        elif entryTopicTitle == "workflow":
            xsdStr += entryWorkflow(entryTopic, indent)

    return(xsdStr)

def dataCluster(entryTopic, dataClusterId, xsdStr, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process data tree" + " -->\n")
    
def entryAudits(topics, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process audits" + " -->\n")


def entryLinks(topics, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process links" + " -->\n")


def entryParticipations(topics, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process participations" + " -->\n")
    

def entryAttestation(topic, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process attestation" + " -->\n")


def entrySubject(topic, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process subject" + " -->\n")


def entryProvider(topic, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process provider" + " -->\n")


def entryProtocol(topic, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process protocol" + " -->\n")


def entryWorkflow(topic, indent):
    padding = ('').rjust(indent)
    return( "<!-- " +padding.rjust(indent + 4) + "process workflow" + " -->\n")


# =======================
def xdboolean(topic, indent):
    return("<!-- Noop -->")


def xdcount(topic, indent):
    return("<!-- Noop -->")


def xdfile(topic, indent):
    return("<!-- Noop -->")


def xdinterval(topic, indent):
    return("<!-- Noop -->")


def xdlink(topic, indent):
    return("<!-- Noop -->")


def xdordinal(topic, indent):
    return("<!-- Noop -->")


def xdquantity(topic, indent):
    return("<!-- Noop -->")


def xdratio(topic, indent):
    return("<!-- Noop -->")


def xdstring(topic, indent):
    return("<!-- Noop -->")


def xdtemporal(topic, indent):
    return("<!-- Noop -->")





if __name__ == "__main__":
    if len(sys.argv) == 2:
        xmindfile = sys.argv[1]
    else:
        print('\n\n Please provide a XMind mindmap file to process. \n\n')
        exit()
        
    dmid, xsdStr = main(xmindfile)
    f = open('dm-' + dmid + '.xsd', 'w')
    f.write(xsdStr)
    f.close()
    


