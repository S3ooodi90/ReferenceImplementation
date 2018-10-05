"""
Meta information classes used by a data model (DMType)

"""
from abc import ABC, abstractmethod


class PartyType:
    """
    Description of a party, including an optional external link to data for this party in a demographic or other identity management system. An additional details element provides for the inclusion of information related to this party directly. If the party
    information is to be anonymous then do not include the details element.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._party_name = None
        self._party_ref = None
        self._party_details = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class AuditType:
    """
    AuditType provides a mechanism to identify the who/where/when tracking of instances as they move from system to system.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._system_id = None
        self._system_user = None
        self._location = None
        self._timestamp = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class AttestationType:
    """
    Record an attestation by a party of the DM content. The type of attestation is recorded by the reason attribute, which my be coded.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self._label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._view = None
        self._proof = None
        self._reason = None
        self._committer = None
        self._committed = None
        self._pending = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)


class ParticipationType:
    """
    Model of a participation of a Party (any Actor or Role) in an activity. Used to represent any participation of a Party in some activity, which is not explicitly in the model, e.g. assisting nurse. Can be used to record past or future participations.
    """

    def __init__(self, label):
        """
        The semantic label (name of the model) is required.
        """
        self._mcuid = cuid()  # model cuid
        self._label = ''

        if checkers.is_string(label, 2):
            if len(label) > 1:
                self.label = label
            else:
                raise ValueError('label must be at least 2 characters in length')
        else:
            raise TypeError('"label" must be a string type. Not a ', type(label))

        self._performer = None
        self._function = None
        self._mode = None
        self._start = None
        self._end = None

    @property
    def label(self):
        """
        The semantic name of the component.
        """
        return self._label

    def __str__(self):
        return(self.__class__.__name__ + ' : ' + self.label + ', ID: ' + self.mcuid)

