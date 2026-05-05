from odoo import models, fields, api
from odoo.exceptions import UserError

class TerminalTransaction(models.Model):
    _name = 'terminal.transaction'
    _description = 'Transacción de Terminal Físico'

    # --- CAMPOS PRINCIPALES ---
    name = fields.Char(string='Referencia', required=True, copy=False, default='Nueva')
    date = fields.Datetime(string='Fecha y Hora', default=fields.Datetime.now, required=True)
    amount = fields.Float(string='Monto Total', required=True)
    
    state = fields.Selection([
        ('draft', 'Borrador / Pendiente'),
        ('processed', 'Procesado Contablemente'),
        ('error', 'Error')
    ], string='Estado', default='draft')

    partner_id = fields.Many2one('res.partner', string='Cliente (Comercio)')
    terminal_identifier = fields.Char(string='ID del Terminal')

    # --- CAMPOS CONTABLES ---
    journal_id = fields.Many2one('account.journal', string='Diario Contable', domain=[('type', 'in', ['bank', 'cash'])])
    move_id = fields.Many2one('account.move', string='Asiento Contable', readonly=True)

    # --- 1. GENERACIÓN DE SECUENCIA AUTOMÁTICA ---
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nueva') == 'Nueva':
                vals['name'] = self.env['ir.sequence'].next_by_code('terminal.transaction') or 'Nueva'
        return super().create(vals_list)

    # --- 2. LÓGICA PARA PROCESAR Y CREAR EL ASIENTO ---
    def action_process_transaction(self):
        for record in self:
            if record.amount <= 0:
                raise UserError("Error: El monto debe ser mayor a cero.")
            if not record.partner_id:
                raise UserError("Error: Debes seleccionar un Cliente.")
            if not record.journal_id:
                raise UserError("Error: Debes seleccionar un Diario Contable.")

            # Preparar las líneas del asiento (Débito y Crédito)
            line_ids = [
                (0, 0, {
                    'name': f'Cobro Terminal {record.terminal_identifier or ""}',
                    'account_id': record.journal_id.default_account_id.id,
                    'debit': record.amount,
                    'credit': 0.0,
                    'partner_id': record.partner_id.id,
                }),
                (0, 0, {
                    'name': f'Cobro Terminal {record.terminal_identifier or ""}',
                    'account_id': record.partner_id.property_account_receivable_id.id,
                    'debit': 0.0,
                    'credit': record.amount,
                    'partner_id': record.partner_id.id,
                })
            ]

            # Crear el objeto asiento contable
            move_vals = {
                'journal_id': record.journal_id.id,
                'date': record.date.date(),
                'ref': record.name,
                'line_ids': line_ids,
            }
            
            new_move = self.env['account.move'].create(move_vals)
            new_move.action_post() # Publica el asiento automáticamente
            
            record.move_id = new_move.id
            record.state = 'processed'

    # --- 3. FUNCIÓN PARA EL SMART BUTTON ---
    def action_view_move(self):
        self.ensure_one() 
        return {
            'type': 'ir.actions.act_window',
            'name': 'Asiento Contable',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.move_id.id,
            'target': 'current',
        }