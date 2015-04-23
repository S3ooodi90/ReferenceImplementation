# Model forms for the admin
from django.forms import ModelForm, CharField, ValidationError
from cmgen.models import *

class DvBooleanAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvBooleanAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvBoolean
        fields = '__all__'


class DvLinkAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvLinkAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvLink
        fields = '__all__'

class DvStringAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvStringAdminForm, self).clean()
        # are the number of enums and enums_Def correct?
        enums = cleaned_data['enums']
        enums_def = cleaned_data['enums_def']
        if len(enums.splitlines()) != len(enums_def.splitlines()):
            if len(enums_def.splitlines()) == 1: # allow one def to be replicated for all enums
                ed = enums_def.splitlines()[0]
                newDefs = []
                for x in range(0,len(enums.splitlines())):
                    newDefs.append(ed)
                    print(newDefs)
                cleaned_data['enums_def'] = '\n'.join(newDefs)
            else:
                raise ValidationError("The number of 'Enumerations' and 'Enumeration Definitions' must be exactly the same. Check for empty lines.")

        return

    class Meta:
        model = DvString
        fields = '__all__'

class DvParsableAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvParsableAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvParsable
        fields = '__all__'

class DvMediaAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvMediaAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvMedia
        fields = '__all__'

class DvIntervalAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvIntervalAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvInterval
        fields = '__all__'

class ReferenceRangeAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(ReferenceRangeAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = ReferenceRange
        fields = '__all__'

class DvOrdinalAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvOrdinalAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvOrdinal
        fields = '__all__'

class DvCountAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvCountAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvCount
        fields = '__all__'


class DvQuantityAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvQuantityAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvQuantity
        fields = '__all__'


class DvRatioAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvRatioAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvRatio
        fields = '__all__'

class DvTemporalAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(DvTemporalAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvTemporal
        fields = '__all__'

class PartyAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(PartyAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Party
        fields = '__all__'


class AuditAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(AuditAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Audit
        fields = '__all__'


class AttestationAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(AttestationAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Attestation
        fields = '__all__'


class ParticipationAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(ParticipationAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Participation
        fields = '__all__'

class ClusterAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(ClusterAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Cluster
        fields = '__all__'

class ConceptAdminForm(ModelForm):

    def clean(self):
        cleaned_data = super(ConceptAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Concept
        fields = '__all__'













