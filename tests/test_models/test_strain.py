#!/usr/bin/env python3
"""Strain Testing Module"""
import pytest
from app.models.strain import Strain

def test_strain_init():
    """ """
    strain = Strain(
        name="Test Strain",
        type="Indica",
        delta_nine_concentration=10.0,
        cbd_concentration=5.0,
        terpene_profile="Myrcene, Limonene, Caryophyllene",
        effects="Relaxed, Euphoric, Sleepy",
        uses="Pain Relief, Anxiety, Insomnia",
        flavor="Earthy, Pine, Sweet"
    )

    assert strain.name == "Test Strain"
    assert strain.type == "Indica"
    assert strain.delta_nine_concentration == 10.0
    assert strain.cbd_concentration == 5.0
    assert strain.terpene_profile == "Myrcene, Limonene, Caryophyllene"
    assert strain.effects == "Relaxed, Euphoric, Sleepy"
    assert strain.uses == "Pain Relief, Anxiety, Insomnia"
    assert strain.flavor == "Earthy, Pine, Sweet"

def test_strain_init_no_args():
    """ """
    strain = Strain()

    assert strain.name is None
    assert strain.type is None
    assert strain.delta_nine_concentration is None
    assert strain.cbd_concentration is None
    assert strain.terpene_profile is None
    assert strain.effects is None
    assert strain.uses is None
    assert strain.flavor is None
