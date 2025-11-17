# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleVisibility(WebsiteSale):
    def _get_customer_visibility_domain(self):
        partner = request.env.user.partner_id if request.env.user else None
        return request.env["product.template"]._get_website_customer_visibility_domain(partner)

    def _get_search_domain(self, search, category, attrib_values):
        domain = super()._get_search_domain(search, category, attrib_values)
        if request.context.get("_disable_customer_visibility"):
            return domain
        return http.AND([domain, self._get_customer_visibility_domain()])

    def _shop_lookup_products(self, term, options=None, limit=5):
        results = super()._shop_lookup_products(term, options=options, limit=limit)
        if request.context.get("_disable_customer_visibility") or not results:
            return results

        visibility_domain = self._get_customer_visibility_domain()
        product_ids = [product.get("id") for product in results if product.get("id")]
        allowed_products = request.env["product.template"].sudo().search(
            http.AND([["id", "in", product_ids], visibility_domain])
        )
        allowed_ids = set(allowed_products.ids)
        return [product for product in results if product.get("id") in allowed_ids]
