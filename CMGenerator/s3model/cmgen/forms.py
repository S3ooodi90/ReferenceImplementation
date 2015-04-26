# Model forms for the admin
from django.forms import ModelForm, CharField, ValidationError, ModelMultipleChoiceField
from cmgen.models import *


#TODO: put this in a utils module.
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return(False)

class DvBooleanAdminForm(ModelForm):
##    semantics = ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        super(DvBooleanAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True
##        else:
##            self.fields['semantics'].queryset = PredObj.objects.filter(prj_name=self.fields['prj_name'])


    def clean(self):
        cleaned_data = super(DvBooleanAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvBoolean
        fields = '__all__'

class DvLinkAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvLinkAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvLinkAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvLink
        fields = '__all__'

class DvStringAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvStringAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

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
    def __init__(self, *args, **kwargs):
        super(DvParsableAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvParsableAdminForm, self).clean()
        # are the number of enums and enums_Def correct?
        enums = cleaned_data['fenums']
        enums_def = cleaned_data['fenums_def']
        if len(enums.splitlines()) != len(enums_def.splitlines()):
            if len(enums_def.splitlines()) == 1: # allow one def to be replicated for all enums
                ed = enums_def.splitlines()[0]
                newDefs = []
                for x in range(0,len(enums.splitlines())):
                    newDefs.append(ed)
                    print(newDefs)
                cleaned_data['fenums_def'] = '\n'.join(newDefs)
            else:
                raise ValidationError("The number of Formalism 'Enumerations' and 'Enumeration Definitions' must be exactly the same. Check for empty lines.")
        cleaned_data['language'] = cleaned_data['lang']

        return

    class Meta:
        model = DvParsable
        fields = '__all__'

class DvMediaAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvMediaAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvMediaAdminForm, self).clean()
        # are the number of enums and enums_Def correct?
        enums = cleaned_data['fenums']
        enums_def = cleaned_data['fenums_def']
        if len(enums.splitlines()) != len(enums_def.splitlines()):
            if len(enums_def.splitlines()) == 1: # allow one def to be replicated for all enums
                ed = enums_def.splitlines()[0]
                newDefs = []
                for x in range(0,len(enums.splitlines())):
                    newDefs.append(ed)
                    print(newDefs)
                cleaned_data['fenums_def'] = '\n'.join(newDefs)
            else:
                raise ValidationError("The number of Formalism 'Enumerations' and 'Enumeration Definitions' must be exactly the same. Check for empty lines.")

        cleaned_data['language'] = cleaned_data['lang']

        return

    class Meta:
        model = DvMedia
        fields = '__all__'

class DvIntervalAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvIntervalAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvIntervalAdminForm, self).clean()

        if cleaned_data['interval_type'] == 'None':
            raise ValidationError("You must select an Interval Type.")

        if 'lower' in cleaned_data:
            l = cleaned_data['lower']
        else:
            l = None

        if 'upper' in cleaned_data:
            u = cleaned_data['upper']
        else:
            u = None

        # check for modelling errors
        if cleaned_data['lower_bounded'] and (l == None or cleaned_data['lower'] == ''):
            raise ValidationError("Enter lower value or uncheck the lower bounded box.")
        if cleaned_data['upper_bounded'] and (u == None or cleaned_data['upper'] == ''):
            raise ValidationError("Enter upper value or uncheck the upper bounded box.")

        if not cleaned_data['lower_bounded'] and l:
            raise ValidationError("Remove lower value or check the lower bounded box.")
        if not cleaned_data['upper_bounded'] and u:
            raise ValidationError("Remove upper value or check the upper bounded box.")

        if cleaned_data['interval_type'] == 'duration':
            if u and not u.startswith('P'):
                raise ValidationError("Durations must begin with the character 'P' (Upper value)")
            if l and not l.startswith('P'):
                raise ValidationError("Durations must begin with the upper case character 'P' (Lower value)")

        # check valid decimals and if the user used a comma as a decimal separator then replace it with a period.
        if cleaned_data['interval_type'] == 'decimal':
            if l and "," in l:
                l = l.replace(",",".")
            if u and "," in u:
                u = u.replace(",",".")
            if l and not is_number(l):
                raise ValidationError("The lower value must be a number.")
            if u and not is_number(u):
                raise ValidationError("The upper value must be a number.")


        # check for valid integers
        if cleaned_data['interval_type'] == 'int':
            if l and not is_number(l):
                raise ValidationError("The lower value must be a number.")
            if u and not is_number(u):
                raise ValidationError("The upper value must be a number.")

        #TODO: check for valid dates
        #TODO: check for valid dateTimes
        #TODO: check for valid times

        cleaned_data['upper'] = u
        cleaned_data['lower'] = l

        return

    class Meta:
        model = DvInterval
        fields = '__all__'

class ReferenceRangeAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReferenceRangeAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(ReferenceRangeAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = ReferenceRange
        fields = '__all__'

class DvOrdinalAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvOrdinalAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvOrdinalAdminForm, self).clean()
        o = cleaned_data['ordinals']
        # test that the ordinals are really ints
        for n in o:
            try:
                x = int(n)
            except:
                raise ValidationError("You MUST use numbers for the Ordinal indicators. It seems one or more of yours is not.")

        # are the number of symbols and definitions correct?
        symbols = cleaned_data['symbols']
        sym_def = cleaned_data['symbols_def']
        if len(symbols.splitlines()) != len(sym_def.splitlines()):
            if len(sym_def.splitlines()) == 1: # allow one def to be replicated for all enums
                sd = sym_def.splitlines()[0]
                newDefs = []
                for x in range(0,len(symbols.splitlines())):
                    newDefs.append(sd)
                cleaned_data['symbols_def'] = '\n'.join(newDefs)
            else:
                raise ValidationError("The number of 'Symbols' and 'Symbol dfinitions' must be exactly the same. Check for empty lines.")

        return

    class Meta:
        model = DvOrdinal
        fields = '__all__'

class DvCountAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvCountAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvCountAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvCount
        fields = '__all__'


class DvQuantityAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvQuantityAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvQuantityAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = DvQuantity
        fields = '__all__'


class DvRatioAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvRatioAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvRatioAdminForm, self).clean()
        nmini = cleaned_data['num_min_inclusive']
        nmine = cleaned_data['num_min_exclusive']
        nmaxi = cleaned_data['num_max_inclusive']
        nmaxe = cleaned_data['num_max_exclusive']
        dmini = cleaned_data['den_min_inclusive']
        dmine = cleaned_data['den_min_exclusive']
        dmaxi = cleaned_data['den_max_inclusive']
        dmaxe = cleaned_data['den_max_exclusive']

        # tests for proper modelling
        if (nmi and nme) or (nmaxi and nmaxe):
            raise ValidationError("There is ambiguity in your numerator constraints for min/max.")
        if (dmi and dme) or (dmaxi and dmaxe):
            raise ValidationError("There is ambiguity in your denominator constraints for min/max.")



        return

    class Meta:
        model = DvRatio
        fields = '__all__'

class DvTemporalAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DvTemporalAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(DvTemporalAdminForm, self).clean()
        #ony one element can be required and if one is required no others are allowed
        required_set = False
        if cleaned_data['require_date']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_time']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_datetime']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_day']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_month']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_year']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_year_month']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_month_day']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_duration']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_ymduration']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        if cleaned_data['require_dtduration']:
            if not required_set:
                required_set = True
            else:
                raise ValidationError("You cannot require more than one temporal element in one DvTemporal. Check your selections.")

        #only one duration is allowed
        if (cleaned_data['allow_duration'] and cleaned_data['allow_ymduration']) or (cleaned_data['allow_duration'] and cleaned_data['allow_dtduration']) or (cleaned_data['allow_ymduration'] and cleaned_data['allow_dtduration']):
            raise ValidationError("Only one of the duration types are allowed to be selected.")

        # if there is a duration, you cannot have any other temporal elements.
        if (cleaned_data['allow_duration'] or cleaned_data['allow_ymduration'] or cleaned_data['allow_dtduration']) \
           and (cleaned_data['allow_date'] or cleaned_data['allow_time'] or cleaned_data['allow_datetime'] or \
                cleaned_data['allow_day'] or cleaned_data['allow_month'] or cleaned_data['allow_year'] or \
                cleaned_data['allow_year_month'] or cleaned_data['allow_month_day']):
            raise ValidationError("You cannot have a duration mixed with other temporal types.")

        return

    class Meta:
        model = DvTemporal
        fields = '__all__'

class PartyAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartyAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(PartyAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Party
        fields = '__all__'


class AuditAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuditAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(AuditAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Audit
        fields = '__all__'


class AttestationAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttestationAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(AttestationAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Attestation
        fields = '__all__'


class ParticipationAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParticipationAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(ParticipationAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Participation
        fields = '__all__'

class ClusterAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClusterAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(ClusterAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Cluster
        fields = '__all__'

class ConceptAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ConceptAdminForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.published:
            for fld in self.fields:
                self.fields[fld].widget.attrs['readonly'] = True
                self.fields[fld].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super(ConceptAdminForm, self).clean()
        # do something here if needed.

        return

    class Meta:
        model = Concept
        fields = '__all__'













