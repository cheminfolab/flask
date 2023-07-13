from barcode.ean import EuropeanArticleNumber13 as BarcodeClass
from django.utils.html import mark_safe


class Barcode(BarcodeClass):
    """EAN13 standard numeric barcode"""

    @property
    def bars(self):
        """Barcode rendered as SVG (code displayed)."""
        return mark_safe(self.render(text=False).decode('utf-8'))

    @property
    def barcode(self):
        """Barcode rendered as SVG (code displayed)."""
        return mark_safe(self.render().decode('utf-8'))
