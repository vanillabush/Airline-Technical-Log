# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class TechnicalLog(models.Model):
    _name = 'aircraft.technical.log'
    _description = 'Aircraft Technical Log'

    name = fields.Char("Log Name")
    date = fields.Date(default=fields.Date.today(),string="Date Captured")
    aircraft_detail_id = fields.Many2one("aircraft.details",string="Aircraft Details")
    captured_by = fields.Many2one('res.users', default=lambda self: self.env.user.id)
    leg_ids = fields.One2many('aircraft.leg','technical_log_id','Leg')
    crew_ids = fields.One2many('aircraft.crew','technical_log_id', 'Crew')
    engine_usage_ids = fields.One2many('aircraft.engine.usage','technical_log_id', 'Engine Usage')
    manifest_ids = fields.One2many('aircraft.leg.manifest','technical_log_id', 'Manifest')


class TechnicalLogLeg(models.Model):
    _name = 'aircraft.leg'
    _description = 'Leg'
    _rec_name = "leg"

    technical_log_id = fields.Many2one('aircraft.technical.log')
    leg = fields.Selection([
        ("leg 1", "Leg 1"),
        ("leg 2", "Leg 2"),
        ("leg 3", "Leg 3"),
        ("leg 4", "Leg 4"),
        ("leg 5", "Leg 5"),
        ("leg 6", "Leg 6"),
    ],string="Leg")
    flight_no = fields.Char("Flight No.")
    point_of_departure = fields.Char('Point of Depature')
    destination = fields.Char('Destination')
    nautical_miles = fields.Float('Nautical Miles')
    passengers = fields.Integer('Passengers')
    hobbs_time_start = fields.Datetime('Hobbs Time Start')
    hobbs_time_end = fields.Datetime('Hobbs TIme End')
    off_chock_time = fields.Datetime('Off Chock Time')
    on_chock_time = fields.Datetime('On Chock Time')
    chock_to_chock_time = fields.Datetime('Chock to Chock Time')
    total_fuel_before = fields.Integer("Total Fuel Before")
    total_fuel_before_to_lb = fields.Char(compute="_compute_total_fuel_before_to_lb",string="Total Fuel Before(lb)")
    total_fuel_after = fields.Integer("Total Fuel After")
    total_fuel_after_to_lb = fields.Char(compute="_compute_total_fuel_after_to_lb",string="Total Fuel After(lb)")
    fuel_uplift = fields.Char("Fuel Uplift")
    fuel_type = fields.Char("Fuel Type")
    supplier = fields.Char("Supplier")
    receipt_no = fields.Char("Reciept no")
    apu_hrs = fields.Char("APU hrs")
    oil_uplift_lr = fields.Char("Oil Uplift l/r")
    hydraulic_uplift = fields.Char("Hydrulic Uplift")

    @api.depends('total_fuel_before')
    def _compute_total_fuel_before_to_lb(self):
        for rec in self:
            pounds = 2.2
            lb = rec.total_fuel_before * pounds
            format_lb = f"{lb} lb"
            rec.total_fuel_before_to_lb  = format_lb

    @api.depends('total_fuel_after')
    def _compute_total_fuel_after_to_lb(self):
        for rec in self:
            pounds = 2.2
            lb = rec.total_fuel_after * pounds
            format_lb = f"{lb} lb"
            rec.total_fuel_after_to_lb  = format_lb



class TechnicalLogFlightDetails(models.Model):
    _name = 'aircraft.details'
    _description = "Flight Details"
    _rec_name = "registration"

    registration = fields.Char("Registration")
    aircraft_type = fields.Char("Type")
    serial_no = fields.Char("Serial Number")
    flight_date = fields.Date("Date")
    next_inspection_type = fields.Char("Next Inspection Time")
    next_inspection_date = fields.Datetime("Next Inspection Date")
    airframe_hrs_start = fields.Datetime("Airframe HRS Start")    
    airframe_hrs_end = fields.Datetime("Airframe HRS End") 
    flight_time = fields.Datetime("Flight Time")
    hobbs_start = fields.Datetime("Hobbs Start")   
    hobbs_end = fields.Datetime("Hobbs End")
    defect_ids = fields.One2many("aircraft.defect","aircraft_details_id","Defects")

class TechnicalFlightDetailsCrew(models.Model):
    _name = 'aircraft.crew'
    _description = "Aircraft Crew"
    _rec_name = "crew_type"

    crew_type = fields.Selection([("PIC", "PIC"),("co-pilot","Co-Pilot"),("cabin crew","Cabin Crew")],string="Crew Type")
    partner_id = fields.Many2one('res.partner',string="Crew")
    sign_on_time = fields.Datetime("Sign-On Time")
    sign_off_time = fields.Datetime("Sign-Off Time")
    flight_duty_time = fields.Datetime("Flight Duty Time")
    licence_no = fields.Char('Licence No')
    technical_log_id = fields.Many2one('aircraft.technical.log')

class TechnicalFlightDetailsDefect(models.Model):
    _name = "aircraft.defect"
    _description = "Aircraft Defects"
    _rec_name = "defect"

    defect = fields.Text("Defects")
    action_taken = fields.Text("Action Taken")
    authorization_no = fields.Char("Authorization Number")
    date = fields.Date(default=fields.Date.today(),string="Date")
    aircraft_details_id = fields.Many2one("aircraft.details", string="Aircraft Detail")

class TechnicalFlightDetailsEngine(models.Model):
    _name = "aircraft.engine.usage"
    _description = "Aircraft Engine Usage"
    _rec_name = "start"

    engine = fields.Selection([("engine 1","Engine 1"),("engine 2","Engine 2")],string="Engine")
    engine_hr = fields.Integer("Engine Hour")
    engine_hr_amount = fields.Char(compute="_compute_engine_hr_amt",string="Amount")
    n1_prop_rpm = fields.Char("N1/Prop RPM")
    n2_ng = fields.Char("N2/Ng")
    start = fields.Char("Start")
    this_log = fields.Char("This Log")
    end = fields.Char("End")
    l_r_engine = fields.Selection([("l engine","L Engine"),("r engine","R Engine")])
    landings = fields.Char("Landings")
    itt = fields.Char("Itt")
    torque = fields.Char("Torque")
    fuel_flow = fields.Char("Fuel Flow")
    oil_temp_press = fields.Char("Oil/Temp/Press")
    generator_load = fields.Char("Generator Load")
    start_temp = fields.Char("Start Temp")
    dor_items = fields.Char("Dor Items")
    col_items = fields.Char("Col Items")
    technical_log_id = fields.Many2one('aircraft.technical.log')


    @api.depends('engine_hr')
    def _compute_engine_hr_amt(self):
        for rec in self:
            charge = 100
            rate = rec.engine_hr * charge
            rec.engine_hr_amount = f"${rate}"

class TechnicalFlightDetailsManifest(models.Model):
    _name = 'aircraft.leg.manifest'
    _description = 'Leg Manifest'
    _rec_name = "partner_id"

    partner_id = fields.Many2one('res.partner')
    technical_log_id = fields.Many2one('aircraft.technical.log')