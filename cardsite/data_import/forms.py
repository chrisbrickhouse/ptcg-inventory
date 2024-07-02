from django import forms

class TabularLoaderForm( forms.Form ):
    tabular_file = forms.FileField(
            label = 'Inventory File',
        )
    sheet_name = forms.ChoiceField(
            label = 'Sheet name',
            help_text = 'Which sheet should be used?'
        )
    cardname_col = forms.ChoiceField(
            label = 'Card column',
            help_text = 'Column with name of cards',
        )
    quantity_col = forms.ChoiceField(
            label = 'Quantity column',
            help_text = 'Column with number of cards',
        )
    location_col = forms.ChoiceField(
            label = 'Location column',
            help_text = 'Column with names of inventory locations',
        )
