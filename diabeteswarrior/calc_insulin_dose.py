#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calculates the insulin dose."""

# pylint: disable=too-many-arguments
# pylint: disable=line-too-long
def main(weight:float = 129.5, meal:int = 0, act_bs:int = 1, tgt_bs:int = 100, cor_fac_wgt:float = 0.5, fg_bias:float = 0.6)->object:
    """Calculate the bolus & basal insulin dose to cover a meal and or correct your blood sugar."""
    # todo write this help.
    # todo write the unit tests
    # todo weight should be read from the health module
    #todo act_bs should be read from the scan module

    tdi:int = round( weight/4)
    meal_cvg:float = (meal*(1/((500*cor_fac_wgt)/tdi)))
    cor_cvg:float = ((act_bs-tgt_bs)/((1800*cor_fac_wgt)/tdi))
    tmd:int = round(meal_cvg+cor_cvg)
    bolus:int = round(tmd*fg_bias)
    basal:int = round(tmd-bolus)
    return F"Bolus dose: {bolus}, Basal dose: {basal}, Total dose: {tmd}"

if __name__ == '__main__':
    print(main(act_bs=180, meal=15))
