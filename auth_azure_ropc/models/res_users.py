# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.exceptions import AccessDenied


class ResUsers(models.Model):

    _inherit = "res.users"

    def _check_credentials(self, password, env):
        try:
            return super(ResUsers, self)._check_credentials(password, env)
        except AccessDenied:
            passwd_allowed = (
                env["interactive"] or not self.env.user._rpc_api_keys_only()
            )
            if passwd_allowed and self.env.user.active:
                ropc_providers = self.env["azure.ropc.provider"].sudo().search([])
                for conf in ropc_providers:
                    if conf._authenticate(self.env.user.login, password):
                        return
            raise
