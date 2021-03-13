# © 2021 Florian Kantelberg - initOS GmbH
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime, timedelta
from uuid import uuid4

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class VaultInbox(models.Model):
    _name = "vault.inbox"
    _description = _("Vault share incoming secrets")

    def _default_expiration(self):
        return datetime.now() + timedelta(days=7)

    @api.depends("token")
    def _compute_inbox_link(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for rec in self:
            rec.inbox_link = f"{base_url}/vault/inbox/{rec.token}"

    token = fields.Char(default=lambda self: uuid4(), readonly=True)
    inbox_link = fields.Char(
        compute=_compute_inbox_link,
        readonly=True,
        help="Using this link you can write to the current inbox. If you want people "
        "to create new inboxes you should give them your inbox link from your key "
        "management.",
    )
    user_id = fields.Many2one("res.users", "Vault", required=True)
    name = fields.Char(required=True)
    secret = fields.Char(readonly=True)
    filename = fields.Char()
    secret_file = fields.Binary(attachment=False, readonly=True)
    key = fields.Char(required=True)
    iv = fields.Char(required=True)
    accesses = fields.Integer(
        "Access counter",
        default=1,
        help="If this is 0 the inbox will be read-only for the owner.",
    )
    expiration = fields.Datetime(
        default=_default_expiration,
        help="If expired the inbox will be read-only for the owner.",
    )

    _sql_constraints = [
        (
            "value_check",
            "CHECK(secret IS NOT NULL OR secret_file IS NOT NULL)",
            _("No value found"),
        ),
    ]

    def read(self, *args, **kwargs):
        # Always load the binary instead of the size
        return super(VaultInbox, self.with_context(bin_size=False)).read(
            *args, **kwargs
        )

    @api.model
    def find_inbox(self, token):
        return self.search([("token", "=", token)])

    def store_in_inbox(self, name, secret, secret_file, iv, key, user, filename):
        if len(self) == 0:
            return self.create(
                {
                    "name": name,
                    "accesses": 0,
                    "iv": iv,
                    "key": key,
                    "secret": secret or None,
                    "secret_file": secret_file or None,
                    "filename": filename,
                    "user_id": user.id,
                }
            )

        if self.accesses > 0 and datetime.now() < self.expiration:
            self.write(
                {
                    "accesses": self.accesses - 1,
                    "iv": iv,
                    "key": key,
                    "secret": secret or None,
                    "secret_file": secret_file or None,
                    "filename": filename,
                }
            )
            return self
