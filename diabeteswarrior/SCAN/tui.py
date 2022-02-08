#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Text User Interface for SCAN records."""

import arrow as A
from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.shortcuts import button_dialog, input_dialog, radiolist_dialog, yes_no_dialog

import __init__ as Scan


def main():
    r_s = "Something went wrong, please check the data and backup files then try again."
    message = radiolist_dialog(
        title=HTML("Abbot FreeStyle Libre 2 Messages"),
        text=HTML(Scan.MODULE_HELP['message']),
        values=[(-3,"Glucose Low"),(-2,"Glucose Going Low"),(-1,"My Low Alert"),
                (0,"None"),
                (1,"My High Alert"),(2,"Glucose Going High"),(3,"Glucose High")]).run()
    notes = input_dialog(
        title=HTML("Notes"),
        text=HTML(Scan.MODULE_HELP['notes'])
    ).run()
    bolus_u = int(input_dialog(
        title=HTML("Bolus Insulin"),
        text=HTML(Scan.MODULE_HELP['bolus_u'])
    ).run())
    basal_u = int(input_dialog(
        title=HTML("Basal Insulin"),
        text=HTML(Scan.MODULE_HELP['basal_u'])
    ).run())
    carbohydrate = int(input_dialog(
        title=HTML('Carbohydrates'),
        text=HTML(Scan.MODULE_HELP['carbohydrate'])
    ).run())
    exercise = button_dialog(
        title=HTML("Exercise Event"),
        text=HTML(Scan.MODULE_HELP['exercise']),
        buttons=[("Yes",True),("No",False)]
    ).run()
    medication = button_dialog(
        title=HTML("Medication"),
        text=HTML(Scan.MODULE_HELP['medication']),
        buttons=[("Yes",True),("No",False)]
    ).run()
    glucose = int(input_dialog(
        title=HTML("Glucose"),
        text=HTML(Scan.MODULE_HELP['glucose'])
    ).run())
    trend = radiolist_dialog(
        title=HTML('Trend'),
        text=HTML(Scan.MODULE_HELP['trend']),
        values=[(-2,"The Arrow Is Pointing Down"),
                (-1,"The Arrow Is Pointing Down And Right"),
                (0,"The Arrow Is Point To The Right"),
                (1,"The Arrow Is Pointing Up And Right"),
                (2,"The Arrow Is Point Up")]).run()

    record = {"message": message,
        "notes": notes,
        "bolus_u": bolus_u,
        "basal_u": basal_u,
        "carbohydrate": carbohydrate,
        "exercise": exercise,
        "medication": medication,
        "glucose": glucose,
        "trend": trend,
        't_s': A.now().format("YYYY-MM-DD HH:mm")}

    formatted_text = FormattedText([("italic",F"Message: {message}\n"),("italic",F"Notes: {notes}\n"),("italic",F"Bolus Insulin: {bolus_u}\n"),
        ("italic",F"Basal Insulin: {basal_u}\n"),("italic",F"Carbohydrates: {carbohydrate}\n"),("italic",F"Exercise: {exercise}\n"),
        ("italic",F"Medication {medication}\n"),("italic",F"Glucose {glucose}\n"),("italic",F"Trend {trend}\n")])

    if correct := yes_no_dialog(title=HTML("Is this correct?"),text=formatted_text).run():
        commit_rollback = "_"
        h_r = Scan.Records(**record).record_add()
        if h_r > 0:
            commit_rollback = button_dialog(title=HTML("Commit or Delete the new record."),text=HTML("Click on <u>Commit</u> and the data will be stored and backed up, <u>Rollback</u> to delete the last record or <u>exit</u> to leave the data without backing up the database."),buttons=[("Commit","commit"),("Rollback","rollback"),("Exit","_")]).run()
        if commit_rollback == 'commit':
            Scan.Records.records_backup_restore('c')
            r_s = str(h_r)
        elif commit_rollback == 'rollback':
            Scan.Records.records_backup_restore('d')
            r_s = str(h_r)
    return r_s

if __name__ == '__main__':
    print(main())
