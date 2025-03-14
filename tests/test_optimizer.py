"""Tests for the Optimizer class."""

import pandas as pd

from corefolio.constraint import MaxAssetsConstraint, MeanConstraint
from corefolio.universe import Universe
from corefolio.optimizer import Optimizer


def test_optimizer_with_max_assets_constraint():
    """
    Test the Optimizer class with MaxAssetsConstraint.
    Ensures that the optimizer selects the correct number of assets.
    """
    df = pd.DataFrame({"ID": [1, 2, 3, 4], "value": [10, 20, 30, 40]})
    universe = Universe(df)
    constraints = [MaxAssetsConstraint(max_assets=2)]
    optimizer = Optimizer(universe, constraints,
                          sense="maximize", target_column="value")
    selected_ids = optimizer.optimize()
    assert len(selected_ids) <= 2
    assert all(id in df["ID"].values for id in selected_ids)


def test_optimizer_with_mean_constraint():
    """
    Test the Optimizer class with MeanConstraint.
    Ensures that the optimizer applies the mean constraint correctly.
    """
    df = pd.DataFrame({"ID": [1, 2, 3, 4], "value": [
                      10, 20, 30, 40], "other_value": [5, 5, 5, 5]})
    universe = Universe(df)
    constraints = [MeanConstraint(column_name="other_value", tolerance=0.01)]
    optimizer = Optimizer(universe, constraints,
                          sense="maximize", target_column="value")
    selected_ids = optimizer.optimize()
    assert len(selected_ids) > 0
    assert all(id in df["ID"].values for id in selected_ids)


def test_optimizer_with_mean_constraint_min_max():
    """
    Test the Optimizer class with MeanConstraint using min_value and max_value.
    Ensures that the optimizer applies the mean constraint correctly with absolute values.
    """
    df = pd.DataFrame({"ID": [1, 2, 3, 4], "value": [
                      10, 20, 30, 40], "other_value": [5, 5, 5, 5]})
    universe = Universe(df)
    constraints = [MeanConstraint(
        column_name="other_value", min_value=4.9, max_value=5.1)]
    optimizer = Optimizer(universe, constraints,
                          sense="maximize", target_column="value")
    selected_ids = optimizer.optimize()
    assert len(selected_ids) > 0
    assert all(id in df["ID"].values for id in selected_ids)


def test_optimizer_with_categorical_mean_constraint():
    """
    Test the Optimizer class with MeanConstraint on a categorical column.
    Ensures that the optimizer applies the mean constraint correctly for categorical data.
    """
    df = pd.DataFrame({"ID": [1, 2, 3, 4], "value": [
                      10, 20, 30, 40], "category": ["A", "A", "B", "B"]})
    universe = Universe(df)
    constraints = [MeanConstraint(column_name="category", tolerance=0.01)]
    optimizer = Optimizer(universe, constraints,
                          sense="maximize", target_column="value")
    selected_ids = optimizer.optimize()
    assert len(selected_ids) > 0
    assert all(id in df["ID"].values for id in selected_ids)


def test_optimizer_with_multiple_constraints():
    """
    Test the Optimizer class with multiple constraints.
    Ensures that the optimizer applies all constraints correctly.
    """
    df = pd.DataFrame({"ID": [1, 2, 3, 4], "value": [10, 20, 30, 40], "other_value": [
                      5, 5, 5, 5], "category": ["A", "A", "B", "B"]})
    universe = Universe(df)
    constraints = [
        MaxAssetsConstraint(max_assets=2),
        MeanConstraint(column_name="other_value", tolerance=0.01),
        MeanConstraint(column_name="category", tolerance=0.01)
    ]
    optimizer = Optimizer(universe, constraints,
                          sense="maximize", target_column="value")
    selected_ids = optimizer.optimize()
    assert len(selected_ids) <= 2
    assert all(id in df["ID"].values for id in selected_ids)
