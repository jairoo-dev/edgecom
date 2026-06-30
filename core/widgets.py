from django import forms


class ClienteSelect(forms.Select):
    """
    Select de Cliente que agrega data-razon-social a cada <option>,
    para que la búsqueda en Select2 pueda filtrar también por razón social
    aunque la etiqueta visible sea solo el RFC.

    Usado por cualquier formulario que tenga un ModelChoiceField a Cliente
    (ej. CotizacionForm, FacturaForm).
    """
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        cliente = getattr(value, 'instance', None)
        if cliente is not None:
            option['attrs']['data-razon-social'] = cliente.razon_social
        return option
