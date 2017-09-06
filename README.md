# NU Course Search

This command line program uses Northwestern's API data to make it easier for students to search for various classes.

## Usage
Make sure to install the google Python module.

`pip install google`

Obtain a Northwestern API Key from this [link](http://developer.asg.northwestern.edu/) and enter it into:

```python
API_KEY = '<NORTHWESTERN API KEY>'
```

Once the program starts, it will query Northwestern's API for course data.  Then, search for classes using the class subject and the class number.  For example, EECS 111-0 or MUSIC 126-2.

Enter Y or N at the prompted line to quit or search again, respectively.
