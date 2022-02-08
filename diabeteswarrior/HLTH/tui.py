#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Text user interface for health records."""

import __init__ as Health
from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.shortcuts import button_dialog,input_dialog,radiolist_dialog,yes_no_dialog
import arrow as A

def main() -> str:
    """For isolation"""
    r_s = "Something went wrong, please check the data and backup files then try again."
    po_pulse = int(input_dialog(title=HTML("Pulseoximeter Pulse"), text=Health.MODULE_HELP['po']).run())
    spox = int(input_dialog(title=HTML("Pulseoximeter Oxygen Saturation"), text=Health.MODULE_HELP['spox']).run())
    weight = float(input_dialog(title=HTML("Scale Weight"), text=Health.MODULE_HELP['weight']).run())
    fat = float(input_dialog(title=HTML("Scale Fat%"),text=Health.MODULE_HELP['fat']).run())
    pulse = int(input_dialog(title=HTML("Blood Pressure Cuff Pulse"), text=Health.MODULE_HELP['pulse']).run())
    systolic = int(input_dialog(title=HTML("Blood Pressure Cuff Systolic Pressure"), text=Health.MODULE_HELP['systolic']).run())
    diastolic = int(input_dialog(title=HTML("Blood Pressure Cuff Diastolic Pressure"), text=Health.MODULE_HELP['diastolic']).run())
    ihb = button_dialog(title=HTML("Blood Pressure Cuff Irregular Heart Beat"),text=Health.MODULE_HELP['ihb'],buttons=[("Yes",1),("No",0)]).run()
    hypertension = radiolist_dialog(title=HTML("Blood Pressure Cuff Hypertension Stage"),text=Health.MODULE_HELP['hypertension'],values=[(0,"None"),(1,"Pre"),(2,"I"),(3,"II")]).run()
    temperature = float(input_dialog(title=HTML("Temperature"),text=Health.MODULE_HELP['temperature']).run())

    record = {
        "po_pulse": po_pulse,
        "spox": spox,
        "weight": weight,
        "fat": fat,
        "pulse": pulse,
        "systolic": systolic,
        "diastolic": diastolic,
        "ihb": ihb,
        "hypertension": hypertension,
        "temperature": temperature,
        "t_s": A.now().format("YYYY-MM-DD HH:mm")
    }

    formatted_text = FormattedText([("italic",f"Pulse:{po_pulse}\n"),("italic",f"SPoX:{spox}\n"),("italic",f"Weight:{weight}\n"),("italic",f"Fat:{fat}\n"),("italic",f"Pulse: {pulse}\n"),("italic",f"Systolic:{systolic}\n"),("italic",f"Diastolic:{diastolic}\n"),("italic",f"IHB:{ihb}\n"),("italic",f"Hypertension:{hypertension}\n"),("italic", f"temperature:{temperature}\n")])

    if _ := yes_no_dialog(title=HTML("Is this correct?"), text=formatted_text).run():
        commit_rollback = "_"
        h_r = Health.Records(**record).record_add()
        if h_r > 0:
            commit_rollback = button_dialog(title=HTML("Commit or Delete the new record."),text=HTML("Click on <u>Commit</u> and the data will be stored and backed up, <u>Rollback</u> to delete the last record or <u>exit</u> to leave the data without backing up the database."),buttons=[("Commit","commit"),("Rollback","rollback"),("Exit","_")]).run()
        if commit_rollback == 'commit':
            Health.Records.records_backup_restore('c')
            r_s = str(h_r)
        elif commit_rollback == 'rollback':
            Health.Records.records_backup_restore('d')
            r_s = str(h_r)
    return r_s

if __name__ == '__main__':
    print(main())
