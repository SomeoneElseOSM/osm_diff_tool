import requests
import StringIO
import xml.etree.cElementTree as ElementTree


def changesetUtil(changeset_id):
    def parseUser(source, handle):
        for event, elem in ElementTree.iterparse(source,
                                                 events=('start','end')):
            if event == 'start':
                handle.startElement(elem.tag, elem.attrib)
            elem.clear()

    class userDecoder():
        def __init__(self):
            self.creation = ""
            self.changesets = 0
            self.blocks = 0
            self.active = 0

        def startElement(self, name, attributes):
            if name == 'tag':
                for attribute in attributes:
                    if attribute == 'comment':
                        self.comment = attributes[attribute]
            elif name == 'changesets':
                self.changesets = int(attributes['count'])
            elif name == 'received':
                self.blocks = int(attributes['count'])
                self.active = int(attributes['active'])

    try:
        url = 'http://www.osm.org/api/0.6/changeset/' + str(changeset_id)

        content = requests.get(url)
        if content.status_code == 404:
            raise Exception

        content = StringIO.StringIO(content.content)

        dataObject = userDecoder()
        parseUser(content, dataObject)
        return dataObject
    except:
        return None
