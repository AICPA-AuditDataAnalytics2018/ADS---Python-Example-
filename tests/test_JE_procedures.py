import pandas as pd
import pytest
from samples.Test_Procedures import Test_1_Procedures


class Test_Procedure_1:
    def test_check_gl_entries(self):
        df_gl_sample = pd.read_csv("../samples/data/"+
                                "GL_Detail_YYYYMMDD_YYYYMMDD.csv")

        result = Test_1_Procedures.check_for_gaps_in_JE_ID(df_gl_sample,
                        Journal_ID_Column = "Journal_ID", output_file = None)

        assert result == 12

    def test_comparison_of_entries_of_GL_and_log_files(self):
        df_log_sample = pd.read_csv("../samples/data/log_file.csv")
        df_gl_sample = pd.read_csv("../samples/data/"+
                                "GL_Detail_YYYYMMDD_YYYYMMDD.csv")

        result = Test_1_Procedures.comparison_of_entries_of_GL_and_log_file(
                   GL_Detail = df_gl_sample, Log_File = df_log_sample, 
                    output_file = None)

        assert result == 0
    
    def test_comparison_of_amounts_of_GL_and_log_files(self):
        df_log_sample = pd.read_csv("../samples/data/log_file.csv")
        df_gl_sample = pd.read_csv("../samples/data/"+
                                "GL_Detail_YYYYMMDD_YYYYMMDD.csv")

        df_gl_sample['Net'] = df_gl_sample.apply(lambda x: x['Amount'] * -1 if
                x['Amount_Credit_Debit_Indicator']=='H' else x['Amount'], axis=1)

        result = Test_1_Procedures.comparison_of_amounts_of_GL_and_log_file(
                    GL_Detail=df_gl_sample, Log_File=df_log_sample, 
                    output_file = None)

        assert result == 2
