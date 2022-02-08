#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Text User Interface To The Food Database."""

import arrow as A
from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.shortcuts import button_dialog, input_dialog, yes_no_dialog

import __init__ as Food


def main():
    r_s = "Something went wrong, please check the data and backup files then try again"

    domain = input_dialog(
        title=HTML("Domain of Food"),
        text=HTML(Food.MODULE_HELP['domain'])
    ).run()
    name = input_dialog(
        title=HTML("Name of Food"),
        text=HTML(Food.MODULE_HELP['name'])
        ).run()
    portion = input_dialog(
        title=HTML("Portions of Food"),
        text=HTML(Food.MODULE_HELP['portion'])
        ).run()
    # todo: Add a menu of standard measures
    unit = input_dialog(
        title=HTML("Unit the Food is measured in."),
        text=HTML(Food.MODULE_HELP['unit'])
        ).run()
    calories = int(input_dialog(
        title=HTML("Calories of the Food"),
        text=HTML(Food.MODULE_HELP['calories'])
        ).run())
    fat = int(input_dialog(
        title=HTML("Fat content of the Food (default in grams)"),
        text=HTML(Food.MODULE_HELP['fat'])
        ).run())
    cholesterol = int(input_dialog(
        title=HTML("Cholesterol of the Food (default in milligrams)"),
        text=HTML(Food.MODULE_HELP['cholesterol'])
        ).run())
    sodium = int(input_dialog(
        title=HTML("Sodium of the Food (default in milligrams)"),
        text=HTML(Food.MODULE_HELP['sodium'])
        ).run())
    carbohydrate = int(input_dialog(
        title=HTML("Carbohydrate of the Food (default in grams)"),
        text=HTML(Food.MODULE_HELP['carbohydrate'])
        ).run())
    protein = int(input_dialog(
        title=HTML("Protein of the Food (default in grams)"),
        text=HTML(Food.MODULE_HELP['protein'])
        ).run())

    record = {
        "domain": domain,
        "name": name,
        "portion": portion,
        "unit": unit,
        "calories": calories,
        "fat": fat,
        "cholesterol": cholesterol,
        "sodium": sodium,
        "carbohydrate": carbohydrate,
        "protein": protein,
        "t_s": A.now().format("YYYY-MM-DD HH:mm"),
    }

    formatted_text = FormattedText([
        ("italic",F"Domain: {domain}\n"),
        ("italic",F"Name: {name}\n"),
        ("italic",F"Portion: {portion}\n"),
        ("italic",F"Unit: {unit}\n"),
        ("italic",F"Calories: {calories}\n"),
        ("italic",F"Fat: {fat}\n"),
        ("italic",F"Cholesterol {cholesterol}\n"),
        ("italic",F"Sodium {sodium}\n"),
        ("italic",F"Carbohydrate: {carbohydrate}\n"),
        ("italic",F"Protein: {protein}\n")
    ])

    if _ := yes_no_dialog(title=HTML("Is this correct?"),text=formatted_text).run():
        commit_rollback =  "_"
        f_r = Food.Records(**record).record_add()
        if f_r > 0:
            commit_rollback = button_dialog(
            title=HTML("Commit or Delete the new record"),
            text=HTML("Click on <u>Commit</u> and the data will be stored and backed up, <u>Rollback</u> to delete the last record or <u>exit</u> to leave the data without backing up the database."),
            buttons=[("Commit","commit"),("Rollback","rollback"),("Exit","_")]
            ).run()
        if commit_rollback == "commit":
            Food.Records.records_backup_restore('c')
            r_s = str(f_r)
        elif commit_rollback == 'rollback':
            Food.Records.records_backup_restore('d')
            r_s = str(f_r)
    return r_s

if __name__ == '__main__':
    print(main())
