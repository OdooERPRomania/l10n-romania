# Copyright  2017 Forest and Biomass Romania
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import Form, common


class TestHREmployeebase(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestHREmployeebase, cls).setUpClass()
        cls.employee_root = cls.env.ref("hr.employee_admin")
        cls.employee_mit = cls.env.ref("hr.employee_mit")
        cls.employee_al = cls.env.ref("hr.employee_al")

        cls.root_ppso = cls.env.ref("l10n_ro_hr.root_ppso")
        cls.root_ppsp = cls.env.ref("l10n_ro_hr.root_ppsp")
        cls.al_also1 = cls.env.ref("l10n_ro_hr.al_also1")
        cls.al_also2 = cls.env.ref("l10n_ro_hr.al_also1")
        cls.al_alsp = cls.env.ref("l10n_ro_hr.al_also1")


class TestEmployeeRelated(TestHREmployeebase):
    def test_person_related_validation(self):
        # Test ssnid validation
        with self.assertRaises(Exception):
            self.root_ppso.ssnid = "1980511469378"
        # Test relation validation
        with self.assertRaises(Exception):
            self.root_ppso.relation = "coinsured"

    def test_employee_related(self):
        # Test employee related calculation
        self.root_ppsp.relation_type = "both"
        self.assertEqual(self.employee_root.person_in_care, 2)

    def test_onchange_ssnid(self):
        """ Check onchange ssnid."""
        # Test onchange from ANAF
        employee_form = Form(self.employee_root)
        employee_form.ssnid = "1701224378225"
        self.assertEqual(employee_form.gender, "male")
        self.assertEqual(employee_form.birthday.strftime("%Y-%m-%d"), "1970-12-24")
        self.assertEqual(employee_form.place_of_birth, "Vaslui")
