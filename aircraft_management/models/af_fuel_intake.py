# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class FuelIntake(models.Model):
    _name = 'aircraft.fuel.intake'
    _description = 'Aircraft Fuel Intake'
    _rec_name = 'date'

    state = fields.Selection([
        ('draft', 'Draft'),('pending','Pending Approval'),('approved','Aproved')
        ],string="State",default="draft")
    amount_of_fuel = fields.Integer('Amount of Fuel Purchased(Liters)')
    amount_of_fuel_pounds = fields.Char(compute="_compute_amount_of_fuel_in_pounds",
                                        string="Amount Of Fuel In Pounds",store=True)
    currency_id = fields.Many2one('res.currency',string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    price_per_liter = fields.Monetary("Price Per Litre")
    calculate_amount = fields.Monetary(compute="_calculate_amount", string="Calculated Amount",store=True)
    date = fields.Date(default=fields.Date.today())


    @api.depends('amount_of_fuel')
    def _compute_amount_of_fuel_in_pounds(self):
        for rec in self:
            pounds = 2.2
            lb = rec.amount_of_fuel * pounds
            format_lb = f"{lb} lb"
            rec.amount_of_fuel_pounds = format_lb
    
    @api.depends('price_per_liter')
    def _calculate_amount(self):
        for rec in self:
            rec.calculate_amount = rec.price_per_liter * rec.amount_of_fuel

    
    def action_submit(self):
        self.write({"state": "pending"})

    def action_approve(self):
        self.write({"state":"approved"})