# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.osv import expression
from odoo.addons.website_sale.controllers.main import WebsiteSale

class ProductVisibilityController(WebsiteSale):

    def _get_visibility_domain(self):
        """
        Determines the exclusion domain based on user type (guest or logged-in)
        and their visibility settings.

        Returns:
            list: An Odoo domain to be added to the main search.
        """
        is_public_user = request.website.is_public_user()
        config_sudo = request.env['ir.config_parameter'].sudo()

        if is_public_user:
            # Guest User: Read settings from ir.config_parameter
            if not config_sudo.get_param('product_visibility_guest_user', 'False') == 'True':
                return []

            mode = config_sudo.get_param('filter_mode')
            # Use literal_eval to safely evaluate the string representation of the list
            try:
                product_ids = eval(config_sudo.get_param('website_product_visibility.available_product_ids', '[]'))
                categ_ids = eval(config_sudo.get_param('website_product_visibility.available_cat_ids', '[]'))
                brand_ids = eval(config_sudo.get_param('website_product_visibility.available_brand_ids', '[]'))
            except (ValueError, SyntaxError):
                product_ids, categ_ids, brand_ids = [], [], []

        else:
            # Logged-in User: Read settings from the partner record
            partner = request.env.user.partner_id
            mode = partner.filter_mode
            product_ids = partner.website_available_product_ids.ids
            categ_ids = partner.website_available_cat_ids.ids
            brand_ids = partner.website_available_brand_ids.ids

        if not mode or mode == 'null':
            return []

        # Build the exclusion domain based on the selected mode
        exclusion_domain = []
        if mode in ['product_only', 'product_and_categ', 'product_and_brand', 'product_categ_and_brand'] and product_ids:
            exclusion_domain.append(('id', 'not in', product_ids))

        if mode in ['categ_only', 'product_and_categ', 'categ_and_brand', 'product_categ_and_brand'] and categ_ids:
            # We must filter products that are in any of the child categories as well
            all_child_categs = request.env['product.public.category'].search([('id', 'child_of', categ_ids)])
            if all_child_categs:
                exclusion_domain.append(('public_categ_ids', 'not in', all_child_categs.ids))

        if mode in ['brand_only', 'product_and_brand', 'categ_and_brand', 'product_categ_and_brand'] and brand_ids:
            exclusion_domain.append(('product_brand_id', 'not in', brand_ids))
            
        return exclusion_domain

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        """
        Overrides the base search domain to add product visibility rules.
        """
        # 1. Get the original domain from Odoo's logic
        base_domain = super()._get_search_domain(
            search, category, attrib_values, search_in_description=search_in_description
        )

        # 2. Get the visibility exclusion domain
        visibility_domain = self._get_visibility_domain()

        # 3. If there's a visibility domain, combine it with the base domain
        if visibility_domain:
            return expression.AND([base_domain, visibility_domain])
        
        return base_domain
