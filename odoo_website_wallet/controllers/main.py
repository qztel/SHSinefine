# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import http, SUPERUSER_ID
from odoo import _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing


class WebsiteWallet(http.Controller):

	@http.route(['/wallet'], type='http', auth="public", website=True)
	def wallet_balance(self, **post):
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		partner = request.env.user.partner_id
		company_currency = request.website.company_id.currency_id
		web_currency = request.website.get_current_pricelist().currency_id
		price = float(partner.wallet_balance)
		if company_currency.id != web_currency.id:
			new_rate = (price * web_currency.rate) / company_currency.rate
			price = round(new_rate, 2)
		return request.render("odoo_website_wallet.wallet_balance", {'wallet': price})

	@http.route(['/add/wallet/balance'], type='http', auth="public", website=True)
	def add_wallet_balance(self, **post):
		cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
		return request.render("odoo_website_wallet.add_wallet_balance")

	@http.route(['/wallet/balance/confirm'], type='http', auth="public", website=True)
	def wallet_balance_confirm(self, **post):

		product = request.website.wallet_product_id
		if product:
			product_id = product.id
			prd_price = 0
			company_currency = request.website.company_id.currency_id
			web_currency = request.website.get_current_pricelist().currency_id
			if company_currency.id != web_currency.id:
				amount = post['amount']
				amount_replace = amount.replace(',', '')
				price = float(amount_replace)
				new_rate = (price * company_currency.rate) / web_currency.rate
				prd_price = new_rate
			else:
				amount = post['amount']
				amount_replace = amount.replace(',', '')
				prd_price = float(amount_replace)
			order = request.website.sale_get_order(force_create=1)
			request.env['sale.order.line'].sudo().create({
				"order_id": order.id,
				"product_id": product_id,
				"product_uom_qty": 1,
				"price_unit": prd_price,
				"line_wallet_amount": prd_price,
			})
			return request.redirect("/shop/cart")
		else:
			return request.render("odoo_website_wallet.wallet_product_error")

	@http.route('/shop/payment/wallet', type='json', auth="public", methods=['POST'], website=True)
	def wallet(self, wallet, **post):
		cr, uid, context = request.cr, request.uid, request.context
		order = request.website.sale_get_order()
		wallet_product_id = request.website.wallet_product_id.id
		if wallet:
			wallet_order_line = order.order_line.filtered(lambda l: l.product_id.id == wallet_product_id)
			order.write({
				'is_wallet': False,
				'order_line': [(2, wallet_order_line.id, 0)],
			})
		if wallet == False:
			order.write({'is_wallet': True})
			web_currency = request.website.get_current_pricelist().currency_id
			wallet_balance = request.website.get_wallet_balance(web_currency)
			if wallet_balance >= order.amount_total:
				order.write({
					'order_line': [(0, 0, {
						'product_id': wallet_product_id,
						'product_uom_qty': 1,
						'price_unit': -order.amount_total
					})]
				})

			if order.amount_total > wallet_balance:
				deduct_amount = order.amount_total - wallet_balance
				order.write({
					'order_line': [(0, 0, {
						'product_id': wallet_product_id,
						'product_uom_qty': 1,
						'price_unit': -deduct_amount
					})]
				})
		return True


class WebsiteWalletPayment(WebsiteSale):

	@http.route(['/shop/cart'], type='http', auth="public", website=True)
	def cart(self, access_token=None, revive='', **post):
		order = request.website.sale_get_order()
		if order:
			if order.is_wallet == True:
				order.write({'is_wallet': False})
		return super(WebsiteWalletPayment, self).cart(**post)

	@http.route(['/shop/confirm_order'], type='http', auth="public", website=True)
	def confirm_order(self, **post):
		order = request.website.sale_get_order()
		if order:
			if order.is_wallet == True:
				order.write({'is_wallet': False})
		return super(WebsiteWalletPayment, self).confirm_order(**post)

	@http.route('/shop/payment/validate', type='http', auth="public", website=True)
	def shop_payment_validate(self, transaction_id=None, sale_order_id=None, **post):
		""" Method that should be called by the server when receiving an update
        for a transaction. State at this point :

         - UDPATE ME
        """
		if sale_order_id is None:
			order = request.website.sale_get_order()
		else:
			order = request.env['sale.order'].sudo().browse(sale_order_id)
			assert order.id == request.session.get('sale_last_order_id')

		if transaction_id:
			tx = request.env['payment.transaction'].sudo().browse(transaction_id)
			assert tx in order.transaction_ids()
		elif order:
			tx = order.get_portal_last_transaction()
		else:
			tx = None

		if not order or (order.amount_total and not tx):
			return request.redirect('/my/home')

		if order and not order.amount_total and not tx:
			order.with_context(send_email=True).action_confirm()
			return request.redirect(order.get_portal_url())

		# clean context and session, then redirect to the confirmation page
		request.website.sale_reset()
		if tx and tx.state == 'draft':
			return request.redirect('/my/home')

		PaymentPostProcessing.remove_transactions(tx)
		return request.redirect('/shop/confirmation')

	@http.route(['/shop/confirmation'], type='http', auth="public", website=True)
	def shop_payment_confirmation(self, **post):
		sale_order_id = request.session.get('sale_last_order_id')
		wallet_product_id = request.website.wallet_product_id.id
		if sale_order_id:
			order = request.env['sale.order'].sudo().browse(sale_order_id)
			if order.is_wallet == True:

				order.state = 'draft'
				# 删除明细行
				wallet_order_line = order.order_line.filtered(lambda l: l.product_id.id == wallet_product_id)
				order.write({
					'order_line': [(2, wallet_order_line.id, 0)],
				})
				order.state = 'sale'

				wallet_obj = request.env['website.wallet.transaction']
				partner = request.env['res.partner'].search([('id','=',order.partner_id.id)])
				wallet_balance = order.partner_id.wallet_balance
				amount_total = (order.amount_untaxed + order.amount_tax)

				company_currency = request.website.company_id.currency_id
				web_currency = order.pricelist_id.currency_id
				price = float(amount_total)

				if company_currency.id != web_currency.id:
					new_rate = (price*company_currency.rate)/web_currency.rate
					price = round(new_rate,2)

				wallet_create = wallet_obj.sudo().create({
					'wallet_type': 'debit',
					'partner_id': order.partner_id.id,
					'sale_order_id': order.id,
					'reference': 'sale_order',
					'amount': price,
					'currency_id': company_currency.id,
					'status': 'done'
				})

				if wallet_balance >= price:
					amount = wallet_balance - price
					order.write({'wallet_used':float(amount_total),'wallet_transaction_id':wallet_create.id })
					partner.sudo().write({'wallet_balance':amount})

				if price > wallet_balance:
					p_wlt = request.website.get_wallet_balance(web_currency)
					order.write({'wallet_used':p_wlt,'wallet_transaction_id':wallet_create.id})
					partner.sudo().write({'wallet_balance':0.0})
					order.wallet_transaction_id.update({'amount':p_wlt})
				wallet_create.wallet_transaction_email_send()

				return request.render("website_sale.confirmation", {'order': order})
			else:
				return super(WebsiteWalletPayment, self).shop_payment_confirmation(**post)
		return super(WebsiteWalletPayment, self).shop_payment_confirmation(**post)


class CustomerPortalWalletTransaction(CustomerPortal):

	def _prepare_portal_layout_values(self):
		values = super(CustomerPortalWalletTransaction, self)._prepare_portal_layout_values()
		partner = request.env.user.partner_id
		WalletTransaction = request.env['website.wallet.transaction'].sudo()
		wallet_count = WalletTransaction.sudo().search_count([
			('partner_id', '=', partner.id)])
		values.update({
			'wallet_count': wallet_count,
		})
		return values

	@http.route(['/my/wallet-transactions', '/my/quotes/page/<int:page>'], type='http', auth="user", website=True)
	def portal_my_wallet_transaction(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
		values = self._prepare_portal_layout_values()
		partner = request.env.user.partner_id
		WalletTransaction = request.env['website.wallet.transaction'].sudo()
		domain = [
			('partner_id', '=', partner.id)]

		searchbar_sortings = {
			'id': {'label': _('Wallet Transactions'), 'order': 'id desc'},

		}
		if not sortby:
			sortby = 'id'
		sort_wallet_transaction = searchbar_sortings[sortby]['order']
		# count for pager
		wallet_count = WalletTransaction.sudo().search_count(domain)
		# make pager
		pager = portal_pager(
			url="/my/wallet-transactions",
			total=wallet_count,
			page=page,
			step=self._items_per_page
		)
		# search the count to display, according to the pager data
		wallets = WalletTransaction.sudo().search(domain, order=sort_wallet_transaction, limit=self._items_per_page,
												  offset=pager['offset'])
		request.session['my_wallet_transaction_history'] = wallets.ids[:100]
		values.update({
			'wallets': wallets.sudo(),
			'page_name': 'wallet',
			'pager': pager,
			'default_url': '/my/subcontractor-job-order',
		})
		return request.render("odoo_website_wallet.portal_my_wallet_transactions", values)
