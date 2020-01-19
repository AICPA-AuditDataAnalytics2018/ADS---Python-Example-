# Audit Data Standards Python Example

This repository displays the benefits of using Python and the Jupyter Notebook in a financial statement audit.

## Requirements

If you haven't already installed Python 3 and Jupyter, the easiest way to install both is by using [Anaconda](https://www.anaconda.com/distribution/).

## Usage

TODO: Write usage instructions
1. [How to reshape SAP Data for your
   audit](https://github.com/AICPA-AuditDataAnalytics2018/ADS---Python-Example-/blob/master/samples/reshape_rename_sap_data.ipynb)
2. [How to reshape Quickbooks General Ledger Data for your audit](https://github.com/AICPA-AuditDataAnalytics2018/ADS---Python-Example-/blob/master/samples/quickbooksGLtoDatabase.py)
3. [How to split a DataFrame (csv, xlsx, other) using pandas and
   groupby](https://github.com/AICPA-AuditDataAnalytics2018/ADS---Python-Example-/blob/master/samples/Split%20Dataframe%20with%20Groupby.ipynb)

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Add your changes: `git add *`
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request :smile:

## History

TODO: Write history

** Consider adding an __init__ method to Test_Procedures, to reduce data entry:
```python
def __init__(self, GL_Detail, Log_File=None, JE_Column=None, Output=None):
   # Checks to make sure data is valid
   assert JE_Column in GL_Detail.columns
   self.GL_Detail = GL_Detail
   ...
def run():
   # Execute all procedures in module
```

## Credits

TODO: Write credits

## License

Apache 2.0
