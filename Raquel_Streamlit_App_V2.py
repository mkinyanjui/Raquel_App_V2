import streamlit as st
import pandas as pd
import numpy as np
import base64
st.beta_set_page_config(layout='wide')


def main():

    st.title('Automated Excel Process')

    """
    Created by Mark Kinyanjui

    """

    """
    ### Step 1: Import Data
    """

    df = st.file_uploader(
        'Import dataset - make sure the $ is removed from both tabs')

    if df is not None:
        df_enrollment = pd.read_excel(df, sheet_name='Enrollments')
        df_payroll = pd.read_excel(df, sheet_name='Payroll')
        """
        ### Step 2: Merging the data & results
        """
        df_enrollment = df_enrollment.groupby(
            ['NAME', 'COMPANY CODE', 'POSITION ID', 'DEDUCTION CODE', 'EMPLOYEE STATUS']).sum('ENROLLMENT AMOUNT').reset_index()

        df_payroll = df_payroll.groupby(['NAME', 'COMPANY CODE',
                                         'POSITION ID', 'DEDUCTION CODE']).sum('DEDUCTION AMOUNT').reset_index()

        st.text(
            'Changing Payroll Deduction Code AC1 to match Enrollment Deduction Code ACC')
        # PAYROLL CHANGE ACC TO AC1
        df_payroll = df_payroll.replace(to_replace='AC1', value='ACC')
        df_enrollment = df_enrollment.replace(to_replace='AC1', value='ACC')

        # Merge the data
        clean = pd.merge(df_enrollment, df_payroll, how='left', left_on=[
                         'POSITION ID', 'DEDUCTION CODE'], right_on=['POSITION ID', 'DEDUCTION CODE'])

        clean = clean[['NAME_x', 'COMPANY CODE_x', 'POSITION ID',
                       'DEDUCTION CODE', 'EMPLOYEE STATUS', 'ENROLLMENT AMOUNT', 'DEDUCTION AMOUNT']]

        clean.columns = ['NAME', 'COMPANY CODE',
                         'POSITION ID', 'DEDUCTION CODE', 'EMPLOYEE STATUS', 'ENROLLMENT  AMOUNT', 'PAYROLL DEDUCTION']
        st.write(clean)
        """
        ### Step 3: Download the Data
        The below link allows you to download the data for further use
        """
        if df is not None:
            clean_exp = clean.to_csv(index=False)
            # When no file name is given, pandas returns the CSV as a string, nice.
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(clean_exp.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ** &lt;file_name&gt;.csv**)'
            st.markdown(href, unsafe_allow_html=True)
        """
        ### Step 4: Enrollment Only Data
        The table below shows people that only appeared in the **Enrollments** table but never on payroll
        """

        # Create Unique Keys to be able to use for a clean merge and join
        df_enrollment['KEY'] = df_enrollment['POSITION ID'] + \
            '-' + df_enrollment['DEDUCTION CODE']
        df_enrollment['KEY1'] = df_enrollment['POSITION ID'] + \
            '-' + df_enrollment['DEDUCTION CODE']
        df_payroll['KEY'] = df_payroll['POSITION ID'] + \
            '-' + df_payroll['DEDUCTION CODE']
        df_payroll['KEY2'] = df_payroll['POSITION ID'] + \
            '-' + df_payroll['DEDUCTION CODE']

        # Enrollment only first
        df_enrollment_only = pd.merge(df_enrollment, df_payroll, on=[
                                      'KEY', 'KEY'], how='left')
        df_enrollment_only = df_enrollment_only[~(
            df_enrollment_only.KEY1 == df_enrollment_only.KEY2)]
        df_enrollment_only = df_enrollment_only.drop(['KEY1', 'KEY2'], axis=1)
        # Final dataframe showing enrollment only data

        df_enrollment_only = df_enrollment_only.groupby(
            ['NAME_x', 'DEDUCTION CODE_x']).sum(['ENROLLMENT AMOUNT']).reset_index()
        df_enrollment_only.columns = [
            'NAME', 'DEDUCTION CODE', 'ENROLLMENT AMOUNT', 'DEDUCTION AMOUNT']
        st.write(df_enrollment_only)
        """
        ### Step 5: Enrollment Data Download
        The link below will allow you to download the **enrollment** data
        """
        if df is not None:
            df_enrollment_only = df_enrollment_only.to_csv(index=False)
            # When no file name is given, pandas returns the CSV as a string, nice.
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(df_enrollment_only.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ** &lt;file_name&gt;.csv**)'
            st.markdown(href, unsafe_allow_html=True)

        """
        ### Step 6: Payroll Only Data
        The table below shows people that only appeared in the **Payroll** table but never in the Enrolled table
        """
        df_payroll_only = pd.merge(df_payroll, df_enrollment, on=[
                                   'KEY', 'KEY'], how='left')
        df_payroll_only = df_payroll_only[~(
            df_payroll_only.KEY2 == df_payroll_only.KEY1)]
        df_payroll_only = df_payroll_only.drop(['KEY2', 'KEY1'], axis=1)
        # Final dataframe showing Payroll only data
        df_payroll_only = df_payroll_only.groupby(
            ['NAME_x', 'DEDUCTION CODE_x']).sum(['DEDUCTION AMOUNT']).reset_index()
        df_payroll_only.columns = [
            'NAME', 'DEDUCTION CODE', 'DEDUCTION AMOUNT', 'ENROLLMENT AMOUNT']
        st.write(df_payroll_only)
        """
        ### Step 7: Payroll Data Download
        The link below will allow you to download the **payroll** data
        """
        if df is not None:
            df_payroll_only = df_payroll_only.to_csv(index=False)
            # When no file name is given, pandas returns the CSV as a string, nice.
            # some strings <-> bytes conversions necessary here
            b64 = base64.b64encode(df_payroll_only.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ** &lt;file_name&gt;.csv**)'
            st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
