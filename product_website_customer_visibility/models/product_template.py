# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    visible_for_all_customers = fields.Boolean(
        string="Visible para todos los clientes",
        default=True,
        help="Si se activa, el producto es visible en el sitio web para cualquier cliente."
        " Si se desactiva, solo los clientes seleccionados podrán verlo.",
    )
    allowed_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Clientes permitidos",
        help="Clientes que pueden ver y comprar este producto en el sitio web cuando no es visible para todos.",
    )

    @api.model
    def _get_website_customer_visibility_domain(self, partner):
        """Domain to restrict website products based on customer visibility.

        This domain keeps standard website restrictions untouched and only
        appends additional conditions for customer-based visibility.
        """
        if not partner:
            # No partner (public/anonymous). Only allow products marked as visible for all.
            return [("visible_for_all_customers", "=", True)]
        return [
            "|",
            ("visible_for_all_customers", "=", True),
            ("allowed_partner_ids", "in", partner.id),
        ]
