import pandas as pd
import pytest
from samples.Test_Procedures import Test_1_Procedures, Test_2_Procedures


df_log_sample = pd.read_csv("../samples/data/log_file.csv")
df_gl_sample = pd.read_csv("../samples/data/"+
                                "GL_Detail_YYYYMMDD_YYYYMMDD.csv")

df_gl_sample['Net'] = df_gl_sample.apply(lambda x: x['Amount'] * -1 if
        x['Amount_Credit_Debit_Indicator']=='H' else x['Amount'], axis=1)

class Test_Procedure_1:

    def test_check_gl_entries(self):

        assert 12 == Test_1_Procedures.check_for_gaps_in_JE_ID(df_gl_sample,
                        Journal_ID_Column = "Journal_ID", output_file = None)

    def test_comparison_of_entries_of_GL_and_log_files(self):

        assert 0 == Test_1_Procedures.comparison_of_entries_of_GL_and_log_file(
                        GL_Detail = df_gl_sample, Log_File = df_log_sample, 
                        output_file = None)

    def test_comparison_of_amounts_of_GL_and_log_files(self):

        assert 2 == Test_1_Procedures.comparison_of_amounts_of_GL_and_log_file(
                    GL_Detail=df_gl_sample, Log_File=df_log_sample, 
                    output_file = None)

    def test_check_for_incomplete_entries(self):

        assert 4 == Test_2_Procedures.check_for_incomplete_entries(
                        GL_Detail = df_gl_sample, output_file = None)

    def test_check_for_duplicate_entries(self):

        assert 6919 == Test_2_Procedures.check_for_duplicate_entries(
                            GL_Detail = df_gl_sample, output_file = None)

    def test_check_for_round_dollar_entries(self):

        assert 226 == Test_2_Procedures.check_for_round_dollar_entries(
                            GL_Detail = df_gl_sample, output_file = None)

    def test_check_for_post_date_entries(self):

        assert 149 == Test_2_Procedures.check_for_post_date_entries(
                            GL_Detail = df_gl_sample, output_file = None)

    def test_check_for_weekend_entries(self):

        assert 0 == Test_2_Procedures.check_for_weekend_entries(
                            GL_Detail = df_gl_sample, output_file = None)

    def test_check_for_nights_entries(self):

        assert 190 == Test_2_Procedures.check_for_nights_entries(
                            GL_Detail = df_gl_sample, output_file = None)

    def test_check_for_rare_users(self):

        assert 52 == Test_2_Procedures.check_for_rare_users(
                            GL_Detail = df_gl_sample, output_file = None)

    def test_check_for_rare_accounts(self):

        assert 32 == Test_2_Procedures.check_for_rare_accounts(
                            GL_Detail = df_gl_sample, output_file = None)

