"""
Data Model 
"""


class DMType:
    """
    This is the root node of a Data Model (DM)
    """

    def __init__(self):
        """
        The Data Model is the wrapper for all of the data components as well as the semantics.
        """
        self._mcuid = cuid()
        self.metadata = self.genMD()
        self._data = ClusterType()
        self._label = self.metadata['title']
        self._dm_language = self.metadata['language']
        self._dm_encoding = 'utf-8'
        self._current_state = ''
        self._subject = None
        self._provider = None
        self._participations = list()
        self._protocol = None
        self._workflow = None
        self._acs = None
        self._audits = list()
        self._attestations = list()
        self._links = list()

    def __str__(self):
        return("S3Model Data Model\n" + "ID: " + self.mcuid + "\n" + self.showMetadata(self.metadata))

    def showMetadata(self):
        mdStr = ''
        for k, v in self.metadata.items():
            mdStr += k + ': ' + repr(v) + '\n'
        return(mdStr)

    def genMD(self):
        """
        Create a metadata dictionary for the DM if one isn't passed in.
        """
        md = OrderedDict()
        md['title'] = 'New Data Model'
        md['creator'] = 'Joe Smith'
        md['subject'] = 'S3M DM'
        md['rights'] = 'Creative Commons'
        md['relation'] = 'None'
        md['coverage'] = 'Global'
        md['type'] = 'S3Model Data Model (DM)'
        md['identifier'] = 'dm-' + self.mcuid
        md['description'] = 'Needs a description'
        md['publisher'] = 'Data Insights, Inc.'
        md['date'] = '{0:%Y-%m-%dT%H:%M:%S}'.format(datetime.now())
        md['format'] = 'text/xml'
        md['language'] = 'en-US'

        return(md)
