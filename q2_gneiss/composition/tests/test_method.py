# ----------------------------------------------------------------------------
# Copyright (c) 2017-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import unittest
import numpy as np
import pandas as pd
from skbio.tree import TreeNode
from gneiss.cluster import gradient_linkage
import pandas.testing as pdt

from q2_gneiss.composition._method import (
    ilr_hierarchical, ilr_phylogenetic, ilr_phylogenetic_ordination
)
from q2_gneiss._util import add_pseudocount


class TestAddPseudocount(unittest.TestCase):

    def test_add_pseudocount(self):
        table = pd.DataFrame(
            [[1., 2., 3., 4.], [1., 0., 2., 1.], [0., 2., 1., 3.]],
            columns=['a', 'b', 'c', 'd'], index=[1, 2, 3])
        obs = add_pseudocount(table)
        exp = pd.DataFrame(
            [[1., 2., 3., 4.], [1., 0.5, 2., 1.], [0.5, 2., 1., 3.]],
            columns=['a', 'b', 'c', 'd'], index=[1, 2, 3])
        pdt.assert_frame_equal(obs, exp)

    def test_add_pseudocount_2(self):
        table = pd.DataFrame(
            [[1.0, 2.0, 2.5], [0.5, 0.0, 1.0], [0.0, 0.5, 1.0]],
            columns=['a', 'b', 'c'], index=[1, 2, 3])
        obs = add_pseudocount(table, 0.5)
        exp = pd.DataFrame(
            [[1.0, 2.0, 2.5], [0.5, 0.5, 1.0], [0.5, 0.5, 1.0]],
            columns=['a', 'b', 'c'], index=[1, 2, 3])
        pdt.assert_frame_equal(obs, exp)

    def test_add_pseudocount_3(self):
        table = pd.DataFrame(
            [[1.7, 1.3, 0.5], [1.5, 3.2, 1.1]],
            columns=['a', 'b', 'c'], index=[1, 2])
        obs = add_pseudocount(table, 2.0)
        exp = pd.DataFrame(
            [[1.7, 1.3, 0.5], [1.5, 3.2, 1.1]],
            columns=['a', 'b', 'c'], index=[1, 2])
        pdt.assert_frame_equal(obs, exp)


class TestILRTransform(unittest.TestCase):

    def test_ilr_hierarchical(self):
        np.random.seed(0)
        table = pd.DataFrame([[1, 1, 2, 2],
                              [1, 2, 2, 1],
                              [2, 2, 1, 1]],
                             index=[1, 2, 3],
                             columns=['a', 'b', 'c', 'd'])
        table = table.reindex(columns=np.random.permutation(table.columns))
        ph = pd.Series([1, 2, 3], index=table.index)
        tree = gradient_linkage(table, ph)
        res_balances = ilr_hierarchical(table, tree)
        exp_balances = pd.DataFrame(
            [[0.693147, -5.551115e-17, 2.775558e-17],
             [0.000000, -4.901291e-01, -4.901291e-01],
             [-0.693147, 5.551115e-17, -2.775558e-17]],
            columns=['y0', 'y1', 'y2'],
            index=[1, 2, 3])
        pdt.assert_frame_equal(res_balances, exp_balances)

    def test_ilr_phylogenetic(self):
        np.random.seed(0)
        table = pd.DataFrame([[1, 1, 2, 2],
                              [1, 2, 2, 1],
                              [2, 2, 1, 1]],
                             index=[1, 2, 3],
                             columns=['a', 'b', 'c', 'd'])
        table = table.reindex(columns=np.random.permutation(table.columns))
        tree = TreeNode.read([
            '((c:0.025,d:0.025,f:0.1,e:0.025):0.2,(b:0.025,a:0.025):0.2);'])
        res_balances, res_tree = ilr_phylogenetic(table, tree)
        exp_balances = pd.DataFrame(
            [[0.693147, 0.0, 3.892122e-17],
             [0.0, -4.901291e-01, -4.901291e-01],
             [-0.693147, -5.551115e-17, -3.892122e-17]],
            columns=['y0', 'y1', 'y2'],
            index=[1, 2, 3])

        pdt.assert_frame_equal(res_balances, exp_balances)
        exp_tree_str = ('((b:0.025,a:0.025)y1:0.2,'
                        '(c:0.025,d:0.025)y2:0.2)y0;\n')
        self.assertEqual(str(res_tree), exp_tree_str)

    def test_ilr_phylogenetic2(self):
        np.random.seed(0)
        table = pd.DataFrame([[1, 1, 2, 2],
                              [1, 2, 2, 1],
                              [2, 2, 1, 1]],
                             index=[1, 2, 3],
                             columns=['a', 'b', 'c', 'd'])
        table = table.reindex(columns=np.random.permutation(table.columns))
        tree = TreeNode.read([
            '((c:0.025,d:0.025,f:0.1,e:0.025):0.2,(b:0.025,a:0.025):0.2);'])
        res_balances, res_tree = ilr_phylogenetic(table, tree)
        exp_balances = pd.DataFrame(
            [[0.693147, 0.0, 3.892122e-17],
             [0.0, -4.901291e-01, -4.901291e-01],
             [-0.693147, -5.551115e-17, -3.892122e-17]],
            columns=['y0', 'y1', 'y2'],
            index=[1, 2, 3])

        pdt.assert_frame_equal(res_balances, exp_balances)
        exp_tree_str = ('((b:0.025,a:0.025)y1:0.2,'
                        '(c:0.025,d:0.025)y2:0.2)y0;\n')
        self.assertEqual(str(res_tree), exp_tree_str)

    def test_ilr_ordination(self):
        np.random.seed(0)
        table = pd.DataFrame([[1, 1, 2, 2],
                              [1, 2, 2, 1],
                              [2, 2, 1, 1]],
                             index=[1, 2, 3],
                             columns=['a', 'b', 'c', 'd'])
        table = table.reindex(columns=np.random.permutation(table.columns))
        tree = TreeNode.read([
            '((c:0.025,d:0.025,f:0.1,e:0.025):0.2,(b:0.025,a:0.025):0.2);'])
        res_ord, res_tree, res_md = ilr_phylogenetic_ordination(
            table, tree, top_k_var=3)
        exp_balances = pd.DataFrame(
            [[0.693147, 0.0, 3.892122e-17],
             [0.0, -4.901291e-01, -4.901291e-01],
             [-0.693147, -5.551115e-17, -3.892122e-17]],
            columns=['y0', 'y1', 'y2'],
            index=[1, 2, 3])

        exp_balances = exp_balances[['y0', 'y1', 'y2']]
        exp_balances.index.name = 'sampleid'
        pdt.assert_frame_equal(res_ord.samples, exp_balances)
        exp_tree_str = ('((b:0.025,a:0.025)y1:0.2,'
                        '(c:0.025,d:0.025)y2:0.2)y0;\n')
        self.assertEqual(str(res_tree), exp_tree_str)

        exp_md = pd.DataFrame([[-0.5, -0.707107, 0.000000],
                               [-0.5, 0.707107, 0.000000],
                               [0.5, 0.000000, -0.707107],
                               [0.5, 0.000000, 0.707107]],
                              columns=['y0', 'y1', 'y2'],
                              index=['b', 'a', 'c', 'd'])
        exp_md.index.name = 'featureid'
        pdt.assert_frame_equal(res_md, exp_md)


if __name__ == '__main__':
    unittest.main()
