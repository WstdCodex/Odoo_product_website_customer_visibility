# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2021-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Neeraj Krishnan V M(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from ast import literal_eval
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    """Inherit Product Template to add filter mode for website users"""

    @api.model
    def _search_fetch(self, search_detail, search, limit, order):
        results, count = super(ProductTemplate, self)._search_fetch(
            search_detail, search, limit, order)
        user = self.env.user
        filter_mode = self.env['ir.config_parameter'].sudo().get_param(
            'filter_mode')
        if user._is_public():
            category = literal_eval(
                self.env['ir.config_parameter'].sudo().get_param(
                    'website_product_visibility.available_cat_ids', '[]'))
            products = literal_eval(
                self.env['ir.config_parameter'].sudo().get_param(
                    'website_product_visibility.available_product_ids', '[]'))
            if filter_mode in ['categ_only', 'product_and_categ']:
                results = results.filtered(
                    lambda r: not any(item in r.public_categ_ids.ids for item in category))
            if filter_mode in ['product_only', 'product_and_categ']:
                results = results.filtered(lambda r: r.id not in products)
        else:
            partner = user.partner_id
            if partner.filter_mode in ['categ_only', 'product_and_categ']:
                category = partner.website_available_cat_ids.ids
                results = results.filtered(
                    lambda r: not any(item in r.public_categ_ids.ids for item in category))
            if partner.filter_mode in ['product_only', 'product_and_categ']:
                products = partner.website_available_product_ids.ids
                results = results.filtered(lambda r: r.id not in products)
        return results, len(results)
